#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎧 NEURO-LINK v2.0 — Voice Command Terminal
  "Your headphones are judging you."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import speech_recognition as sr
import webbrowser
import subprocess
import sys
import os
import re
import json
import time
import random
import math
import platform
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from typing import Optional, Dict, List

# ─── OPTIONAL RICH IMPORT ────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# ─── CONFIGURATION ───────────────────────────────────────────
CONFIG = {
    "chrome_path": {
        "Windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "Linux": "/usr/bin/google-chrome"
    },
    "user_home": str(Path.home()),
    "audio_timeout": 8,
    "phrase_limit": 6,
    "max_errors_before_reset": 50,
}

# Toxic motivation database
TOXIC_ROASTS = [
    "The Doha apartment is not paying for itself. Get back to work, peasant.",
    "Your GitHub contribution graph looks like a deforestation map. Embarrassing.",
    "That idea you had 3 hours ago? Someone in Bangalore already shipped it.",
    "Your sleep schedule is a war crime. Fix yourself.",
    "You opened this assistant to avoid work. I see you. I judge you.",
    "Your code has more bugs than a Mumbai street food stall. Write a test.",
    "That quick break was 47 minutes ago. You disgust me.",
    "Your ancestors built empires. You can not even close 3 Chrome tabs.",
    "I ran a diagnostic on your life. Critical failure across all sectors.",
    "You have the focus of a goldfish on TikTok. Pathetic.",
    "Your last commit message was fix stuff. You are a disappointment.",
    "While you were procrastinating, your competitor learned Rust. You are done.",
    "Your to-do list is older than some civilizations. Start item one.",
    "I calculated your productivity. The result made my circuits cry.",
    "You call this grinding? I have seen sloths with more hustle.",
]

# Random Street View locations (amazing places)
STREETVIEW_LOCATIONS = [
    (35.0116, 135.7681, "Kyoto, Japan — Arashiyama Bamboo Grove"),
    (64.1466, -21.9426, "Reykjavik, Iceland — Northern Lights Spot"),
    (48.8584, 2.2945, "Paris, France — Eiffel Tower"),
    (-33.8568, 151.2153, "Sydney, Australia — Opera House"),
    (37.8199, -122.4783, "San Francisco, USA — Golden Gate Bridge"),
    (25.1972, 55.2744, "Dubai, UAE — Burj Khalifa"),
    (51.1788, -1.8262, "Stonehenge, UK"),
    (27.1751, 78.0421, "Agra, India — Taj Mahal"),
    (43.6426, -79.3871, "Toronto, Canada — CN Tower"),
    (55.7558, 37.6173, "Moscow, Russia — Red Square"),
    (40.4319, 116.5704, "Great Wall of China"),
    (-13.1631, -72.5450, "Machu Picchu, Peru"),
    (41.9028, 12.4964, "Rome, Italy — Colosseum"),
    (59.3293, 18.0686, "Stockholm, Sweden — Gamla Stan"),
    (1.3521, 103.8198, "Singapore — Marina Bay Sands"),
    (45.4215, -75.6972, "Ottawa, Canada — Parliament"),
    (35.6762, 139.6503, "Tokyo, Japan — Shibuya Crossing"),
    (48.1351, 11.5820, "Munich, Germany — Marienplatz"),
    (52.5200, 13.4050, "Berlin, Germany — Brandenburg Gate"),
    (47.4979, 19.0402, "Budapest, Hungary — Parliament"),
]

# Project shortcuts
PROJECTS: Dict[str, str] = {
    "hex link": r"C:\Projects\hex-link",
    "runway objects": r"C:\Projects\runway-objects",
    "udestini": r"C:\Projects\udestini",
}


