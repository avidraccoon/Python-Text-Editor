from imgui_bundle import imgui, imgui_color_text_edit as ed, imgui_md
from imgui_bundle.immapp import static
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


import sys, subprocess, threading

TextEditor = ed.TextEditor
opening_file = [False]
current_tab = 0
id = 0
tabs = []

# Editor, filename
creatingTab = False

def open_file(file, editor):
    print(file, editor)
    with open(file, encoding="utf8") as f:
        this_file_code = f.read()
    editor.set_text(this_file_code)


def _prepare_text_editor():
    
    editor = TextEditor()
    editor.set_language_definition(TextEditor.LanguageDefinition.python())
    return editor
file = __file__
editor = _prepare_text_editor()
tabs.append([editor, file, "new"])
open_file(file, editor)
current_tab = len(tabs)
creatingTab = True
def save_file(editor):
    with open(tabs[current_tab][1], encoding="utf8", mode="w") as f:
        f.write(editor.get_text())


def demo_gui():
    global opening_file, current_tab, tabs, spareEditor, creatingTab
    static = demo_gui
    editing = current_tab >= 0
    if len(tabs) > 0 and current_tab >= 0 and current_tab < len(tabs):
        current_editor = tabs[current_tab][0]
    elif len(tabs) > 0 and current_tab>=len(tabs):
        current_tab = len(tabs)-1
        current_editor = _prepare_text_editor()
        editing = True
    else:
        tabs.append([_prepare_text_editor(), "Untitled", "new"])
        current_tab = len(tabs)-1
        current_editor = tabs[-1][0]
        editing = True
        creatingTab = True
    tab = tabs[current_tab]
    
    if imgui.is_key_pressed(imgui.Key.s) and imgui.get_io().key_ctrl and editing:
        save_file(current_editor)

    if imgui.is_key_pressed(imgui.Key.o) and imgui.get_io().key_ctrl:
        file = filedialog.askopenfilename()
        if not file == "":
            editor = _prepare_text_editor()
            tabs.append([editor, file, "new"])
            open_file(file, editor)
            current_tab = len(tabs)-1
            creatingTab = True
    if imgui.is_key_pressed(imgui.Key.r) and imgui.get_io().key_ctrl:
        t = threading.Thread(target = subprocess.call, args= ["python main.py"], kwargs={"shell": True})
        t.start()
        sys.exit()
    
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("Menu"):
            if imgui.menu_item_simple("Restart", "Ctrl+R"):
                t = threading.Thread(target = subprocess.call, args= ["python main.py"], kwargs={"shell": True})
                t.start()
                sys.exit()
            imgui.end_menu()
            
                
        if imgui.begin_menu("File"):
            if imgui.menu_item_simple("Open", "Ctrl+O"):
                file = filedialog.askopenfilename()
                if not file == "":
                    editor = _prepare_text_editor()
                    tabs.append([editor, file, "new"])
                    open_file(file, editor)
                    current_tab = len(tabs)
                    creatingTab = True
            if imgui.menu_item_simple("Save", "Ctrl+S") and editing:
                save_file(current_editor)
            imgui.end_menu()
        imgui.end_main_menu_bar()
    imgui.text("")
    if imgui.begin_tab_bar("Tabs"):
        keepTrue = False
        if (len(tabs)> 0):
            for i in range(len(tabs)-1, -1, -1):
                ctab = tabs[i]
                text = ctab[1]+""
                flag = 0
                if ctab[2] == "new":
                    flag = imgui.TabItemFlags_.set_selected.value
                    ctab[2] = False
                #Fix later
                #if ctab[2]:
                #    if ctab[2] == "change":
                #        keepTrue = True
                #        ctab[2] = True
                #    text+=" *"
                ret = imgui.begin_tab_item(text, True, flags=flag)
                if ret[0]:
                    if not creatingTab:
                        current_tab = i
                    if not ret[1]:
                        tabs.pop(i)
                    imgui.end_tab_item()
        else:
            #if imgui.begin_tab_item("Untitled"):
            #    imgui.end_tab_item()
            pass
        creatingTab = keepTrue
        if imgui.tab_item_button("+", imgui.TabItemFlags_.trailing.value | imgui.TabItemFlags_.no_tooltip.value):
            global id
            tabs.append([_prepare_text_editor(), "Untitled "+str(id), "new"])
            id += 1
            current_tab = len(tabs)-1
            creatingTab = True
        imgui.end_tab_bar()
    imgui.push_font(imgui_md.get_code_font())
    if not tab[2] and current_editor.is_text_changed():
        creatingTab = True
        tab[2] = "change"
    current_editor.render("Code")
    imgui.pop_font()
    
    


def main():
    from imgui_bundle import immapp

    immapp.run(demo_gui, with_markdown=True)


if __name__ == "__main__":
    main()
