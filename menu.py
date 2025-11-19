import dearpygui.dearpygui as dpg
import minescript
import os



Width = 500
Height = 500

scripts_location = "scripts"

asd = os.path.join(os.path.dirname(os.path.abspath(__file__)), scripts_location)

files = [f for f in os.listdir(asd) if os.path.isfile(os.path.join(asd, f))]

dpg.create_context()
dpg.create_viewport(
    title='Minescript',
    width=Width,
    height=Height,
    decorated=True,
    always_on_top=False,
    resizable=False,
)
dpg.setup_dearpygui()

with dpg.window(
    label="Example Window",
    tag="main_window",
    width=Width,
    height=Height,
    no_resize=True,
    no_move=True,
    collapsed=False
):
    for file in files:
        file_nopy = file[:-3]
        file_exe = f"\menu\scripts\{file_nopy}"
        
        dpg.add_checkbox(label=file_nopy, 
        callback=lambda s, a, u: minescript.execute(u), 
        user_data=file_exe)
        
        


if __name__ == "__main__":
    minescript.echo("Minescript GUI started")
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()