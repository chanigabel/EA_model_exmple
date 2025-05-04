# EA_GIT - Enterprise Architect Scripts & Tools

This repository contains a variety of scripts, installers, and helper files developed for working with Sparx Systems Enterprise Architect.

## 📁 Folder Structure

- **EA/** - EA project files (`.eap`, `.eapx`)
- **External Scripts/** - Python/VB scripts and utilities for EA automation and documentation
  - `SQL/` - SQL queries for EA
  - `TryScripts/` - Experimental or in-development scripts
- **Installers/** - MSI installers for EA Add-Ins
- **MDGs/** - Model Driven Generation XML files
- **Scripts_NotTested/** - Scripts not yet tested or approved
- **TevelEAAddin/** - Scripts and utilities specific to the Tevel EA Add-in
  - `DDL/` - Scripts for generating DDL from diagrams
  - `Exist_VBScript/` - Legacy or ported scripts
- **VBScripts/** - VBScript files for automation within EA

## 🛠 Example Scripts

- `DeleteTagValuesFromRequirement.py` – Deletes specific tagged values from requirements
- `ModelViewAndPie.py` – Generates charts from EA model elements
- `CreateActors.txt` – Creates actors with specific stereotypes

## 🧪 Status

- ✅ Tested scripts: In root of `External Scripts/`
- ⚠️ To try: In `TryScripts/`
- ❌ Not yet tested: In `Scripts_NotTested/`

## 📦 Installers

- `TevelEAAddinInstaller.msi` – Installer for the Tevel EA Add-in (32-bit)
- `ACTL Scripts.xml` – MDG technology file

## 📝 Notes

- Most Python scripts assume EA is accessible via the COM API.
- Use EA 15+ for best compatibility.