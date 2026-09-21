# Avionics Hardware
> 2026-2027 SRAD Avionics Hardware Repository

This repository contains **schematics**, **PCB layouts**, and related **documentation and datasheets** for QRET SRAD Avionics. 
- All ECAD was designed in or transferred to **KiCad 10**.
- Covers **all** avionics systems, including power, propulsion, recovery, telemetry, and shared libraries.
- The **main** branch contains the latest stable hardware that is not currently under active development.
- If you're contributing, please read over the [`Development Standards`](#development-standards) section.
---

## Folder Structure
Avionics systems are organized into root-level directories (e.g., `power/`, `telemetry/`, etc.). 

Each system contains folders per boards and a respective documentation file `AV-SYSTEM-HW.MD`

Each board follows the structure below:
- `docs`: Board-specific documentation, datasheets, and other reference materials. 
- `symbols`: Board-specific schematic symbols.
- `footprints`: Board-specific PCB footprints.
- `models`: Board-specific component 3D-models.

**Example Structure**
```
av-hardware/
  power/
    POWER-HW.md
    power-module/
      power-module.kicad_pro
      power-module.kicad_sch
      power-module.kicad_pcb
      docs/
        POWER-MODULE.md
        datasheets/
      symbols/
      footprints/
      models/
```

## Development Standards
- **Always** ensure you've fetched and pulled from Git before contributing.
```
git fetch origin
git pull
```
- Keep `main` stable. Never make changes directly on `main`.
- If contributing, use focused, concise, and descriptive branch names and commit messages. Look at standards below.
  
### Branches
Contribute by creating a branch.

**Naming Conventions**
- Creating a new board: `dev/<description>`
- Updating or adding a feature to an existing board: `feature/board/<description>`
- Resolving an issue on an existing board: `fix/board/<description>`
- Updating documentation and reference materials: `docs/<description>`

For example:
- `dev/camera-module`
- `feature/power-module/change-buck`
- `fix/lcm/can-trx`

### Commits
Commit messages should be focused, concise, and descriptive. Each commit should represent a single logical change.
- You should try and commit after making a **single change**, rather than committing for several changes at once.

**Examples**
```text
Setup schematic env for camera module
Tune differential pair lengths
Update comms module with new LoRa module
Review updated comms module
```

### Pull Requests
Pull requests should clearly describe the changes being introduced and their purpose.

Before opening a pull request:

- Ensure the branch is up to date with `main`.
- Ensure all work and changes are peer-reviewed in person during meetings or office hours.
- Confirm that no unrelated changes are included.

**Title Convention**

```text
<type/board-name>: <short-description>
```
For example:
```text
feature/power-module: Change buck converter
fix/lcm: Switch to standard CAN transceiver
dev/camera-module: Initial design
docs/gps-antenna: Add images to documentation
```
If you're ever unsure about anything, reach out to one us leads!!

---
QRET, 2026-2027
