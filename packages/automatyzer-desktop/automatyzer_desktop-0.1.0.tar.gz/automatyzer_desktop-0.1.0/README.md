# desktop-bot

# Desktop Automation Bot

A powerful desktop automation tool that can connect via Remote Desktop Protocol (RDP) and perform actions based on text commands across different operating systems.

## Features

- Connect to remote computers via RDP
- Automate mouse actions (clicking, scrolling)
- Simulate keyboard inputs
- Screen element detection through image recognition
- Optical Character Recognition (OCR)
- Email retrieval and code extraction
- Cross-platform shell command execution

## Prerequisites

### System Dependencies
- Python 3.8+
- Tesseract OCR
- Additional system libraries depending on your OS

### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/automatyzer/desktop-bot.git
cd desktop-bot
```

2. Create and activate a virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install system dependencies

#### Windows
```powershell
# Install Tesseract OCR from official website
# Download and add to PATH: https://github.com/UB-Mannheim/tesseract/wiki
pip install -r requirements.txt
```

#### Ubuntu/Debian
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    tesseract-ocr \
    libgl1-mesa-glx \
    xvfb \
    xserver-xorg-video-dummy

# Install Python dependencies
pip install -r requirements.txt
```

#### macOS
```bash
# Install Tesseract via Homebrew
brew install tesseract

# Install dependencies
pip install -r requirements.txt
```

4. Verify Installation
```bash
# Check installed modules
pip list

# Run the application
python app.py
```

### Troubleshooting Common Issues

#### Missing Module Errors
If you encounter `ModuleNotFoundError`, ensure:
- Virtual environment is activated
- All requirements are installed with `pip install -r requirements.txt`
- You're using the correct Python interpreter from the virtual environment

#### Tesseract OCR Configuration
- Ensure Tesseract is installed and accessible
- Update `tesseract_path` in `config.ini` if needed

### Usage Examples

```python
# Create bot instance
bot = AutomationBot()

# Connect via RDP
bot.connect_rdp(host="example.com", username="user", password="pass")

# Execute tasks
bot.execute_task("open application firefox")
bot.execute_task("login to linkedin portal")
```

### Command Line Usage

```bash
# Execute single task
python automatyzer_desktop.py --task "open application firefox"

# Run script with multiple tasks
python automatyzer_desktop.py --script tasks.txt
```

### Configuration

Customize `config.ini` for:
- RDP Connection settings
- Email retrieval
- Delay between actions
- Tesseract OCR path

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

## Disclaimer

This tool is for educational and authorized testing purposes only. Always obtain proper authorization before accessing remote systems.


## Quick Start

### Local Development
1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
