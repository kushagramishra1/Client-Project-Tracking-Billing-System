# 🐍 Python Installation Guide

## Option 1: Install Python (Recommended)

### Download from Official Website
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.11" (or latest version)
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Complete the installation

### Install from Microsoft Store
1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click Install

## Option 2: Use Python Launcher (if already installed)
```bash
py -m pip install -r requirements.txt
py start.py
```

## Option 3: Check if Python is installed but not in PATH
```bash
# Try these commands:
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt
C:\Program Files\Python311\python.exe -m pip install -r requirements.txt
C:\Python311\python.exe -m pip install -r requirements.txt
```

## After Installing Python

1. **Open a new Command Prompt/PowerShell**
2. **Verify Python is installed:**
   ```bash
   python --version
   ```
3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python start.py
   ```

## Troubleshooting

### If "pip is not recognized":
```bash
python -m pip install -r requirements.txt
```

### If Python is not found:
- Make sure you checked "Add Python to PATH" during installation
- Restart your command prompt after installation
- Try using `py` instead of `python`

### If you get permission errors:
```bash
pip install --user -r requirements.txt
```

## Quick Test Commands

After installing Python, test with:
```bash
python --version
pip --version
```

If both work, you're ready to run the project!
