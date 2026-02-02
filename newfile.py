import json
import os
import time
import shutil
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
FILENAME = "mini_brain.json"
BACKUP_FILENAME = "mini_brain_backup.json"
INPUT_FOLDER = "mini_files"
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "processed")

# --- THE "PERFECT BRAIN" BLUEPRINT ---
# This data is used to create the brain file if it doesn't exist yet.
DEFAULT_BRAIN_STRUCTURE = {
    "master_info": {
        "name": "Achmed Davids",
        "access_level": "Soul Master",
        "location": "Mitchell's Plain, CP"
    },
    "level": 1,
    "intelligence_points": 50,
    "long_term_memory": {
        "CORE_DIRECTIVE": [
            {
                "data": "I am Mini, the External Brain for Achmed Davids. My goal is to serve as a digital extension of his memory.",
                "timestamp": "2026-01-26"
            }
        ]
    }
}

class MiniAI:
    def __init__(self):
        self.name = "Mini"
        self.short_term_memory = []
        
        # 1. Setup Folders
        self.setup_folders()
        
        # 2. Load or Create Brain
        self.attributes = self.load_brain()
        
        # 3. Greet
        self.greet_master()

    def setup_folders(self):
        """Ensures input folders exist"""
        if not os.path.exists(INPUT_FOLDER):
            os.makedirs(INPUT_FOLDER)
        if not os.path.exists(PROCESSED_FOLDER):
            os.makedirs(PROCESSED_FOLDER)

    def load_brain(self):
        """Loads memory file. If missing, it builds a new one from the Blueprint above."""
        if os.path.exists(FILENAME):
            try:
                with open(FILENAME, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Main brain file corrupted. Checking backup...")
                if os.path.exists(BACKUP_FILENAME):
                    shutil.copy(BACKUP_FILENAME, FILENAME)
                    with open(FILENAME, 'r') as f:
                        print("✅ Restored from Backup.")
                        return json.load(f)
                else:
                    return self.create_new_brain()
        else:
            # File doesn't exist yet -> Create it automatically
            return self.create_new_brain()

    def create_new_brain(self):
        """Creates the brain file using the Achmed Davids Blueprint"""
        print(f"✨ First time setup! Creating brain for {DEFAULT_BRAIN_STRUCTURE['master_info']['name']}...")
        with open(FILENAME, 'w') as f:
            json.dump(DEFAULT_BRAIN_STRUCTURE, f, indent=4)
        return DEFAULT_BRAIN_STRUCTURE

    def greet_master(self):
        lvl = self.attributes.get('level', 1)
        xp = self.attributes.get('intelligence_points', 0)
        user = self.attributes['master_info']['name']
        
        print(f"\n🔮 SYSTEM ONLINE: {self.name}")
        print(f"   --------------------------------")
        print(f"   👤 User: {user}")
        print(f"   🧠 Lvl:  {lvl} | XP: {xp}")
        print(f"   📚 Memories: {len(self.attributes.get('long_term_memory', {}))}")
        print(f"   --------------------------------")

    def direct_input(self):
        """Type directly into console"""
        print("\n📝 DIRECT INPUT MODE")
        category = input("   Topic: ").strip()
        content = input("   Data:  ").strip()
        
        if category and content:
            self.learn(category, content)
            print(f"   -> Remembered.")
        else:
            print("   ⚠️ Empty input.")

    def read_files_and_learn(self):
        """Reads .txt files from folder"""
        print(f"\n👀 Scanning '{INPUT_FOLDER}'...")
        files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.txt')]
        
        if not files:
            print("   ⚠️ No .txt files found.")
            return

        count = 0
        for file_name in files:
            cat = file_name.replace(".txt", "")
            src = os.path.join(INPUT_FOLDER, file_name)
            dst = os.path.join(PROCESSED_FOLDER, file_name)
            
            try:
                with open(src, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.learn(cat, content)
                        count += 1
                shutil.move(src, dst)
            except Exception as e:
                print(f"   ❌ Error: {e}")

        if count > 0:
            print(f"   ✅ Learned {count} files. Press [S] to save.")

    def learn(self, category, knowledge):
        entry = {
            "category": category, 
            "data": knowledge,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.short_term_memory.append(entry)

    def recall_memory(self):
        print("\n🔎 RECALL")
        query = input("   Search: ").lower().strip()
        found = False
        
        memories = self.attributes.get("long_term_memory", {})
        
        for cat, data_list in memories.items():
            if query in cat.lower():
                for item in data_list:
                    print(f"   📂 [{cat}]: {item['data'][:100]}...")
                    found = True
            else:
                for item in data_list:
                    if query in item['data'].lower():
                        print(f"   📄 [{cat}]: ...{item['data']}...")
                        found = True
        if not found:
            print("   ❌ Nothing found.")

    def sleep_and_save(self):
        print(f"\n💤 Saving...")
        time.sleep(0.5)

        # 1. Update Memory
        if "long_term_memory" not in self.attributes:
            self.attributes["long_term_memory"] = {}

        new_items = len(self.short_term_memory)
        for mem in self.short_term_memory:
            cat = mem["category"]
            if cat not in self.attributes["long_term_memory"]:
                self.attributes["long_term_memory"][cat] = []
            
            # Avoid duplicates
            existing = [x['data'] for x in self.attributes["long_term_memory"][cat]]
            if mem['data'] not in existing:
                self.attributes["long_term_memory"][cat].append(mem)

        # 2. XP & Level
        if new_items > 0:
            self.attributes["intelligence_points"] += (new_items * 50)
            cur_xp = self.attributes["intelligence_points"]
            new_lvl = 1 + (cur_xp // 200)
            if new_lvl > self.attributes["level"]:
                print(f"   🌟 LEVEL UP! {new_lvl}")
                self.attributes["level"] = new_lvl

        # 3. Clear RAM
        self.short_term_memory = []

        # 4. Backup & Save
        try:
            if os.path.exists(FILENAME):
                shutil.copy(FILENAME, BACKUP_FILENAME)
            
            with open(FILENAME, 'w') as f:
                json.dump(self.attributes, f, indent=4)
            print("   💾 Saved & Backed up.")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    app = MiniAI()
    while True:
        print("\nCOMMANDS: [L]earn Files | [T]ype | [R]ecall | [S]leep | [Q]uit")
        c = input(f"Achmed ({app.attributes['level']}) > ").upper().strip()
        
        if c == 'L': app.read_files_and_learn()
        elif c == 'T': app.direct_input()
        elif c == 'R': app.recall_memory()
        elif c == 'S': app.sleep_and_save()
        elif c == 'Q': 
            app.sleep_and_save()
            print("👋 Bye.")
            break
            import sys
import platform
import datetime

def get_mobile_env():
    print(f"--- Mobile Python Environment ---")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Platform: {platform.machine()}")
    print(f"OS: Android (Linux Kernel {platform.release()})")
    print(f"---------------------------------")

if __name__ == "__main__":
    get_mobile_env()
import os
import json
from datetime import datetime

class SovereignMobile:
    def __init__(self):
        self.operator = "Achmed Davids"
        self.company = "Vortex Resonance (Pty) Ltd"
        self.id_number = "7912195264089"
        
        # CATEGORIZED DATA ACCESS
        self.vault = {
            "LEGAL": ["Shaun Case (VW Polo)", "Woodville Primary (Safety/Misconduct)"],
            "FINANCIAL": ["Standard Bank Proposal (R300k)", "FNB/Nedbank Submissions"],
            "ASSETS": ["76 Mitchells Avenue HQ", "Vortex Resonance IP"],
            "LOGISTICS": ["Nissan 1400 Bakkie Research", "Technical Commission Rollout"]
        }

    def authenticate(self):
        """Standard Secure Entry"""
        print(f"--- {self.company} SECURE MOBILE ACCESS ---")
        pin = input("ENTER OPERATOR SECURITY PIN: ")
        if pin == "1952": # Last 4 of your ID or custom
            return True
        return False

    def get_info(self, category):
        """Rapid Information Retrieval"""
        category = category.upper()
        if category in self.vault:
            print(f"\n[RECALLING {category} DATA...]")
            for item in self.vault[category]:
                print(f" > {item}")
        else:
            print("Category not found in Sovereign Vault.")

    def system_status(self):
        """Current Mobile OS Telemetry"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nSTATUS REPORT | {now}")
        print(f"Operator: {self.operator}")
        print(f"HQ: 76 Mitchells Avenue, Woodlands")
        print(f"Active Phase: Technical Commission (TC)")

# --- MOBILE INTERFACE ---
mobile_sys = SovereignMobile()

if mobile_sys.authenticate():
    mobile_sys.system_status()
    # Example: Accessing Legal data on the go
    mobile_sys.get_info("LEGAL")
else:
    print("UNAUTHORIZED ACCESS DETECTED.")
import google.generativeai as genai

# 1. Configuration - Link to the 'Intellect'
# Get your API key from: aistudio.google.com
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# 2. Setup the Model (Gemini 3 Pro)
# This model handles reasoning, coding, and technical analysis
model = genai.GenerativeModel('gemini-3-pro-preview')

def ask_sovereign_intellect(query):
    """Sends hardware or strategic data to the Google core for analysis."""
    
    # Context injection: Reminding the AI who it is working for
    context = (
        "You are the intellect for Vortex Resonance (Pty) Ltd. "
        "User: Achmed Davids. Project: VR3 Monster (10kW). "
        "Hardware: Black Pill, IGBT Muscle, 42mm2 Bus Bars. "
        "Safety threshold: 31.5V. Analyze the following: "
    )
    
    response = model.generate_content(context + query)
    return response.text

# --- 🚀 RUNNING A MOBILE TEST ---
# Example: Asking the intellect to check your winding efficiency logic
output = ask_sovereign_intellect(
    "Analyze the Perfect Space winding methodology for a 6.5kW rated industrial generator. "
    "Check for heat dissipation bottlenecks in 42mm2 twisted copper bus bars."
)

print(output)
import os
import hashlib
import socket
import time
from datetime import datetime

# 1. INTEGRITY GUARD: Detects modified system files or new malware
def calculate_file_hash(filepath):
    """Generates SHA-256 signature to detect tampered files."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# 2. NETWORK SENTRY: Detects Spyware exfiltrating data
def monitor_connections():
    """Scans for active outgoing connections to unknown IPs."""
    # This is a simplified logic; real-world requires 'psutil' or 'socket'
    print(f"[{datetime.now()}] Scanning network arteries...")
    # Logic: If connection != Trusted_HQ_IP, trigger alert.
    pass

# 3. CORE PROTECTION ENGINE
class SovereignGuard:
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir
        self.baseline_hashes = {}

    def secure_baseline(self):
        """Map the 'clean' state of your system."""
        for root, _, files in os.walk(self.watch_dir):
            for file in files:
                path = os.path.join(root, file)
                self.baseline_hashes[path] = calculate_file_hash(path)
        print("✅ System Baseline Secured.")

    def deep_scan(self):
        """Continuous monitor for 'The Beast' & 'VR3' logic protection."""
        while True:
            for path, original_hash in self.baseline_hashes.items():
                if calculate_file_hash(path) != original_hash:
                    print(f"🚨 CRITICAL: File Tampering Detected at {path}!")
                    # TRIGGER: Execute Kill-Switch logic
            time.sleep(60) # Scan interval

# --- INITIALIZE PROTECTION ---
# guard = SovereignGuard("/path/to/vortex/logic")
# guard.secure_baseline()
# guard.deep_scan()
class VortexResonanceCore:
    def __init__(self):
        self.master_profile = "Achmed Davids"
        self.company = "Vortex Resonance (Pty) Ltd"
        
        # 1. THE MONSTER (VR3) - Kinetic Engine
        self.monster_vr3 = {
            "output_rated": "6.5kW",
            "output_peak": "10kW",
            "winding": "Perfect Space Methodology",
            "controller": "ESP32",
            "drivers": "TC4420CPA",
            "muscle": "Dual Parallel IGBTs",
            "bus_bars": "42mm2 hand-twisted copper",
            "protection": ["150A ANL Fuse", "Marine Kill Switch", "XT90-S Anti-Spark"]
        }

        # 2. THE BEAST - Command Hub
        self.the_beast = {
            "type": "High-Fidelity Lifestyle/Cinema",
            "security": ["Face Recognition", "Voice Recognition"],
            "interface": "Biometric Command Hub"
        }

        # 3. SEAMLESS FORTRESS - Gate Automation
        self.gate_motor = {
            "build_cost_zar": 1995,
            "labor_reduction": "80%",
            "mechanism": "High-torque Worm Motor",
            "strategy": "Invisible Strategic Acquisition"
        }

        # 4. INDUSTRIAL AWNING
        self.awning_motor = {
            "application": "Retractable Shield",
            "logic": "Worm Motor Drive",
            "features": ["Wind Resistance", "Horizontal Deployment"]
        }

        # 5. THE SUPERCOMPUTER (Sovereign Box)
        self.supercomputer = {
            "logic_tier": "Quad-Stage Sovereign",
            "role": "Central Ecosystem Redundancy",
            "network": "Multi-node ESP32 Management"
        }

        # 6. POWER RAIL & THE LUNGS
        self.power_system = {
            "voltage_nominal": 36.0,
            "cutoff_voltage": 31.5,
            "cooling_system": "The Lungs (2L External Acid Reservoir)",
            "sensors": "Graphite Probe Acid Sensing",
            "critical_state": "Boiling"
        }

    def get_status(self, project_name):
        """Quick recall for rollout status."""
        return getattr(self, project_name, "Project Not Found")

# Initialize the System
mini_brain = VortexResonanceCore()
class VortexResonanceCore:
    def __init__(self):
        self.master_profile = "Achmed Davids"
        self.company = "Vortex Resonance (Pty) Ltd"
        
        # 1. THE MONSTER (VR3) - Kinetic Engine
        self.monster_vr3 = {
            "output_rated": "6.5kW",
            "output_peak": "10kW",
            "winding": "Perfect Space Methodology",
            "controller": "ESP32",
            "drivers": "TC4420CPA",
            "muscle": "Dual Parallel IGBTs",
            "bus_bars": "42mm2 hand-twisted copper",
            "protection": ["150A ANL Fuse", "Marine Kill Switch", "XT90-S Anti-Spark"]
        }

        # 2. THE BEAST - Command Hub
        self.the_beast = {
            "type": "High-Fidelity Lifestyle/Cinema",
            "security": ["Face Recognition", "Voice Recognition"],
            "interface": "Biometric Command Hub"
        }

        # 3. SEAMLESS FORTRESS - Gate Automation
        self.gate_motor = {
            "build_cost_zar": 1995,
            "labor_reduction": "80%",
            "mechanism": "High-torque Worm Motor",
            "strategy": "Invisible Strategic Acquisition"
        }

        # 4. INDUSTRIAL AWNING
        self.awning_motor = {
            "application": "Retractable Shield",
            "logic": "Worm Motor Drive",
            "features": ["Wind Resistance", "Horizontal Deployment"]
        }

        # 5. THE SUPERCOMPUTER (Sovereign Box)
        self.supercomputer = {
            "logic_tier": "Quad-Stage Sovereign",
            "role": "Central Ecosystem Redundancy",
            "network": "Multi-node ESP32 Management"
        }

        # 6. POWER RAIL & THE LUNGS
        self.power_system = {
            "voltage_nominal": 36.0,
            "cutoff_voltage": 31.5,
            "cooling_system": "The Lungs (2L External Acid Reservoir)",
            "sensors": "Graphite Probe Acid Sensing",
            "critical_state": "Boiling"
        }

    def get_status(self, project_name):
        """Quick recall for rollout status."""
        return getattr(self, project_name, "Project Not Found")

# Initialize the System
mini_brain = VortexResonanceCore()
self.stateclass RestrainedExpert:
    def __init__(self):
        self.state = "SENSORY_ONLY"
        self.mode = "LEG_TO_LEG"
        self.safety_limit = 31.5  # Critical Cutoff
        self.logic_stage = "ESP32_3.3V" #

    def process_input(self, component, landmark):
        # Discard fluff. Focus on physical connection.
        return self.generate_weld_map(component, landmark)

    def generate_weld_map(self, part, location):
        # Step 1: Identify Leg A (Source)
        # Step 2: Identify Leg B (Destination)
        # Step 3: Verify Safety/Isolation
        pass
class RestrainedExpert:
    # Your state logic here
    pass
self.state_class = RestrainedExpert
self.state = RestrainedExpert
# Correct way to assign an instance to a variable
self.state = RestrainedExpert()
import cv2
import numpy as np
import time

# ==========================================
# SYSTEM: VORTEX BENCH ASSISTANT (VBA)
# MODE: ACTIVE BENCH PARTNER
# FUNCTION: COMPONENT ID & MATERIAL ANALYSIS
# ==========================================

class BenchAssistant:
    def __init__(self):
        self.cap = cv2.VideoCapture(0) # Index 0 is usually back camera
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        # DEFINING "SIGHT" (HSV Color Ranges)
        # We teach the machine what "Copper" looks like
        self.copper_lower = np.array([10, 100, 100]) # Low Orange/Brown
        self.copper_upper = np.array([25, 255, 255]) # High Orange/Gold
        
        # We teach the machine what "PCB Green" looks like
        self.pcb_lower = np.array([40, 40, 40])
        self.pcb_upper = np.array([80, 255, 255])

        print("[VBA] EYES OPEN. WAITING FOR INPUT...")

    def draw_hud(self, frame, text, color, box=None):
        """
        Draws the sci-fi style overlay on the screen.
        """
        height, width, _ = frame.shape
        
        # 1. Crosshair in the center (The Fovea)
        cx, cy = width // 2, height // 2
        cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 255, 0), 1)
        cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 255, 0), 1)
        
        # 2. Status Text
        cv2.putText(frame, f"ANALYSIS: {text}", (20, 50), self.font, 0.8, color, 2)
        cv2.putText(frame, "VORTEX RESONANCE", (20, height - 20), self.font, 0.5, (255, 255, 255), 1)

        # 3. Object Box (if detected)
        if box is not None:
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    def scan_materials(self, frame):
        """
        The 'Brain' that identifies what is on the bench.
        """
        # Convert to HSV (Hue, Saturation, Value) for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 1. Check for COPPER (Busbars/Wire)
        mask_copper = cv2.inRange(hsv, self.copper_lower, self.copper_upper)
        contours_copper, _ = cv2.findContours(mask_copper, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # 2. Check for PCB (Green Boards)
        mask_pcb = cv2.inRange(hsv, self.pcb_lower, self.pcb_upper)
        contours_pcb, _ = cv2.findContours(mask_pcb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detected_text = "SCANNING..."
        detected_color = (200, 200, 200) # Grey default
        box = None

        # LOGIC: What is the biggest thing I see?
        if contours_copper:
            largest = max(contours_copper, key=cv2.contourArea)
            if cv2.contourArea(largest) > 500: # Filter out noise
                detected_text = "COPPER CONDUCTOR DETECTED"
                detected_color = (0, 165, 255) # Orange (BGR)
                box = cv2.boundingRect(largest)
                return detected_text, detected_color, box

        if contours_pcb:
            largest = max(contours_pcb, key=cv2.contourArea)
            if cv2.contourArea(largest) > 500:
                detected_text = "PCB / LOGIC BOARD"
                detected_color = (0, 255, 0) # Green
                box = cv2.boundingRect(largest)
                return detected_text, detected_color, box
        
        return detected_text, detected_color, box

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 1. Analyze
            text, color, box = self.scan_materials(frame)
            
            # 2. Visualize
            self.draw_hud(frame, text, color, box)
            
            # 3. Display
            cv2.imshow('VORTEX BENCH ASSISTANT', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.stateclass RestrainedExpert:


# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    assistant = BenchAssistant()
    assistant.run()
self.stateclass RestrainedExpert:
# Option 1: If 'self.state' was just a variable reference or incomplete assignment
self.state = "some_value"  # Make sure to complete this logic
class RestrainedExpert:
    pass

# Option 2: If 'self.state' was accidental debris, simply delete it
class RestrainedExpert:
    pass
import os
import time
import json
import threading
from datetime import datetime

# --- HARDWARE ABSTRACTION LAYER ---
try:
    import android
    droid = android.Android()
    PLATFORM = "ANDROID"
except ImportError:
    print("SYSTEM WARNING: Android module not found. Running in simulation mode.")
    class MockDroid:
        def makeToast(self, msg): print(f"[PHONE DISPLAY]: {msg}")
        def ttsSpeak(self, msg): print(f"[VOICE]: {msg}")
        def recognizeSpeech(self, title, prompt, wait): 
            return [input("[MANUAL INPUT]: ")] # Simulates voice input
        def startActivity(self, intent, uri): print(f"[OPENING APP]: {uri}")
    
    droid = MockDroid()
    PLATFORM = "PC/SIMULATION"

# --- CORE LOGIC: RESTRAINED EXPERT ---
class RestrainedExpert:
    def __init__(self, alias="Pirate3"):
        self.alias = alias
        self.memory_file = "vortex_memory.json"
        self.state = "ACTIVE"
        
        # Core Capabilities (URIs)
        self.commands = {
            "google": "http://google.com",
            "email": "mailto:",
            "youtube": "http://youtube.com",
            "music": "content://media/internal/audio/media"
        }
        
        self.memory = self.load_memory()

    def load_memory(self):
        # Loads habits and past interactions
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass 
        return {"habits": [], "interactions": 0, "start_count": 0}

    def save_memory(self):
        # Commits data to long-term storage
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f)

    def speak(self, text):
        print(f"[{self.alias}]: {text}")
        droid.ttsSpeak(text)

    def listen(self):
        # Activates microphone for command
        print("\n[LISTENING...]")
        try:
            # Pydroid speech recognition intent
            result = droid.recognizeSpeech("Vortex Command", "Speak now...", None)
            if result:
                return result[1].lower() if len(result) > 1 else result[0].lower()
        except Exception as e:
            print(f"Sensor Error: {e}")
        return None

    def execute_command(self, cmd):
        if not cmd:
            return

        self.memory["interactions"] += 1
        self.save_memory()

        # 1. App Launching Logic
        if "open" in cmd:
            for key, uri in self.commands.items():
                if key in cmd:
                    self.speak(f"Opening {key}")
                    droid.startActivity("android.intent.action.VIEW", uri)
                    return
        
        # 2. Status Check
        if "status" in cmd:
            self.speak(f"Systems nominal. Interaction count: {self.memory['interactions']}")
            return

        self.speak(f"Command not recognized: {cmd}")

# --- EXECUTION LOOP ---
if __name__ == "__main__":
    system = RestrainedExpert()
    system.speak(f"Vortex Resonance Systems Online. Platform: {PLATFORM}")
    
    # Simple loop for testing
    while True:
        cmd = system.listen()
        if cmd == "exit":
            break
        system.execute_command(cmd)
