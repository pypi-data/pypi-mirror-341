# 🤖 DroidRun

DroidRun is a powerful framework for controlling Android devices through LLM agents. It allows you to automate Android device interactions using natural language commands.

## ✨ Features

- Control Android devices with natural language commands
- Supports multiple LLM providers (OpenAI, Anthropic, Gemini)
- Easy to use CLI
- Extendable Python API for custom automations
- Screenshot analysis for visual understanding of the device

## 📦 Installation

### 🚀 Option 1: Install from PyPI (Recommended)

```bash
pip install droidrun
```

### 🔧 Option 2: Install from Source

```bash
git clone https://github.com/yourusername/droidrun.git
cd droidrun
pip install -e .
```

## 📋 Prerequisites

1. An Android device connected via USB or ADB over TCP/IP
2. ADB (Android Debug Bridge) installed and configured
3. DroidRun Portal app installed on your Android device
4. API key for at least one of the supported LLM providers:
   - OpenAI
   - Anthropic
   - Google Gemini

### 🔧 Setting up ADB

ADB (Android Debug Bridge) is required for DroidRun to communicate with your Android device:

1. **Install ADB**:
   - **Windows**: Download [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) and extract the ZIP file
   - **macOS**: `brew install android-platform-tools`
   - **Linux**: `sudo apt install adb` (Ubuntu/Debian) or `sudo pacman -S android-tools` (Arch)

2. **Add ADB to your PATH**:
   - **Windows**: Add the path to the extracted platform-tools folder to your system's PATH environment variable
   - **macOS/Linux**: Add the following to your ~/.bashrc or ~/.zshrc:
     ```bash
     export PATH=$PATH:/path/to/platform-tools
     ```

3. **Verify ADB installation**:
   ```bash
   adb version
   ```

4. **Enable USB debugging on your Android device**:
   - Go to **Settings → About phone**
   - Tap **Build number** 7 times to enable Developer options
   - Go to **Settings → System → Developer options** (location may vary by device)
   - Enable **USB debugging**

## 🛠️ Setup

### 📱 1. Install DroidRun Portal App

DroidRun requires the DroidRun Portal app to be installed on your Android device:

1. Download the DroidRun Portal APK from the [DroidRun Portal repository](https://github.com/droidrun/droidrun-portal)
2. Use DroidRun to install the portal app:
   ```bash
   droidrun setup --path=/path/to/droidrun-portal.apk
   ```

Alternatively, you can use ADB to install it manually:
```bash
adb install -r /path/to/droidrun-portal.apk
```

### 🔑 2. Set up API keys

Create a `.env` file in your working directory or set environment variables:

```bash
# Choose at least one of these based on your preferred provider
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export GEMINI_API_KEY="your_gemini_api_key_here"
```

To load the environment variables from the `.env` file:

```bash
source .env
```

### 📱 3. Connect to an Android device

Connect your device via USB or set up wireless ADB:

```bash
# List connected devices
droidrun devices

# Connect to a device over Wi-Fi
droidrun connect 192.168.1.100
```

### 🔄 4. Verify the setup

Verify that everything is set up correctly:

```bash
# Should list your connected device and show portal status
droidrun status
```

## 💻 Using the CLI

DroidRun's CLI is designed to be simple and intuitive. You can use it in two ways:

### 🚀 Basic Usage

```bash
# Format: droidrun "task description" [options]
droidrun "Open the settings app"
```

### 🔌 With Provider Options

```bash
# Using OpenAI
droidrun "Open the calculator app" --provider openai --model gpt-4o-mini

# Using Anthropic
droidrun "Check the battery level" --provider anthropic --model claude-3-sonnet-20240229

# Using Gemini
droidrun "Install and open Instagram" --provider gemini --model gemini-2.0-flash
```

### ⚙️ Additional Options

```bash
# Specify a particular device
droidrun "Open Chrome and search for weather" --device abc123

# Set maximum number of steps
droidrun "Open settings and enable dark mode" --steps 20
```

## 📝 Creating a Minimal Test Script

If you want to use DroidRun in your Python code rather than via the CLI, you can create a minimal test script:

```python
#!/usr/bin/env python3
import asyncio
import os
from droidrun.agent.react_agent import ReActAgent
from droidrun.agent.llm_reasoning import LLMReasoner
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def main():
    # Create an LLM instance (choose your preferred provider)
    llm = LLMReasoner(
        llm_provider="gemini",  # Can be "openai", "anthropic", or "gemini"
        model_name="gemini-2.0-flash",  # Choose appropriate model for your provider
        api_key=os.environ.get("GEMINI_API_KEY"),  # Get API key from environment
        temperature=0.2
    )
    
    # Create and run the agent
    agent = ReActAgent(
        task="Open the Settings app and check the Android version",
        llm=llm
    )
    
    steps = await agent.run()
    print(f"Execution completed with {len(steps)} steps")

if __name__ == "__main__":
    asyncio.run(main())
```

Save this as `test_droidrun.py`, ensure your `.env` file has the appropriate API key, and run:

```bash
python test_droidrun.py
```

## ❓ Troubleshooting

### 🔑 API Key Issues

If you encounter errors about missing API keys, ensure:
1. You've set the correct environment variable for your chosen provider
2. The API key is valid and has appropriate permissions
3. You've correctly sourced your `.env` file or exported the variables manually

### 📱 Device Connection Issues

If you have trouble connecting to your device:
1. Ensure USB debugging is enabled on your Android device
2. Check that your device is recognized by ADB: `adb devices`
3. For wireless connections, make sure your device and computer are on the same network

### 🤖 LLM Provider Selection

If DroidRun is using the wrong LLM provider:
1. Explicitly specify the provider with `--provider` (in CLI) or `llm_provider=` (in code)
2. When using Gemini, ensure you have set `GEMINI_API_KEY` and specified `--provider gemini`

## 💡 Example Use Cases

- Automated UI testing of Android applications
- Creating guided workflows for non-technical users
- Automating repetitive tasks on Android devices
- Remote assistance for less technical users
- Exploring Android UI with natural language commands

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 