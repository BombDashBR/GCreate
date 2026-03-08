import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import webbrowser
import json

CONFIG_FILE = Path(__file__).parent / "config.json"

def save_config(path):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"last_path": str(path)}, f)
    except Exception as e:
        print(f"Error saving configuration: {e}")

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("last_path", "")
        except:
            return ""
    return ""

path_to_create_pj = load_config()
project_name = "Untitled"

window = tk.Tk()
window.geometry("400x450")
window.resizable(False, False)
window.title("GCreator")

lbl_path_status = tk.Label(window, text=f"Folder: {path_to_create_pj if path_to_create_pj else 'None selected'}", fg="gray", font=("Arial", 8), wraplength=350)

try:
    logo_path = Path(__file__).parent / "gcreator logo.png"
    img_aberta = Image.open(logo_path) 
    img_redimensionada = img_aberta.resize((60, 60))
    logo_img = ImageTk.PhotoImage(img_redimensionada)
    label_logo = tk.Label(window, image=logo_img)
    label_logo.pack(pady=10)
    label_logo.image = logo_img 
except Exception as e:
    tk.Label(window, text="GCreator", font=("Arial", 20, "bold")).pack(pady=10)

def open_page_donate():
    webbrowser.open("https://ko-fi.com/roxinhomm")

def select_paf():
    global path_to_create_pj
    paf = filedialog.askdirectory(title="Select the GMOD mods folder")
    if paf:
        path_to_create_pj = paf
        save_config(paf)
        lbl_path_status.config(text=f"Pasta: {paf}")

def save_weapon_file(data, window_to_close):
    global path_to_create_pj, project_name

    pasta_weapons = Path(path_to_create_pj) / project_name / "lua" / "weapons"
    pasta_weapons.mkdir(parents=True, exist_ok=True)
    
    clean_name = data['name'].lower().replace(" ", "_")
    if not clean_name: clean_name = "custom_weapon"
    
    file_path = pasta_weapons / f"weapon_{clean_name}.lua"
    
    lua_content = f"""
SWEP.PrintName = "{data['name']}"
SWEP.Author = "{data['author']}"
SWEP.Category = "{data['category']}"
SWEP.Spawnable = true
SWEP.AdminOnly = {data['admin']}
SWEP.Base = "weapon_base"

SWEP.Primary.Damage = {data['damage']}
SWEP.Primary.ClipSize = {data['clip']}
SWEP.Primary.Ammo = "{data['ammo']}"
SWEP.Primary.Automatic = {data['auto']}
SWEP.Primary.Delay = {data['delay']}
SWEP.Primary.Recoil = {data['recoil']}
SWEP.Primary.Force = {data['force']}
SWEP.Primary.Spread = {data['spread']}

SWEP.ViewModel = "models/weapons/c_pistol.mdl"
SWEP.WorldModel = "models/weapons/w_pistol.mdl"

function SWEP:PrimaryAttack()
    if ( !self:CanPrimaryAttack() ) then return end
    self:ShootEffects()
    self:EmitSound("Weapon_Pistol.Single")
    self:TakePrimaryAmmo(1)
    self:SetNextPrimaryFire( CurTime() + self.Primary.Delay )
end

function SWEP:Reload()
    self:DefaultReload(ACT_VM_RELOAD)
end
"""
    try:
        file_path.write_text(lua_content, encoding="utf-8")
        messagebox.showinfo("Success!", f"Weapon created in: lua/weapons/weapon_{clean_name}.lua")
        window_to_close.destroy()
    except Exception as e:
        messagebox.showerror("Error 404", f"Failed to save: {e}")