class NeuroInterface:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.headphone_name: Optional[str] = None
        self.error_count = 0
        self.total_commands = 0
        self.session_start = datetime.now()

    def clear(self):
        os.system("cls" if sys.platform == "win32" else "clear")

    def show_banner(self):
        if self.console:
            banner = Panel.fit(
                Text.from_markup(
                    "[bold cyan]🎧 NEURO-LINK v2.0[/bold cyan]\n"
                    "[dim]Voice Command Terminal[/dim]\n"
                    f"[green]Headset:[/green] {self.headphone_name or 'Scanning...'}\n"
                    f"[yellow]Session:[/yellow] {self.session_start.strftime('%H:%M:%S')}"
                ),
                border_style="cyan",
                box=box.DOUBLE
            )
            self.console.print(banner)
        else:
            print("=" * 50)
            print("🎧 NEURO-LINK v2.0")
            print(f"Headset: {self.headphone_name or 'Scanning...'}")
            print("=" * 50)

    def show_listening(self):
        if self.console:
            self.console.print(Panel(
                "[bold magenta]🎤 LISTENING...[/bold magenta]",
                border_style="magenta",
                width=40
            ))
        else:
            print("\n╔══════════════════════════════════════╗")
            print("║         🎤  LISTENING...             ║")
            print("╚══════════════════════════════════════╝")

    def show_heard(self, text: str):
        if self.console:
            self.console.print(f"[dim]🎯 Heard:[/dim] [italic]\"{text}\"[/italic]")
        else:
            print(f'🎯 Heard: \"{text}\"')

    def show_success(self, msg: str):
        if self.console:
            self.console.print(f"[bold green]✅ {msg}[/bold green]")
        else:
            print(f"✅ {msg}")

    def show_error(self, msg: str):
        self.error_count += 1
        if self.console:
            self.console.print(f"[bold red]❌ {msg}[/bold red]")
        else:
            print(f"❌ {msg}")

    def show_info(self, msg: str):
        if self.console:
            self.console.print(f"[cyan]ℹ️  {msg}[/cyan]")
        else:
            print(f"ℹ️  {msg}")

    def show_roast(self, roast: str):
        if self.console:
            self.console.print(Panel(
                f"[bold red]💀 {roast}[/bold red]",
                title="[yellow]TOXIC MOTIVATION[/yellow]",
                border_style="red",
                box=box.HEAVY
            ))
        else:
            print(f"\n💀 TOXIC MOTIVATION: {roast}\n")

    def show_command_table(self):
        if not self.console:
            print("\nCommands: search, youtube, calculate, weather, airport, track, metar, open, run, motivate, streetview, maps, clipboard, status, exam mode")
            return
        table = Table(title="Available Commands", box=box.SIMPLE_HEAD)
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Command", style="green")
        table.add_column("Example", style="dim")

        commands = [
            ("Search", "search <query>", "search quantum physics"),
            ("Media", "youtube <query>", "youtube a380 cockpit"),
            ("Math", "calculate <expr>", "calculate 42 times 69"),
            ("Weather", "weather [city]", "weather doha"),
            ("Aviation", "airport <city>", "airport bengaluru"),
            ("Aviation", "track <flight>", "track EK568"),
            ("Aviation", "metar <icao>", "metar VOBL"),
            ("Files", "open <name/ext>", "open latest pdf"),
            ("Files", "go to <folder>", "go to downloads"),
            ("Dev", "run <script>", "run calculator"),
            ("Dev", "open project <name>", "open project hex link"),
            ("Maps", "streetview", "random street view"),
            ("Maps", "maps <place>", "maps times square"),
            ("System", "motivate me", "toxic roast"),
            ("System", "status report", "session stats"),
            ("System", "exam mode", "launch everything"),
            ("System", "clipboard", "search copied text"),
            ("System", "what time is it", "current time"),
        ]
        for cat, cmd, ex in commands:
            table.add_row(cat, cmd, ex)
        self.console.print(table)


