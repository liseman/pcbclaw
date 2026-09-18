#!/usr/bin/env python3
"""Small offline PCB workflow helpers. No upload, order, CAD edit or live pricing."""
import argparse, csv, datetime, hashlib, json, pathlib, shutil, subprocess, sys, tarfile, zipfile

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def route(text):
    words = text.strip().split(maxsplit=1)
    if not words or words[0].lower() != "pcb":
        raise ValueError("Not a pcb invocation")
    tail = words[1] if len(words) > 1 else ""
    if not tail:
        return {"mode":"interview", "question":"What should the board do? Describe its purpose and any power, connection, or size requirements you already know?"}
    mode = tail.split(maxsplit=1)[0].lower()
    if mode in {"modify","resume","reprice","package"}:
        return {"mode":mode, "arguments":tail[len(mode):].strip()}
    return {"mode":"design", "supplied_requirements":tail}

def merge(*values):
    out = {}
    for value in values:
        for key, item in value.items():
            out[key] = merge(out.get(key, {}) if isinstance(out.get(key), dict) else {}, item) if isinstance(item, dict) else item
    return out

def preflight(stage):
    result = {"stage":stage,"tools":{}}
    names = ["git"] if stage in {"interview","reprice"} else ["git","kicad-cli"]
    for name in names:
        executable = shutil.which(name)
        item = {"available":bool(executable),"path":executable}
        if executable:
            proc = subprocess.run([executable,"version" if name == "kicad-cli" else "--version"],capture_output=True,text=True,timeout=20)
            item.update(returncode=proc.returncode,version=proc.stdout.strip())
        result["tools"][name] = item
    root = pathlib.Path.home()/"pcb-projects"
    result["workspace_exists"] = root.is_dir()
    result["standards_exists"] = (root/"standards/JLCPCB.md").is_file()
    result["template_exists_not_validated"] = (root/"templates/jlcpcb-2layer").is_dir()
    result["note"] = "Check only needed subcommands via installed --help; catalog/network/GUI and template correctness require independent checks."
    return result