def click_create_weapon():
    win_wep = tk.Toplevel(window)
    win_wep.title("Configure Weapon")
    win_wep.geometry("400x620")
    
    entries = {}
    fields = [
        ("Weapon Name", "name", "Gun"),
        ("Author", "author", "Anonymous"),
        ("Category", "category", "GCreator Mods"),
        ("Damage", "damage", "25"),
        ("Clip", "clip", "30"),
        ("Ammo Type", "ammo", "Pistol"),
        ("Delay", "delay", "0.1"),
        ("Recoil", "recoil", "1.0"),
        ("Force", "force", "5"),
        ("Spread", "spread", "0.01")
    ]

    for label_text, key, default in fields:
        tk.Label(win_wep, text=label_text, font=("Arial", 9, "bold")).pack(pady=(5, 0))
        entry = tk.Entry(win_wep)
        entry.insert(0, default)
        entry.pack(pady=2, padx=20, fill="x")
        entries[key] = entry

    var_admin = tk.StringVar(value="false")
    tk.Checkbutton(win_wep, text="Admin only?", variable=var_admin, onvalue="true", offvalue="false").pack()
    
    var_auto = tk.StringVar(value="true")
    tk.Checkbutton(win_wep, text="Automatic?", variable=var_auto, onvalue="true", offvalue="false").pack()

    def collect_and_save():
        data = {k: e.get() for k, e in entries.items()}
        data['admin'] = var_admin.get()
        data['auto'] = var_auto.get()
        save_weapon_file(data, win_wep)

    tk.Button(win_wep, text="Create", bg="#27ae60", fg="white", command=collect_and_save).pack(pady=20)

def save_lua_script():
    name = field_cs.get().strip()
    path = Path(path_to_create_pj) / project_name / "lua" / f"{name}.lua"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("-- Script created with GCreator", encoding="utf-8")
    messagebox.showinfo("OK", "Script Created!")
    window_script_popup.destroy()

def click_create_script():
    global window_script_popup, field_cs
    window_script_popup = tk.Toplevel(window)
    window_script_popup.title("New Script")
    window_script_popup.geometry("250x150")
    tk.Label(window_script_popup, text="Script Name: ").pack(pady=10)
    field_cs = tk.Entry(window_script_popup)
    field_cs.pack()
    tk.Button(window_script_popup, text="Save", command=save_lua_script).pack(pady=15)

def window_project():
    win_pj = tk.Toplevel(window)
    win_pj.title(f"Project: {project_name}")
    win_pj.geometry("350x300")
    tk.Label(win_pj, text=f"Project: {project_name}", font=("Arial", 12, "bold")).pack(pady=15)
    tk.Button(win_pj, text="New Script Lua", width=25, command=click_create_script).pack(pady=10)
    tk.Button(win_pj, text="New Weapon (SWEP)", width=25, command=click_create_weapon).pack(pady=10)

def start_project():
    global project_name, path_to_create_pj
    project_name = field_cp.get().strip()
    if not path_to_create_pj or not project_name:
        messagebox.showwarning("Warning", "Fill in the name and select the folder!")
        return
    
    base_path = Path(path_to_create_pj) / project_name
    try:
        (base_path / "lua" / "weapons").mkdir(parents=True, exist_ok=True)
        win_new_pj.destroy()
        window_project()
    except Exception as e:
        messagebox.showerror("Error 404", f"Error creating folders: {e}")

def click_create_project():
    global win_new_pj, field_cp
    if not path_to_create_pj:
        messagebox.showwarning("Warning", "Select the mods folder")
        return
    win_new_pj = tk.Toplevel(window)
    win_new_pj.title("New Project")
    win_new_pj.geometry("250x150")
    tk.Label(win_new_pj, text="Name Project:").pack(pady=10)
    field_cp = tk.Entry(win_new_pj)
    field_cp.pack()
    tk.Button(win_new_pj, text="Create Now", bg="#27ae60", fg="white", command=start_project).pack(pady=15)

tk.Button(window, text="Select Mods Folder", width=30, command=select_paf).pack(pady=20)

lbl_path_status.pack(pady=5)

tk.Button(window, text="Create New Project", width=30, command=click_create_project).pack(pady=20)

btn_donate = tk.Button(window, text="Donate!", width=15, bg="lightblue", command=open_page_donate)
btn_donate.pack(side="bottom", pady=20)

if __name__ == "__main__":
    window.mainloop()