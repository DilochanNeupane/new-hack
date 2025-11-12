"""
prank_hacker_realistic.py
Highly realistic-looking, harmless "hacked" prank UI.

DOES NOT access or modify files, networks, or system settings.
Purely visual. Press ESC to quit immediately.
"""

import tkinter as tk
import threading
import random
import time
import math
import sys

# Optional short Windows beep - harmless
try:
    if sys.platform.startswith("win"):
        import winsound
    else:
        winsound = None
except Exception:
    winsound = None

# ------------- Config -------------
WIDTH = 1200
HEIGHT = 720
FULLSCREEN = False   # set True for fullscreen effect (be careful while testing)
FONT_MONO = ("Consolas", 13)
FONT_BIG = ("Helvetica", 32, "bold")
# -----------------------------------

root = tk.Tk()
root.title("SYSTEM ALERT - Unauthorized Access Detected")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="black")
root.attributes("-topmost", True)
if FULLSCREEN:
    root.attributes("-fullscreen", True)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Close on ESC
def close(event=None):
    try:
        root.destroy()
    except:
        pass

root.bind("<Escape>", close)

# Global state for UI updates
frame = 0
running = True

# Utility: draw semi-transparent rectangle by stipple (tkinter limited)
def draw_panel(x0, y0, x1, y1, fill="#0b1320", tag=None):
    canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="", tags=tag)

# ---------------- Matrix rain background ----------------
cols = int(WIDTH / 12)
drops = [random.randint(-HEIGHT, 0) for _ in range(cols)]
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*()[]{}<>?/|\\"

def draw_matrix():
    canvas.delete("matrix")
    for i in range(cols):
        x = i * 12
        y = drops[i]
        glyph = random.choice(chars)
        canvas.create_text(x + 6, y, text=glyph, anchor="nw", font=("Consolas", 11), fill="#0faa5f", tags="matrix")
        drops[i] += random.randint(6, 18)
        if drops[i] > HEIGHT + 20:
            drops[i] = random.randint(-200, 0)

# ---------------- Fake terminal with typing ----------------
terminal_lines = []
TERMINAL_MAX = 30
terminal_lock = threading.Lock()

def add_terminal_line(text, color="#9ef2c2"):
    with terminal_lock:
        terminal_lines.append((text, color))
        if len(terminal_lines) > TERMINAL_MAX:
            terminal_lines.pop(0)

def draw_terminal():
    canvas.delete("terminal")
    tx, ty = 30, 30
    panel_w = 760
    panel_h = 380
    draw_panel(tx-8, ty-8, tx+panel_w, ty+panel_h, fill="#071013", tag="terminal")
    y = ty
    with terminal_lock:
        for text, color in terminal_lines:
            canvas.create_text(tx+6, y, text=text, anchor="nw", font=FONT_MONO, fill=color, tags="terminal")
            y += 22

# Simulated typing for a string (visual only)
def type_line(text, color="#9ef2c2", speed=0.02):
    buf = ""
    for ch in text:
        buf += ch
        add_terminal_line(buf + "_", color)
        time.sleep(speed)
        # remove the last temporary line to avoid duplication
        if terminal_lines:
            terminal_lines.pop()
    add_terminal_line(text, color)

# ---------------- Fake file scanner & progress ----------------
fake_files = []
# generate many believable-looking file paths
folders = ["Documents", "Pictures", "Desktop", "Wallets", "Backups", "Downloads", "Secrets"]
for f in range(1, 70):
    folder = random.choice(folders)
    name = random.choice(["tax", "invoice", "id", "photo", "wallet", "notes", "pass", "ssn", "backup"])
    ext = random.choice([".docx", ".pdf", ".jpg", ".png", ".csv", ".xlsx", ".txt", ".db"])
    fake_files.append(f"/home/user/{folder}/{name}_{random.randint(1,9999)}{ext}")

scan_index = 0
file_status = {f: "OK" for f in fake_files}
file_lock = threading.Lock()

