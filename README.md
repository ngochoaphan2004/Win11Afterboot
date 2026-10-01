# 🚀 Win11 After Boot (v1.1.0)

A lightweight, modern post-installation setup utility for Windows 11. Quickly configure essential system settings and batch-install your favorite software silently.

---

## ⚡ Quick Install (One Command)

Open **PowerShell** and run:

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/ngochoaphan2004/Win11Afterboot/main/install.ps1")))
```

---

## ✨ Features

- **⚡ Silent App Installer**: Download and install essential tools unattended in the background:
  - **Browsers**: Google Chrome
  - **Development**: VS Code, Git, Node.js (v20, v22, v24), Python (choose versions 3.10 - 3.13), Visual Studio Community, Docker Desktop
  - **Communication**: Zalo
  - **Utilities**: WinRAR
- **🗓️ Instant Date Format Switcher**: Change Windows date formats (e.g. `dd/MM/yyyy`, `MM/dd/yyyy`, ISO `yyyy-MM-dd`) immediately without restarting your PC.
- **⚡ Concurrent Downloads**: Multi-threaded downloader with real-time speed, progress bars, and file size tracking.
- **🎨 Modern Dark UI**: Clean, responsive interface built with CustomTkinter.

---

## 🔨 Build Standalone Executable (.exe)

You can package the app into a portable standalone `.exe` using the included build script:

```powershell
.\build.ps1
```

The compiled binary will be saved in `dist\Win11AfterBoot.exe`.

---

## 📄 License

MIT License