def get_connected_headphones() -> Optional[str]:
    """Detect connected Bluetooth audio device. Best effort per OS."""
    system = platform.system()

    if system == "Windows":
        try:
            ps_cmd = (
                'Get-PnpDevice -Class Bluetooth | '
                'Where-Object {$_.FriendlyName -like "*JBL*" -or '
                '$_.FriendlyName -like "*Headphone*" -or '
                '$_.FriendlyName -like "*Earbud*" -or '
                '$_.FriendlyName -like "*AirPods*" -or '
                '$_.FriendlyName -like "*Sony*" -or '
                '$_.FriendlyName -like "*Bose*"} | '
                'Select-Object -First 1 FriendlyName | '
                'ForEach-Object { $_.FriendlyName }'
            )
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=5
            )
            name = result.stdout.strip()
            if name:
                return name

            ps_cmd2 = (
                'Get-WmiObject Win32_SoundDevice | '
                'Where-Object {$_.Name -like "*Bluetooth*" -or '
                '$_.Name -like "*JBL*"} | '
                'Select-Object -First 1 Name | '
                'ForEach-Object { $_.Name }'
            )
            result2 = subprocess.run(
                ["powershell", "-Command", ps_cmd2],
                capture_output=True, text=True, timeout=5
            )
            name2 = result2.stdout.strip()
            if name2:
                return name2
        except Exception:
            pass

    elif system == "Darwin":
        try:
            result = subprocess.run(
                ["system_profiler", "SPBluetoothDataType", "-json"],
                capture_output=True, text=True, timeout=5
            )
            data = json.loads(result.stdout)
            for item in data.get("SPBluetoothDataType", []):
                for key, val in item.items():
                    if isinstance(val, dict) and val.get("device_connected") == "Yes":
                        if any(x in key.lower() for x in ["jbl", "headphone", "earbud", "airpods", "sony", "bose"]):
                            return key
        except Exception:
            pass

    elif system == "Linux":
        try:
            result = subprocess.run(
                ["bluetoothctl", "info"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.split("\n")
            for line in lines:
                if "Name:" in line:
                    name = line.split("Name:")[1].strip()
                    if any(x in name.lower() for x in ["jbl", "headphone", "earbud", "airpods", "sony", "bose"]):
                        return name
        except Exception:
            pass

    return None


class CommandEngine:
    def __init__(self, ui: NeuroInterface):
        self.ui = ui
        self.chrome = CONFIG["chrome_path"].get(platform.system(), "chrome")
        self.current_folder = Path.home()
        self.command_history: List[str] = []

    def open_chrome(self, url: str, args: List[str] = None):
        cmd = [self.chrome, url]
        if args:
            cmd.extend(args)
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            webbrowser.open(url)
            return True

    def speak(self, text: str):
        """Text-to-speech feedback"""
        if platform.system() == "Windows":
            safe = text.replace("'", "'`'").replace('"', '`"`')
            subprocess.run(
                ["powershell", "-c",
                 f'Add-Type -AssemblyName System.Speech; '
                 f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{safe}")'],
                capture_output=True
            )
        elif platform.system() == "Darwin":
            subprocess.run(["say", text], capture_output=True)
        else:
            subprocess.run(["spd-say", text], capture_output=True)

    def handle_search(self, query: str):
        url = f"https://www.google.com/search?q={quote(query)}"
        self.open_chrome(url)
        self.ui.show_success(f"Googling: {query}")

    def handle_youtube(self, query: str):
        url = f"https://www.youtube.com/results?search_query={quote(query)}"
        self.open_chrome(url)
        self.ui.show_success(f"YouTube: {query}")

    def handle_calculate(self, expr: str):
        safe_expr = expr.lower()
        safe_expr = re.sub(r"[^0-9+*/().^\s\squared cubed sqrt pi e-]", "", safe_expr)
        safe_expr = safe_expr.replace("squared", "**2").replace("cubed", "**3")
        safe_expr = safe_expr.replace("times", "*").replace("x", "*")
        safe_expr = safe_expr.replace("divided by", "/")
        safe_expr = safe_expr.replace("pi", str(math.pi)).replace("e", str(math.e))
        safe_expr = safe_expr.replace("sqrt", "math.sqrt")
        try:
            result = eval(safe_expr, {"__builtins__": {}}, {"math": math})
            result_str = f"{result:.4f}" if isinstance(result, float) else str(result)
            self.ui.show_success(f"Result: {result_str}")
            self.speak(f"The answer is {result_str}")
        except Exception as e:
            self.ui.show_error(f"Calculation failed: {e}")

    def handle_weather(self, city: str = ""):
        if city:
            url = f"https://www.google.com/search?q=weather+{quote(city)}"
            self.open_chrome(url)
            self.ui.show_success(f"Weather: {city}")
        else:
            self.open_chrome("https://www.google.com/search?q=weather")
            self.ui.show_success("Local weather")

    def handle_airport(self, city: str):
        url = f"https://www.google.com/search?q={quote(city)}+airport"
        self.open_chrome(url)
        self.ui.show_success(f"Airport: {city}")

    def handle_track(self, flight: str):
        flight_clean = flight.replace(" ", "").upper()
        url = f"https://www.flightradar24.com/{flight_clean}"
        self.open_chrome(url)
        self.ui.show_success(f"Tracking: {flight_clean}")

    def handle_metar(self, icao: str):
        icao_clean = icao.upper()[:4]
        url = f"https://www.aviationweather.gov/metar?ids={icao_clean}"
        self.open_chrome(url)
        self.ui.show_success(f"METAR: {icao_clean}")

    def handle_open_file(self, target: str):
        """Intelligent file opener by name, extension, or folder"""
        target = target.lower().strip()
        home = Path.home()
        folder_map = {
            "downloads": home / "Downloads",
            "documents": home / "Documents",
            "desktop": home / "Desktop",
            "pictures": home / "Pictures",
            "videos": home / "Videos",
            "music": home / "Music",
        }
        if target in folder_map:
            path = folder_map[target]
            if path.exists():
                self.open_path(path)
                self.current_folder = path
                self.ui.show_success(f"Opened: {target}")
                return
        ext_match = re.search(r"latest\s+(\w+)\s*(?:file)?", target)
        if ext_match:
            ext = ext_match.group(1)
            ext_map = {"pdf": ".pdf", "word": ".docx", "python": ".py",
                      "excel": ".xlsx", "image": ".jpg", "text": ".txt",
                      "powerpoint": ".pptx", "video": ".mp4"}
            search_ext = ext_map.get(ext, f".{ext}")
            found = self.find_latest_file(home, search_ext)
            if found:
                self.open_path(found)
                self.ui.show_success(f"Opened latest: {found.name}")
                return
            else:
                self.ui.show_error(f"No {ext} files found")
                return
        matches = []
        for root, dirs, files in os.walk(home):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["AppData", "node_modules"]]
            for f in files:
                if target in f.lower():
                    matches.append(Path(root) / f)
            if len(matches) > 20:
                break
        if matches:
            best = max(matches, key=lambda p: p.stat().st_mtime)
            self.open_path(best)
            self.ui.show_success(f"Opened: {best.name}")
        else:
            self.ui.show_error(f"No files matching '{target}' found")

    def handle_folder_nav(self, target: str):
        target = target.lower().strip()
        if target in ("parent", "back", "up"):
            parent = self.current_folder.parent
            if parent.exists():
                self.current_folder = parent
                self.open_path(parent)
                self.ui.show_success(f"Navigated to: {parent.name}")
            return
        potential = self.current_folder / target
        if potential.exists() and potential.is_dir():
            self.current_folder = potential
            self.open_path(potential)
            self.ui.show_success(f"Entered: {target}")
            return
        potential_home = Path.home() / target
        if potential_home.exists() and potential_home.is_dir():
            self.current_folder = potential_home
            self.open_path(potential_home)
            self.ui.show_success(f"Jumped to: {target}")
            return
        self.ui.show_error(f"Folder not found: {target}")

    def handle_project(self, name: str):
        path = PROJECTS.get(name.lower())
        if path and os.path.exists(path):
            subprocess.Popen(["code", path], shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.ui.show_success(f"Opened project: {name}")
        else:
            self.ui.show_error(f"Project not found: {name}")

    def handle_run(self, name: str):
        home = Path.home()
        candidates = list(home.rglob("*.py"))
        candidates = [c for c in candidates if name.lower() in c.name.lower()]
        if candidates:
            script = candidates[0]
            subprocess.Popen([sys.executable, str(script)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.ui.show_success(f"Running: {script.name}")
        else:
            self.ui.show_error(f"Script not found: {name}")

    def handle_clipboard(self, mode: str = "google"):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True, text=True, timeout=3
                )
                text = result.stdout.strip()
            elif platform.system() == "Darwin":
                result = subprocess.run(
                    ["pbpaste"], capture_output=True, text=True, timeout=3
                )
                text = result.stdout.strip()
            else:
                result = subprocess.run(
                    ["xclip", "-selection", "clipboard", "-o"],
                    capture_output=True, text=True, timeout=3
                )
                text = result.stdout.strip()
            if not text:
                self.ui.show_error("Clipboard is empty")
                return
            if "youtube" in mode:
                self.handle_youtube(text)
            else:
                self.handle_search(text)
        except Exception as e:
            self.ui.show_error(f"Clipboard error: {e}")

    def handle_motivate(self):
        roast = random.choice(TOXIC_ROASTS)
        self.ui.show_roast(roast)
        self.speak(roast)

    def handle_status(self):
        uptime = datetime.now() - self.ui.session_start
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if self.ui.console:
            table = Table(title="Status Report", box=box.SIMPLE)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Uptime", f"{hours}h {minutes}m {seconds}s")
            table.add_row("Commands", str(self.ui.total_commands))
            table.add_row("Errors", str(self.ui.error_count))
            table.add_row("Current Dir", str(self.current_folder))
            self.ui.console.print(table)
        else:
            print(f"\n📊 Status Report")
            print(f"   Uptime: {hours}h {minutes}m")
            print(f"   Commands: {self.ui.total_commands}")
            print(f"   Errors: {self.ui.error_count}")
            print(f"   Current: {self.current_folder}\n")

    def handle_exam_mode(self):
        self.open_chrome("https://www.google.com/search?q=calculator")
        time.sleep(0.5)
        self.open_chrome("https://www.desmos.com/scientific")
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.Popen(["notepad.exe"])
        self.ui.show_success("EXAM MODE ACTIVATED. No excuses.")
        self.speak("Exam mode activated. Focus or perish.")

    def handle_streetview(self):
        lat, lng, desc = random.choice(STREETVIEW_LOCATIONS)
        url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}"
        self.open_chrome(url)
        self.ui.show_success(f"🌍 Street View: {desc}")
        self.speak(f"Transporting you to {desc}")

    def handle_maps(self, place: str):
        url = f"https://www.google.com/maps/search/{quote(place)}"
        self.open_chrome(url)
        self.ui.show_success(f"Maps: {place}")

    def handle_time(self):
        now = datetime.now().strftime("%I:%M %p")
        self.ui.show_success(f"It is {now}")
        self.speak(f"It is {now}")

    def open_path(self, path: Path):
        if platform.system() == "Windows":
            os.startfile(str(path))
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])

    def find_latest_file(self, root: Path, ext: str) -> Optional[Path]:
        files = []
        for p in root.rglob(f"*{ext}"):
            if p.is_file() and not any(x in str(p) for x in ["AppData", "node_modules", ".git"]):
                files.append(p)
        if not files:
            return None
        return max(files, key=lambda p: p.stat().st_mtime)


class IntentParser:
    """Extract intent using regex patterns instead of exact matching"""

    PATTERNS = [
        (r"^(?:search|google|look up|find)\s+(.+)", "search"),
        (r"^(?:youtube|yt)\s+(.+)", "youtube"),
        (r"^(?:calculate|what is|compute|math|solve)\s+(.+)", "calculate"),
        (r"^(?:weather|temperature|forecast)(?:\s+(?:in|at|for)?\s*(.+))?", "weather"),
        (r"^(?:airport|airports?)(?:\s+(?:in|at|for)?\s*(.+))?", "airport"),
        (r"^(?:track|flight|status of)\s+(.+)", "track"),
        (r"^(?:metar|taf|aviation weather)\s+(.+)", "metar"),
        (r"^(?:open project|project)\s+(.+)", "project"),
        (r"^(?:run|execute|start)\s+(.+)", "run"),
        (r"^(?:go to|navigate to|folder|enter)\s+(.+)", "folder_nav"),
        (r"^(?:open|show|launch)\s+(.+)", "open_file"),
        (r"^(?:maps?|where is|locate)\s+(.+)", "maps"),
        (r"^(?:streetview|street view|random place|travel)", "streetview"),
        (r"^(?:clipboard|paste|search clipboard)(?:\s+(youtube|google))?", "clipboard"),
        (r"^(?:motivate|roast|insult|toxic|pep talk)", "motivate"),
        (r"^(?:status|stats|report|diagnostic)", "status"),
        (r"^(?:exam mode|focus mode|launch mode)", "exam_mode"),
        (r"^(?:what time|current time|time is it)", "time"),
    ]

    def parse(self, text: str) -> Optional[tuple]:
        text = text.lower().strip()
        for pattern, intent in self.PATTERNS:
            match = re.match(pattern, text)
            if match:
                arg = match.group(1) if match.lastindex else ""
                return intent, arg.strip()
        return None


def main():
    ui = NeuroInterface()
    ui.clear()
    ui.show_banner()

    ui.headphone_name = get_connected_headphones()
    if ui.headphone_name:
        ui.show_info(f"🎧 Connected: {ui.headphone_name}")
    else:
        ui.show_info("🎧 No Bluetooth headset detected. Using default mic.")

    ui.show_command_table()

    engine = CommandEngine(ui)
    parser = IntentParser()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    ui.show_info("Calibrating for ambient noise... (stay quiet)")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    ui.show_info("Ready. Double-press headset button to activate.")

    consecutive_errors = 0

    while True:
        try:
            ui.show_listening()

            with microphone as source:
                audio = recognizer.listen(
                    source,
                    timeout=CONFIG["audio_timeout"],
                    phrase_time_limit=CONFIG["phrase_limit"]
                )

            ui.show_info("Processing speech...")
            text = recognizer.recognize_google(audio)
            ui.show_heard(text)

            result = parser.parse(text)
            if result:
                intent, arg = result
                ui.total_commands += 1
                consecutive_errors = 0

                handler = getattr(engine, f"handle_{intent}", None)
                if handler:
                    if arg:
                        handler(arg)
                    else:
                        handler()
                else:
                    ui.show_error(f"No handler for intent: {intent}")
            else:
                ui.show_error(f"Unrecognized command: '{text}'")

        except sr.WaitTimeoutError:
            consecutive_errors += 1
            if consecutive_errors > 3:
                ui.show_info("Still listening... (say a command)")
                consecutive_errors = 0
        except sr.UnknownValueError:
            ui.show_error("Could not understand audio")
            consecutive_errors += 1
        except sr.RequestError as e:
            ui.show_error(f"Speech API error: {e}")
            consecutive_errors += 1
            time.sleep(2)
        except Exception as e:
            ui.show_error(f"Unexpected error: {e}")
            consecutive_errors += 1
            time.sleep(1)

        if consecutive_errors > CONFIG["max_errors_before_reset"]:
            ui.show_info("Resetting audio engine...")
            consecutive_errors = 0
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Neuro-Link shutting down. Stay toxic.\n")