def draw_file_panel():
    canvas.delete("files")
    panel_x = 820
    panel_y = 30
    panel_w = WIDTH - panel_x - 30
    panel_h = 380
    draw_panel(panel_x-8, panel_y-8, panel_x+panel_w, panel_y+panel_h, fill="#071018", tag="files")
    canvas.create_text(panel_x+10, panel_y+10, text="DATA SCAN (local files)", anchor="nw", font=FONT_MONO, fill="#d6ffe6", tags="files")
    y = panel_y + 40
    with file_lock:
        for i in range(12):
            if scan_index + i < len(fake_files):
                f = fake_files[scan_index + i]
                status = file_status[f]
                color = "#66ff66" if status == "OK" else "#ff4c4c"
                display = f"{f[:60]:60}  [{status}]"
                canvas.create_text(panel_x+10, y, text=display, anchor="nw", font=("Consolas", 11), fill=color, tags="files")
                y += 20

# ---------------- Fake processes panel ----------------
processes = [
    ("ssh", 2), ("chrome", 18), ("discord", 5), ("dropbox", 1), 
    ("cameraSvc", 2), ("walletd", 0.5), ("backupd", 0.3), ("sysmon", 1)
]
def draw_process_panel(cpu_sim=0):
    canvas.delete("procs")
    px, py = 30, 430
    pw, ph = 520, 200
    draw_panel(px-8, py-8, px+pw, py+ph, fill="#071018", tag="procs")
    canvas.create_text(px+12, py+6, text="PROCESS MONITOR", anchor="nw", font=FONT_MONO, fill="#dfffe0", tags="procs")
    y = py + 36
    # Simulate CPU usage bar
    canvas.create_text(px+12, y, text=f"CPU USAGE: {cpu_sim:.1f}%", anchor="nw", font=("Consolas", 12), fill="#fff", tags="procs")
    bar_x0, bar_y0 = px+12, y+26
    bar_x1, bar_y1 = px+400, bar_y0 + 18
    canvas.create_rectangle(bar_x0, bar_y0, bar_x1, bar_y1, outline="#444", tags="procs")
    fill_x = bar_x0 + (bar_x1-bar_x0) * min(cpu_sim/100.0, 1.0)
    canvas.create_rectangle(bar_x0, bar_y0, fill_x, bar_y1, fill="#ff6b6b", width=0, tags="procs")
    y += 70
    # list processes
    for name, base in processes:
        usage = base + random.random() * 8
        canvas.create_text(px+12, y, text=f"{name:12}  PID {1000+random.randint(1,9000):5}   CPU {usage:.1f}%", anchor="nw", font=("Consolas", 11), fill="#bfffd8", tags="procs")
        y += 18

# ---------------- Fake popups (visual only) ----------------
def spawn_popup(title, message, kind="error"):
    # simple styled rectangle that looks like a native dialog
    popup_w = 480
    popup_h = 160
    x = WIDTH//2 - popup_w//2 + random.randint(-60,60)
    y = HEIGHT//2 - popup_h//2 + random.randint(-40,40)
    tag = f"popup_{int(time.time()*1000)}"
    bg = "#2b0000" if kind=="error" else "#222233"
    txtcol = "#ffb3b3" if kind=="error" else "#dfe6ff"
    canvas.create_rectangle(x, y, x+popup_w, y+popup_h, fill=bg, outline="#ff4444", width=2, tags=tag)
    canvas.create_text(x+20, y+18, anchor="nw", text=title, font=("Helvetica", 16, "bold"), fill=txtcol, tags=tag)
    canvas.create_text(x+20, y+56, anchor="nw", text=message, font=("Consolas", 12), fill="#fff", width=popup_w-40, tags=tag)
    # auto remove after a few seconds
    root.after(4000, lambda: canvas.delete(tag))

