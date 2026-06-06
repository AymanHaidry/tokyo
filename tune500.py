#!/usr/bin/env python3
"""
JBL Tune 500BT Voice Command System
Handles voice commands via headset button double-press
"""

import speech_recognition as sr
import webbrowser
import subprocess
import sys
import os
import json
import time
import threading
from datetime import datetime
from pathlib import Path

# ─── CONFIGURATION ─────────────────────────────────────────────
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Windows
# CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # macOS
# CHROME_PATH = "/usr/bin/google-chrome"  # Linux

KOSMOSIC_URL = "https://kosmosic.vercel.app/app"

# Command registry
COMMANDS = {
    # Study Commands
    "open kosmosic": {"url": "https://kosmosic.vercel.app"},
    "open study": {"url": KOSMOSIC_URL},
    "start grind": {"url": KOSMOSIC_URL, "fullscreen": True},
    
    # Coding Commands
    "open vs code": {"app": "code"},
    "open github": {"url": "https://github.com"},
    "run python": {"script": "python", "args": ["-i"]},
    
    # PC Commands
    "open calculator": {"app": "calc"},
    "open chrome": {"app": CHROME_PATH},
    "what time is it": {"action": "time"},
    
    # Aviation Commands
    "show flightradar": {"url": "https://www.flightradar24.com"},
    "show aircraft news": {"url": "https://www.aviationtoday.com"},
    "airport weather": {"url": "https://www.aviationweather.gov"},
}

# ─── CORE FUNCTIONS ──────────────────────────────────────────────

def open_chrome(url, fullscreen=False):
    """Open URL in Chrome with optional fullscreen"""
    args = [CHROME_PATH, url]
    if fullscreen:
        args.append("--start-fullscreen")
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🌐 Opened Chrome: {url}")

def open_app(command):
    """Open system applications"""
    try:
        if sys.platform == "win32":
            subprocess.Popen(f"start {command}", shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", command])
        else:
            subprocess.Popen([command])
        print(f"📱 Opened app: {command}")
    except Exception as e:
        print(f"❌ Failed to open {command}: {e}")

def speak_time():
    """Return current time verbally"""
    now = datetime.now().strftime("%I:%M %p")
    print(f"🕐 It's {now}")
    # Optional: text-to-speech feedback
    if sys.platform == "win32":
        os.system(f'powershell -c "Add-Type -AssemblyName System.Speech; '
                  f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'It is {now}\')"')

def execute_command(text):
    """Parse and execute matched command"""
    text = text.lower().strip()
    print(f"🎯 Heard: '{text}'")
    
    # Fuzzy match
    for cmd, action in COMMANDS.items():
        if cmd in text or any(word in text for word in cmd.split()):
            print(f"✅ Matched: {cmd}")
            
            if "url" in action:
                open_chrome(action["url"], action.get("fullscreen", False))
            elif "app" in action:
                open_app(action["app"])
            elif "action" in action and action["action"] == "time":
                speak_time()
            elif "script" in action:
                subprocess.Popen(action["script"])
            
            return True
    
    print("❌ No command matched")
    return False

def listen_loop():
    """Main voice recognition loop"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Calibrate for ambient noise
    print("🔧 Calibrating microphone...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    
    print("\n" + "="*50)
    print("🎧 JBL Voice Command System Ready")
    print("Double-press headset button to activate")
    print("Say 'start grind' to open study dashboard")
    print("="*50 + "\n")
    
    while True:
        try:
            with microphone as source:
                print("🎤 Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("🧠 Processing...")
            text = recognizer.recognize_google(audio)
            execute_command(text)
            
        except sr.WaitTimeoutError:
            pass  # No speech detected
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except sr.RequestError as e:
            print(f"🌐 API error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            break

# ─── ACTIVATION TRIGGER ────────────────────────────────────────

def trigger_popup():
    """Simulate the 'Listening...' popup (Windows)"""
    # You can replace this with a custom Tkinter overlay
    print("\n" + "╔" + "═"*38 + "╗")
    print("║" + " "*12 + "🎤 Listening..." + " "*11 + "║")
    print("╚" + "═"*38 + "╝\n")

# ─── ENTRY POINT ───────────────────────────────────────────────

if __name__ == "__main__":
    trigger_popup()
    listen_loop()