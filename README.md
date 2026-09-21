# PCBClaw — OpenClaw PCB workflow

Version: 0.2.0-beta.1 • License: MIT

Turn conversational PCB requirements into editable KiCad projects, verified manufacturing candidates and JLCPCB Economic PCBA cost comparisons. This is an agent workflow with offline helpers, not an autonomous CAD engine or a shell command named pcb. Independent engineering review and prototype testing remain necessary.

## Requirements

- OpenClaw with native AgentSkills, file/shell tools and public web research access.
- Python 3.10+ for bundled standard-library-only helpers.
- A supported stable KiCad with kicad-cli ERC, DRC and export commands for CAD stages; KiCad 9 is the initial target.
- Git optional for commits; missing author identity does not block work.
- A connected graphical desktop/computer tool only when CAD operations need it.
- Browser/account access only for authorized supplier quote/preview work.

Ubuntu is the initial administration target. Other operating systems require their own verified installation methods. No API key or provider configuration is included.

## Install from GitHub

```bash
openclaw skills install git:liseman/pcbclaw@v0.2.0-beta.1 --as pcb
openclaw skills info pcb
```

Start a new conversation and say `pcb`.

## Install from the release ZIP

1. Extract the ZIP. The pcb directory contains SKILL.md at its root.
2. Review the instructions and Python source before installation.
3. From the extraction directory run:

   `openclaw skills install ./pcb --as pcb`
4. Run `openclaw skills info pcb` and confirm its path and availability. Start a new conversation so skill discovery refreshes.
5. Say `pcb`. Expected response: one short question about purpose, power, connections and size, not a long questionnaire.

Commands were checked against OpenClaw 2026.9.4. Consult installed --help on other versions. Do not use --force over an existing customized skill; back it up, compare changes and deliberately replace it. If a Workshop or other pcb skill already exists, resolve duplicate precedence and confirm the discovered path before use. Local installs are refreshed by reinstalling a reviewed release, not by assuming registry updates.

## Use

- pcb
- pcb ESP32 temperature logger powered by USB-C
- pcb modify ~/pcb-projects/controller add reverse-polarity protection
- pcb resume ~/pcb-projects/controller
- pcb reprice ~/pcb-projects/controller
- pcb package ~/pcb-projects/controller

These are conversational requests, not guaranteed lexical interception. All supplied requirements are retained; only consequential gaps should be asked.

## Defaults and workspace

Bundled defaults: assets/defaults.json. First use initializes ~/pcb-projects/pcb-defaults.json if absent. Precedence: current request > existing project requirements > user defaults > bundled defaults. Project overrides do not alter future defaults.

Default fabrication: 2-layer rigid FR-4, 1.6 mm, 1 oz, green, ordinary economical options. Default assembly: JLCPCB Economic PCBA with technically suitable Basic/promotional parts. Price categories: Economic MINIMUM / MIDDLE / MAXIMUM of verified valid finished-board quantities, never invented fixed quantities. Current sourcing, pricing and service limits require live verification.

Projects live under ~/pcb-projects/. No private project, standards, existing template or credentials are distributed. Missing standards/template are created and verified on demand; see references/environment.md.

## Outputs and boundaries

Editable project/libraries, Gerbers/drills, fabrication ZIP, BOM/CPL, PDF, verification reports, cost comparison, source archive and complete bundle. Local generation follows successful validation without extra approval. Unresolved issues produce REVIEW REQUIRED or BLOCKED, not a manufacturing-ready claim. Uploads, publication, orders, payments and chargeable reservations require explicit authorization. No automatic purchase or login credential collection.

## Validation and limits

Run `python3 -B pcb/scripts/test_helpers.py` from the extraction directory. See RELEASE.md for exact tested scope, and references/validation.md for conversation acceptance cases. Helper tests do not prove circuit functionality, actual model interview behavior or supplier placement accuracy. Download delivery depends on the host interface; filesystem paths are not web download URLs.

## Contributions and reporting

See CONTRIBUTING.md. This release has no published support endpoint or registry listing. Report issues to the person or repository distributing your copy; include sanitized versions and a minimal synthetic reproduction, never credentials or private board files. Not affiliated with KiCad, JLCPCB or OpenClaw.
