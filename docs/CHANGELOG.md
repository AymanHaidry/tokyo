# Changelog

All notable changes to Neuro-Link will be documented in this file.

---

## [0.4.0] - 2026-06-06

### 🧠 Intelligence Module

* Added dedicated `neuro_link_intel.py` module.
* Separated NLP and knowledge processing from the main application.
* Improved maintainability and modularity.

---

### 🗣 Natural Language Understanding

Introduced a Natural Language Processor (NLP) layer capable of understanding conversational speech and common mistakes.

#### Examples

| User Input                 | Interpreted As              |
| -------------------------- | --------------------------- |
| what's the weather in doha | what is the weather in doha |
| whats the time             | what is the time            |
| tell me about orion        | knowledge lookup            |
| i'm tired                  | memory event                |
| how to cook rice           | Google search               |
| exambored                  | exam mode                   |
| hell / hellp / halp        | help                        |

Features:

* Contraction expansion
* Homophone correction
* Intent normalization
* Query cleanup before processing

---

### 📁 File Explorer Integration

Folders now open directly in Windows Explorer.

#### Example

```text
Voice: open downloads
```

Result:

```text
explorer.exe C:\Users\<user>\Downloads
```

Additional functionality:

* Displays numbered file list in terminal
* Opens actual Explorer window
* Supports file browsing workflows

---

### 🍎 Apple-Style Boot Experience

Replaced legacy startup screen with a cleaner boot sequence.

#### New Startup

```text
●
Loading Neuro-Link...
Initializing voice engine...
Connecting to intelligence module...
✓ Ready
```

Focus:

* Minimal interface
* Faster startup feedback
* Cleaner user experience

---

### 🔄 Reboot System Improvements

Fixed restart reliability.

Previous implementation:

```python
os.execl(...)
```

New implementation:

```python
subprocess.Popen(...)
sys.exit(0)
```

Benefits:

* Reliable relaunching
* Separate console support
* Reduced startup failures

---

### 🆘 Help Recognition Improvements

Expanded homophone recognition for help commands.

Supported variations:

```text
help
hell
hellp
halp
helf
elpe
```

All variations now correctly trigger the Help system.

---

### 📚 Exam Mode Recognition

Improved recognition of spoken exam-related commands.

Supported variations:

```text
exam mode
exambored
exambord
exum mode
eggsam mode
```

All variations now resolve to:

```text
exam mode
```

---

### 🌙 Sleep System Changes

Removed automatic sleep functionality.

Removed:

* wake_misses
* sleep_after_misses

Behavior:

* Neuro-Link remains active indefinitely
* Sleep only occurs through explicit commands

---

### 🔋 Manual Sleep & Wake Controls

#### Sleep Commands

```text
sleep
go to sleep
shut down
```

#### Wake Commands

```text
Tokyo
wake
wake up
start
online
```

#### Headset Wake

```text
[text] > wake
```

Simulates JBL headset activation workflow.

---

### 🌌 Built-In Knowledge Base

Added bundled intelligence datasets.

#### Constellations

Topics include:

* Orion
* Ursa Major
* Cassiopeia
* Scorpius
* Cygnus
* Leo
* Andromeda
* Crux

#### Moon Phases

Topics include:

* New Moon
* Waxing Crescent
* First Quarter
* Waxing Gibbous
* Full Moon
* Waning Gibbous
* Last Quarter
* Waning Crescent

#### Aviation Facts

Topics include:

* V1
* V2
* Mach Number
* ICAO
* Squawk Codes
* Altitude
* Wake Turbulence
* ILS
* METAR
* TAF

#### Space Facts

Topics include:

* International Space Station (ISS)
* Mars
* Black Holes
* Light Years
* Big Bang
* Nebulae
* Supernovae
* Dark Matter

---

### 🌐 External Knowledge Sources

Added Wikimedia integration.

Sources:

* Wikimedia Dumps
* Wikipedia REST API

Capabilities:

* Dynamic fact retrieval
* Knowledge expansion beyond bundled datasets
* Improved response coverage

---

### ⚙ Internal Improvements

* Cleaner architecture
* Better separation of concerns
* Reduced complexity in main application file
* Improved maintainability for future releases

---

## Previous Releases

### [0.3.x]

* Initial voice command framework
* URL launcher system
* Project launcher support
* Aviation utilities
* Calculator engine
* File navigation features
* JBL headset workflow foundation
for anything not in local knowledge.