# --------------- Fake SSH / Banner ---------------
def draw_banner():
    canvas.delete("banner")
    banner_text = "SSH: attacker@darknet ~> connected"
    canvas.create_text(WIDTH//2, HEIGHT-32, text=banner_text, anchor="s", font=("Consolas", 10, "italic"), fill="#a6f0b3", tags="banner")

# --------------- Realistic sequences (background thread) ---------------
def background_sequence():
    global frame, scan_index, running
    # initial dramatic lines
    sequences = [
        ("[INIT] Bootstrapping remote exploit modules...", 0.02),
        ("[CORE] Establishing covert channel...", 0.03),
        ("[CORE] Exploit loaded: CVE-FAKE-2025", 0.02),
        ("[CORE] Gaining privileges: OK", 0.02),
        ("[SCAN] Enumerating local storage...", 0.02),
    ]
    for text, speed in sequences:
        type_line(text, color="#9ef2c2", speed=speed)
        time.sleep(0.35)

    # Simulate scanning many files
    for i in range(0, len(fake_files), 12):
        if not running:
            return
        with file_lock:
            scan_index = i
        # "processing" block
        for f in fake_files[i:i+12]:
            if not running:
                return
            add_terminal_line(f"> scanning {f[:60]}", "#9ef2c2")
            # small chance to mark as sensitive
            if random.random() < 0.07:
                with file_lock:
                    file_status[f] = "SENSITIVE"
                add_terminal_line(f"  -> SENSITIVE DATA FOUND: {f.split('/')[-1]}", "#ffd6a5")
            time.sleep(0.06 + random.random()*0.06)
        time.sleep(0.3)

    # simulate data exfiltrate progress
    add_terminal_line("[EXFIL] Preparing data transfer stream...", "#9ef2c2")
    total = 100
    for p in range(total+1):
        if not running:
            return
        add_terminal_line(f"[EXFIL] Uploading... {p}%", "#eaffff")
        # occasional fake network gibberish
        if p % 7 == 0:
            add_terminal_line("> NET: SYN ACK ...", "#bfefff")
        time.sleep(0.05)

    # dramatic: mark many files as ENCRYPTED or ERASED
    for f in random.sample(fake_files, k=min(18, len(fake_files))):
        if not running:
            return
        with file_lock:
            file_status[f] = random.choice(["ERASED", "ENCRYPTED"])
        add_terminal_line(f"[!!!] {f} -> {file_status[f]}", "#ff8a8a")
        # dramatic beep on Windows
        try:
            if winsound and random.random() < 0.3:
                winsound.Beep(800, 150)
        except:
            pass
        time.sleep(0.08)

    # final ransom-like banner
    add_terminal_line(">>> PAYLOAD DEPLOYED - CHECK INSTRUCTIONS ON DARKNET", "#ffb3b3")
    spawn_popup("!!! CRITICAL !!!", "All user documents encrypted. Payment required. (FAKE)", kind="error")
    # final simulated countdown (visual only)
    for t in range(10, 0, -1):
        add_terminal_line(f"[ALERT] Self-destruct sequence in {t}s", "#ffb3b3")
        time.sleep(1)
    add_terminal_line("[NOTICE] This was a prank demo. No real harm done.", "#a6f0b3")

# --------------- Main UI update loop ---------------
def ui_loop():
    global frame
    cpu_sim = 5.0
    while running:
        frame += 1
        draw_matrix()
        draw_terminal()
        draw_file_panel()
        # simulate CPU slowly varying
        cpu_sim = 10 + 30 * abs(math.sin(frame * 0.03)) + random.random()*5
        draw_process_panel(cpu_sim)
        draw_banner()

        # occasionally spawn realistic popups
        if random.random() < 0.01:
            spawn_popup("SECURITY ALERT", "Unauthorized access detected in camera module.", kind="error")
        if random.random() < 0.008:
            spawn_popup("NETWORK", "Outgoing connection detected to 185.120.45.77:443", kind="info")

        root.update_idletasks()
        root.update()
        time.sleep(0.06)

# Start threads
t_bg = threading.Thread(target=background_sequence, daemon=True)
t_ui = threading.Thread(target=ui_loop, daemon=True)
t_bg.start()
t_ui.start()

# Final safety: ensure root.mainloop() so Esc binding works reliably
try:
    root.mainloop()
except:
    running = False

running = False
