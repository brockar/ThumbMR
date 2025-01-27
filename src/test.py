from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
import subprocess
import webbrowser
import os

class VCSIGUI(BoxLayout):
    recursive_mode = BooleanProperty(False)
    input_file = StringProperty("/home/")
    width = NumericProperty(1500)
    grid = StringProperty("4x4")
    end_delay_percentage = StringProperty("20")
    output_file = StringProperty(os.path.join(os.path.expanduser("~"), "Pictures/routput.png"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Create tabs
        self.tabs = TabbedPanel()
        self.add_widget(self.tabs)

        # Simple Tab
        simple_tab = TabbedPanelItem(text="Simple Tab")
        self.tabs.add_widget(simple_tab)

        # Advanced Tab
        advanced_tab = TabbedPanelItem(text="Advanced Tab")
        self.tabs.add_widget(advanced_tab)

        # Simple Tab Content
        self.create_simple_tab(simple_tab)

        # Advanced Tab Content
        self.create_advanced_tab(advanced_tab)

    def create_simple_tab(self, tab):
        layout = BoxLayout(orientation="vertical", spacing=10)

        # Title
        layout.add_widget(Label(text="VCSI GUI", font_size=24, size_hint_y=None, height=50))

        # Recursive Mode
        recursive_layout = BoxLayout(orientation="horizontal", spacing=10)
        recursive_layout.add_widget(Label(text="Recursive Mode:", size_hint_x=0.3))
        self.recursive_check = CheckBox(active=self.recursive_mode, size_hint_x=0.1)
        self.recursive_check.bind(active=self.toggle_recursive_mode)
        recursive_layout.add_widget(self.recursive_check)
        layout.add_widget(recursive_layout)

        # Input File
        input_layout = BoxLayout(orientation="horizontal", spacing=10)
        input_layout.add_widget(Label(text="Input File/Folder:", size_hint_x=0.3))
        self.input_entry = TextInput(text=self.input_file, size_hint_x=0.5)
        input_layout.add_widget(self.input_entry)
        browse_button = Button(text="Browse", size_hint_x=0.2)
        browse_button.bind(on_press=self.browse_file)
        input_layout.add_widget(browse_button)
        layout.add_widget(input_layout)

        # Width
        width_layout = BoxLayout(orientation="horizontal", spacing=10)
        width_layout.add_widget(Label(text="Width:", size_hint_x=0.3))
        self.width_slider = Slider(min=500, max=2000, value=self.width, size_hint_x=0.5)
        self.width_slider.bind(value=self.update_width)
        width_layout.add_widget(self.width_slider)
        self.width_entry = TextInput(text=str(self.width), size_hint_x=0.2)
        width_layout.add_widget(self.width_entry)
        layout.add_widget(width_layout)

        # Grid
        grid_layout = BoxLayout(orientation="horizontal", spacing=10)
        grid_layout.add_widget(Label(text="Grid:", size_hint_x=0.3))
        self.grid_entry = TextInput(text=self.grid, size_hint_x=0.7)
        grid_layout.add_widget(self.grid_entry)
        layout.add_widget(grid_layout)

        # End Delay Percentage
        delay_layout = BoxLayout(orientation="horizontal", spacing=10)
        delay_layout.add_widget(Label(text="End Delay Percentage:", size_hint_x=0.3))
        self.delay_entry = TextInput(text=self.end_delay_percentage, size_hint_x=0.7)
        delay_layout.add_widget(self.delay_entry)
        layout.add_widget(delay_layout)

        # Output File
        output_layout = BoxLayout(orientation="horizontal", spacing=10)
        output_layout.add_widget(Label(text="Output File:", size_hint_x=0.3))
        self.output_entry = TextInput(text=self.output_file, size_hint_x=0.7)
        output_layout.add_widget(self.output_entry)
        layout.add_widget(output_layout)

        # Run Button
        run_button = Button(text="Run", size_hint_y=None, height=50)
        run_button.bind(on_press=self.run_vcsi)
        layout.add_widget(run_button)

        tab.add_widget(layout)

    def create_advanced_tab(self, tab):
        layout = BoxLayout(orientation="vertical", spacing=10)

        # Commands Info Button
        commands_info_button = Button(text="Commands Info", size_hint_y=None, height=50)
        commands_info_button.bind(on_press=self.open_commands_info)
        layout.add_widget(commands_info_button)

        # Add Command Button
        add_command_button = Button(text="Add Command", size_hint_y=None, height=50)
        add_command_button.bind(on_press=self.add_command_entry)
        layout.add_widget(add_command_button)

        # Scrollable Area for Commands
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        self.commands_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.commands_layout.bind(minimum_height=self.commands_layout.setter("height"))
        scroll_view.add_widget(self.commands_layout)
        layout.add_widget(scroll_view)

        tab.add_widget(layout)

    def toggle_recursive_mode(self, instance, value):
        self.recursive_mode = value
        self.output_entry.disabled = value

    def browse_file(self, instance):
        if self.recursive_mode:
            self.file_chooser_popup("Select Directory", self.input_entry, is_folder=True)
        else:
            self.file_chooser_popup("Select File", self.input_entry)

    def file_chooser_popup(self, title, target_widget, is_folder=False):
        content = BoxLayout(orientation="vertical")
        file_chooser = FileChooserListView()
        content.add_widget(file_chooser)
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.9))

        def on_select(instance):
            target_widget.text = file_chooser.selection and file_chooser.selection[0] or ""
            popup.dismiss()

        select_button = Button(text="Select", size_hint_y=None, height=50)
        select_button.bind(on_press=on_select)
        content.add_widget(select_button)

        popup.open()

    def update_width(self, instance, value):
        self.width = int(value)
        self.width_entry.text = str(self.width)

    def add_command_entry(self, instance):
        command_entry = TextInput(hint_text="Command", size_hint_y=None, height=50)
        value_entry = TextInput(hint_text="Value", size_hint_y=None, height=50)
        self.commands_layout.add_widget(command_entry)
        self.commands_layout.add_widget(value_entry)

    def open_commands_info(self, instance):
        webbrowser.open("https://github.com/amietn/vcsi?tab=readme-ov-file#usage")

    def run_vcsi(self, instance):
        input_file = self.input_entry.text
        width = self.width
        grid = self.grid_entry.text
        end_delay_percentage = self.delay_entry.text
        output_file = self.output_entry.text

        command = [
            "vcsi", input_file,
            "-t",
            "-w", str(width),
            "-g", grid,
            "--end-delay-percent", end_delay_percentage,
            "-o", output_file
        ]

        for i in range(0, len(self.commands_layout.children), 2):
            cmd = self.commands_layout.children[i + 1].text.strip()
            value = self.commands_layout.children[i].text.strip()
            if cmd and value:
                command.append(f"-{cmd}")
                command.append(value)

        subprocess.run(command)

class VCSIApp(App):
    def build(self):
        return VCSIGUI()

if __name__ == "__main__":
    VCSIApp().run()