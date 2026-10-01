# 🚀 Win11 After Boot

A lightweight, modern post-installation setup utility for Windows 11. Quickly configure essential system settings and batch-install your favorite software silently.

---

## ⚡ Quick Install (One Command)

Open **PowerShell** and run:

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/<YOUR_USERNAME>/Win11Afterboot/main/install.ps1")))
```

> **Tip:** Replace `<YOUR_USERNAME>` with your GitHub username (or custom shortlink).

Alternatively, you can also use:
```powershell
irm "https://raw.githubusercontent.com/<YOUR_USERNAME>/Win11Afterboot/main/install.ps1" | iex
```

---

## ✨ Features

- **⚡ Silent App Installer**: Download and install essential tools unattended in the background:
  - **Browsers**: Google Chrome
  - **Development**: VS Code, Git, Python (choose versions 3.10 - 3.13), Visual Studio Community, Docker Desktop
  - **Utilities**: WinRAR
- **🗓️ Instant Date Format Switcher**: Change Windows date formats (e.g. `dd/MM/yyyy`, `MM/dd/yyyy`, ISO `yyyy-MM-dd`) immediately without restarting your PC.
- **⚡ Concurrent Downloads**: Multi-threaded downloader with real-time speed, progress bars, and file size tracking.
- **🎨 Modern Dark UI**: Clean, responsive interface built with CustomTkinter.

---

## 💻 Run from Source

### Prerequisites
- Windows 10 or 11
- Python 3.10+ installed

### Steps

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/<YOUR_USERNAME>/Win11Afterboot.git
   cd Win11Afterboot
   ```

2. **Set up virtual environment & install requirements:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Start the app:**
   ```powershell
   python main.py
   ```

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