def backup(project, destination):
    project, destination = project.resolve(), destination.resolve()
    if not project.is_dir() or destination == project or project in destination.parents:
        raise ValueError("Backup destination must be outside an existing project")
    paths = sorted(project.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise ValueError("Review symlinks explicitly before complete backup")
    hashes = {str(p.relative_to(project)):digest(p) for p in paths if p.is_file()}
    if not hashes:
        raise ValueError("Empty project")
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination.mkdir(parents=True,exist_ok=True)
    output = destination/(project.name+"-"+stamp+".tar.gz")
    with tarfile.open(output,"x:gz") as archive:
        archive.add(project,arcname=project.name)
    with tarfile.open(output) as archive:
        actual = {str(pathlib.PurePosixPath(m.name).relative_to(project.name)):hashlib.sha256(archive.extractfile(m).read()).hexdigest() for m in archive.getmembers() if m.isfile()}
    after = {str(p.relative_to(project)):digest(p) for p in project.rglob("*") if p.is_file()}
    if hashes != actual or hashes != after:
        raise ValueError("Project changed or archive verification failed; preserve archive and retry after safe save")
    return {"backup":str(output),"bytes":output.stat().st_size,"sha256":digest(output),"verified_files":len(hashes)}

def quantities(valid):
    if not isinstance(valid,list) or not valid or any(type(q) is not int or q <= 0 for q in valid):
        raise ValueError("Supply verified positive integer finished-board quantities")
    q = sorted(set(valid))
    middle = min(q[1:-1],key=lambda x:(abs(2*x-q[0]-q[-1]),x)) if len(q)>=3 else None
    return {"MINIMUM":q[0],"MIDDLE":middle,"MAXIMUM":q[-1] if len(q)>1 else None}

def costs(data):
    if data.get("service") != "Economic PCBA":
        raise ValueError("Default calculator is Economic PCBA only")
    for field in ("currency","timestamp","quantity_source"):
        if not data.get(field):
            raise ValueError("Missing "+field)
    selection = quantities(data["valid_quantities"]) if data.get("quantity_verified") is True else dict.fromkeys(["MINIMUM","MIDDLE","MAXIMUM"])
    output=[]
    for level,qty in selection.items():
        item=data.get("rows",{}).get(str(qty),{}) if qty is not None else {}
        values=[item.get(k) for k in ("pcb_fab","components","assembly_setup_other")]
        for value in values:
            if value is not None and (type(value) not in (int,float) or value < 0 or not __import__("math").isfinite(value)):
                raise ValueError("Costs must be nonnegative finite values or null")
        known=sum(v for v in values if v is not None)
        total=sum(values) if qty and all(v is not None for v in values) else None
        output.append(dict(level=level,assembled_qty=qty,pcb_fab=values[0],components=values[1],assembly_setup_other=values[2],known_subtotal=known if any(v is not None for v in values) else None,estimated_total=total,cost_per_assembled_board=total/qty if total is not None else None,kind=item.get("kind","unknown"),limitations=item.get("limitations","Verification required"),fabricated_qty=item.get("fabricated_qty"),panels=item.get("panels"),boards_per_panel=item.get("boards_per_panel")))
    return {"service":data["service"],"currency":data["currency"],"timestamp":data["timestamp"],"quantity_source":data["quantity_source"],"quantity_verified":data.get("quantity_verified") is True,"shipping_tax_duties":data.get("shipping_tax_duties","excluded"),"rows":output}

def crosscheck(bom,cpl):
    # Normalized inputs; verify supplier schema separately.
    with bom.open(newline="",encoding="utf-8-sig") as f: b=list(csv.DictReader(f))
    with cpl.open(newline="",encoding="utf-8-sig") as f: c=list(csv.DictReader(f))
    refs=[]
    for row in b:
        group=[x.strip() for x in row["Designator"].split(",") if x.strip()]
        if not group or int(row["Quantity"])!=len(group):
            raise ValueError("BOM Quantity must equal per-board designator count")
        if not row.get("LCSC","").strip():
            raise ValueError("Missing LCSC")
        refs.extend(group)
    positions=[row["Designator"].strip() for row in c]
    if not refs or any(not x for x in positions) or len(refs)!=len(set(refs)) or len(positions)!=len(set(positions)):
        raise ValueError("Empty or duplicate references")
    if set(refs)!=set(positions):
        raise ValueError("BOM/CPL fitted-reference mismatch")
    return {"matched_references":len(refs),"geometry_verified":False}

def package(source,output):
    source,output=source.resolve(),output.resolve()
    if not source.is_dir() or output==source or source in output.parents or output.exists():
        raise ValueError("Use a new archive outside a controlled staging directory")
    files=sorted(source.rglob("*"))
    if any(p.is_symlink() for p in files):
        raise ValueError("Symlink requires explicit review")
    paths=[p for p in files if p.is_file()]
    if not paths:
        raise ValueError("Empty delivery")
    forbidden={".git",".env","__pycache__","node_modules"}
    if any(any(x in forbidden for x in p.relative_to(source).parts) or p.suffix in {".pem",".key",".lck",".kicad_prl"} for p in paths):
        raise ValueError("Sensitive/editor/cache paths in staging; inspect and remove from staging only")
    # This check cannot prove absence of secrets. Review the explicit staging file list first.
    expected={p.relative_to(source).as_posix():digest(p) for p in paths}
    with zipfile.ZipFile(output,"x",zipfile.ZIP_DEFLATED) as z:
        for p in paths: z.write(p,p.relative_to(source).as_posix())
    with zipfile.ZipFile(output) as z:
        if z.testzip() or {n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}!=expected:
            raise ValueError("ZIP validation failed")
    return {"archive":str(output),"sha256":digest(output),"files":expected}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    a=sub.add_parser("preflight");a.add_argument("stage",choices=["interview","design","modify","resume","reprice","package"])
    a=sub.add_parser("route");a.add_argument("text")
    a=sub.add_parser("backup");a.add_argument("project",type=pathlib.Path);a.add_argument("destination",type=pathlib.Path)
    a=sub.add_parser("quantities");a.add_argument("valid",help="JSON list of verified valid assembled quantities")
    a=sub.add_parser("costs");a.add_argument("input",type=pathlib.Path)
    a=sub.add_parser("crosscheck");a.add_argument("bom",type=pathlib.Path);a.add_argument("cpl",type=pathlib.Path)
    a=sub.add_parser("package");a.add_argument("source",type=pathlib.Path);a.add_argument("output",type=pathlib.Path)
    args=p.parse_args()
    if args.command=="preflight":result=preflight(args.stage)
    elif args.command=="route":result=route(args.text)
    elif args.command=="backup":result=backup(args.project,args.destination)
    elif args.command=="quantities":result=quantities(json.loads(args.valid))
    elif args.command=="costs":result=costs(json.loads(args.input.read_text()))
    elif args.command=="crosscheck":result=crosscheck(args.bom,args.cpl)
    else:result=package(args.source,args.output)
    print(json.dumps(result,indent=2))
if __name__=="__main__":
    try:main()
    except (ValueError,KeyError,OSError,subprocess.TimeoutExpired) as e:
        print("BLOCKED: "+str(e),file=sys.stderr);sys.exit(1)
