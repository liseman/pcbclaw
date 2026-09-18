#!/usr/bin/env python3
"""Synthetic offline checks. No real board, manufacturing export or network."""
import csv, json, pathlib, tempfile, unittest
import pcb_helpers as h

class Tests(unittest.TestCase):
    def test_routes(self):
        self.assertEqual(h.route("pcb")["mode"],"interview")
        text="ESP32 temperature logger powered by USB-C"
        self.assertEqual(h.route("pcb "+text)["supplied_requirements"],text)
        for mode in ["modify","resume","reprice","package"]:
            self.assertEqual(h.route("pcb "+mode+" ~/pcb-projects/demo")["mode"],mode)
        with self.assertRaises(ValueError):h.route("pcboard")
    def test_precedence(self):
        a={"fabrication":{"layers":2,"finish":"HASL"}}
        b={"fabrication":{"layers":4}}
        c={"fabrication":{"finish":"ENIG"}}
        d={"fabrication":{"layers":6}}
        self.assertEqual(h.merge(a,b,c,d),{"fabrication":{"layers":6,"finish":"ENIG"}})
        self.assertEqual(a["fabrication"]["layers"],2)
    def test_quantity_selection(self):
        # Synthetic lists only, never claims about JLCPCB's real range.
        self.assertEqual(h.quantities([2,6,8,12]),{"MINIMUM":2,"MIDDLE":6,"MAXIMUM":12})
        self.assertEqual(h.quantities([2,5,19]),{"MINIMUM":2,"MIDDLE":5,"MAXIMUM":19})
        self.assertIsNone(h.quantities([2,12])["MIDDLE"])
        self.assertIsNone(h.quantities([2])["MAXIMUM"])
        for value in [[],[0],[2.5],[True]]:
            with self.assertRaises(ValueError):h.quantities(value)
    def test_unknown_costs(self):
        d={"service":"Economic PCBA","currency":"TEST","timestamp":"fixture","quantity_source":"synthetic","quantity_verified":True,"valid_quantities":[2,6,12],"rows":{"2":{"pcb_fab":4,"components":None,"assembly_setup_other":3}}}
        r=h.costs(d)["rows"][0]
        self.assertEqual(r["known_subtotal"],7)
        self.assertIsNone(r["estimated_total"])
        d["rows"]["2"]["components"]=3
        self.assertEqual(h.costs(d)["rows"][0]["cost_per_assembled_board"],5)
        d["quantity_verified"]=False
        self.assertTrue(all(x["assembled_qty"] is None for x in h.costs(d)["rows"]))
        d["service"]="Standard PCBA"
        with self.assertRaises(ValueError):h.costs(d)
    def test_files(self):
        with tempfile.TemporaryDirectory() as temp:
            base=pathlib.Path(temp);project=base/"fixture";project.mkdir()
            (project/"source.txt").write_text("synthetic non-CAD fixture")
            saved=h.backup(project,base/"backups")
            self.assertEqual(saved["verified_files"],1)
            with self.assertRaises(ValueError):h.backup(project,project/"bad")
            packed=h.package(project,base/"bundle.zip")
            self.assertEqual(len(packed["files"]),1)
            with self.assertRaises(ValueError):h.package(project,base/"bundle.zip")
            bom=base/"bom.csv";cpl=base/"cpl.csv"
            bom.write_text('Designator,Quantity,LCSC\n"R1,R2",2,fixture\n')
            cpl.write_text("Designator\nR1\nR2\n")
            self.assertEqual(h.crosscheck(bom,cpl)["matched_references"],2)
            cpl.write_text("Designator\nR1\nR1\n")
            with self.assertRaises(ValueError):h.crosscheck(bom,cpl)
            (project/".env").write_text("synthetic")
            with self.assertRaises(ValueError):h.package(project,base/"rejected.zip")
    def test_policy_contract(self):
        root=pathlib.Path(__file__).resolve().parents[1]
        s=(root/"SKILL.md").read_text()
        defaults=json.loads((root/"assets/defaults.json").read_text())
        self.assertLess(len(s),10000)
        self.assertIn("without another permission request",s)
        self.assertIn("require separate explicit authorization",s)
        self.assertTrue(defaults["permissions"]["local_manufacturing_generation_after_validation"])
        self.assertFalse(defaults["permissions"]["order"])
        self.assertEqual(defaults["costs"]["levels"],["MINIMUM","MIDDLE","MAXIMUM"])
        for ref in ["environment","design","release","costs","validation"]:
            self.assertTrue((root/"references"/(ref+".md")).is_file())

if __name__=="__main__":unittest.main()
