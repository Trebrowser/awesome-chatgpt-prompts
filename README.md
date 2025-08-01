# 🖥️ Deskhog - Zoom Disconnect Tool

A simple and effective desktop application that provides a **center button** to quickly disconnect from active Zoom calls. Perfect for situations where you need an emergency disconnect or quick exit from meetings.

## 🎯 Features

- **🔴 Center Button Interface**: Large, prominent red button for instant Zoom call disconnection
- **🔍 Real-time Monitoring**: Continuously monitors for active Zoom processes
- **⚡ Multiple Disconnect Methods**: 
  - Graceful disconnection using system hotkeys (Alt+Q on Linux, AppleScript on macOS)
  - Process termination as fallback
- **📊 Status Indicators**: Visual feedback showing Zoom status and last actions
- **🖥️ Cross-platform**: Works on Linux, macOS, and Windows
- **🎨 Modern GUI**: Clean, intuitive interface built with tkinter

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
```bash
chmod +x launch_deskhog.sh
./launch_deskhog.sh
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip3 install psutil

# Run the app
python3 deskhog_app.py
```

## 📋 Requirements

- **Python 3.6+** with tkinter support
- **psutil** library for process monitoring
- **Optional**: `xdotool` on Linux for enhanced functionality

### Installing Requirements

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk xdotool
pip3 install psutil
```

#### CentOS/RHEL:
```bash
sudo yum install python3 python3-pip tkinter xdotool
pip3 install psutil
```

#### Fedora:
```bash
sudo dnf install python3 python3-pip python3-tkinter xdotool
pip3 install psutil
```

#### Arch Linux:
```bash
sudo pacman -S python python-pip tk xdotool
pip3 install psutil
```

#### macOS:
```bash
# Install Python 3 if not available
brew install python3
pip3 install psutil
```

#### Windows:
```bash
# Python 3 from python.org includes tkinter
pip install psutil
```

## 🖱️ How to Use

1. **Launch the Application**:
   - Run `./launch_deskhog.sh` or `python3 deskhog_app.py`

2. **Monitor Zoom Status**:
   - The app continuously scans for active Zoom processes
   - Status indicator shows: 🔍 Scanning, 🟢 Active, or ❌ No Zoom

3. **Disconnect from Zoom**:
   - Click the large red **"DISCONNECT ZOOM CALL"** button
   - The app will attempt graceful disconnection first
   - If that fails, it will terminate Zoom processes

4. **Visual Feedback**:
   - Status updates show the current state
   - Information panel displays last actions with timestamps
   - Button color changes based on Zoom status

## 🎮 Interface Guide

```
┌─────────────────────────────────┐
│        🖥️ Deskhog               │
├─────────────────────────────────┤
│ ┌─ Zoom Status ───────────────┐ │
│ │ 🟢 Zoom Active - Ready      │ │
│ │ ████████████████████████     │ │
│ └─────────────────────────────┘ │
│                                 │
│        ┌─────────────────┐      │
│        │       📞        │      │
│        │   DISCONNECT    │      │
│        │   ZOOM CALL     │      │
│        └─────────────────┘      │
│                                 │
│ ┌─ Information ───────────────┐ │
│ │ Disconnected at 14:32:15    │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

## 🔧 Desktop Integration

### Linux Desktop Entry
Copy `deskhog.desktop` to `~/.local/share/applications/` to add Deskhog to your applications menu:

```bash
cp deskhog.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/deskhog.desktop
```

### Create Desktop Shortcut
```bash
cp deskhog.desktop ~/Desktop/
chmod +x ~/Desktop/deskhog.desktop
```

## ⚙️ How It Works

1. **Process Detection**: Uses `psutil` to scan for Zoom processes (`zoom`, `Zoom.exe`, `ZoomLauncher`, etc.)

2. **Graceful Disconnection**:
   - **Linux**: Sends `Alt+Q` using `xdotool`
   - **macOS**: Uses AppleScript to quit Zoom
   - **Windows**: Falls back to process termination

3. **Process Termination**: If graceful methods fail, terminates Zoom processes directly

4. **Real-time Monitoring**: Background thread checks Zoom status every 2 seconds

## 🛠️ Troubleshooting

### Common Issues

**Issue**: "No Zoom process found"
- **Solution**: Make sure Zoom is actually running before clicking disconnect

**Issue**: "Failed to disconnect from Zoom"
- **Solution**: Try running with elevated privileges or check if Zoom is frozen

**Issue**: "tkinter not found"
- **Solution**: Install Python tkinter package:
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - CentOS/RHEL: `sudo yum install tkinter`

**Issue**: xdotool not working on Linux
- **Solution**: Install xdotool: `sudo apt-get install xdotool`

### Debug Mode
Run with Python's verbose mode for debugging:
```bash
python3 -v deskhog_app.py
```

## 🔒 Security Notes

- The app only monitors and terminates Zoom processes
- No network connections or data collection
- All operations are performed locally
- Source code is fully open for inspection

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve Deskhog!

### Development Setup
```bash
git clone <repository>
cd deskhog
pip3 install -r requirements.txt
python3 deskhog_app.py
```

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Credits

Created as a simple, effective tool for managing Zoom calls with a prominent disconnect button interface.

---

**⚠️ Disclaimer**: This tool is designed for legitimate use cases where you need to quickly disconnect from Zoom calls. Use responsibly and in accordance with your organization's policies.