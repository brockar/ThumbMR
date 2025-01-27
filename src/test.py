from dearpygui.dearpygui import *

add_text("Hello, World!")
add_button("OK", callback=lambda: print("Button clicked"))
start_dearpygui()