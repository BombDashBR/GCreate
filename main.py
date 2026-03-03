import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import webbrowser

path_to_create_pj = ""
project_name = "Untitled"
script_lua_name = "script"

window = tk.Tk()

window.geometry("500x300")
window.resizable(False, False)
window.title("GCreator")

label_paf = tk.Label(window, text="C:\Program Files (x86)\Steam\steamapps\commun\Garry's Mod\garrymod").pack()

def select_paf():
    paf = filedialog.askdirectory(title="Selecione a pasta de mods do GMOD")

    if paf:
        print(f"Pasta selecionada: {paf}")

        paf_to_create_pj = paf

btn_paf = tk.Button(window, text="Pasta De Mods", command=select_paf).pack(pady=20)

def click_create_project():
    window_create_project = tk.Toplevel(window)
    window_create_project.title("Create New Project")
    window_create_project.resizable(False, False)
    window_create_project.geometry("200x200")

    text_create_project = tk.Label(window_create_project, text="Project Name", font=("Arial", 10)).pack(pady=10)    
    field = tk.Entry(window_create_project, width=20).pack()

    #project_name = field.get()

    btn_create_file = tk.Button(window_create_project, text="Create", command=create_file).pack(pady=20)

    window_create_project.mainloop()

def click_create_script():
    window_create_project = tk.Toplevel(window)
    window_create_project.title("Create New Script Lua")
    window_create_project.resizable(False, False)
    window_create_project.geometry("200x200")

    text_create_project = tk.Label(window_create_project, text="Script Name", font=("Arial", 10)).pack(pady=10)    
    field = tk.Entry(window_create_project, width=20).pack()

    #project_name = field.get()

    btn_create_file = tk.Button(window_create_project, text="Create", command=create_lua_script).pack(pady=20)

    window_create_project.mainloop()

pasta_project = Path(path_to_create_pj)
pasta_lua = pasta_project / "lua"

def create_file():
    pasta_project = Path(path_to_create_pj) / project_name
    pasta_project.mkdir(exist_ok=True)

    project_file = pasta_project / f"{project_name}_was_created_with_gcreator.txt"
    project_file.write_text("This mod was created using a mod creation program for GMOD called GCreator.\n You can install it for free from this website: https://github.com/BombDashBR/GCreate", encoding="utf-8")

    pasta_lua.mkdir(exist_ok=True)
    
    window_project()

def create_lua_script():
    script_lua = pasta_lua / f"{script_lua_name}.lua"
    script_lua.write_text("", encoding="utf-8")

def window_project():
    window_project_manager = tk.Toplevel(window)
    window_project_manager.title(f"{project_name} - GCreator")
    window_project_manager.resizable(False, False)
    window_project_manager.geometry("800x800")

    #apa de criação
    btn_lua = tk.Button(window_project_manager, text="New Script Lua", command=create_lua_script).pack(pady=20)

    window_project_manager.mainloop()

btn_create = tk.Button(window, text="Create New Project", command=click_create_project).pack(pady=50)

btn_donate = tk.Button(window, text="Donate!", command=webbrowser.open("https:/ko-fi.com/roxinhomm"), cursor="hand2", background="light-blue").pack(pady=20)

window.mainloop()