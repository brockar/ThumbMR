from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
import subprocess
import os

class VCSIGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create TabbedPanel
        self.tabbed_panel = TabbedPanel()
        self.add_widget(self.tabbed_panel)

        # Simple Tab
        self.simple_tab = TabbedPanelItem(text='Simple Tab')
        self.tabbed_panel.add_widget(self.simple_tab)

        # Advanced Tab
        self.advanced_tab = TabbedPanelItem(text='Advanced Tab')
        self.tabbed_panel.add_widget(self.advanced_tab)

        # Simple Tab Content
        self.simple_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.simple_tab.content = self.simple_layout

        # Title Label
        self.title_label = Label(text='VCSI GUI', font_size='18sp', bold=True)
        self.simple_layout.add_widget(self.title_label)

        # Recursive Mode
        self.recursive_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.recursive_checkbox = CheckBox()
        self.recursive_checkbox.bind(active=self.toggle_recursive_mode)
        self.recursive_label = Label(text='Recursive Mode', size_hint_x=None, width=150)
        self.recursive_layout.add_widget(self.recursive_checkbox)
        self.recursive_layout.add_widget(self.recursive_label)
        self.simple_layout.add_widget(self.recursive_layout)

        # Input File
        self.input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.input_label = Label(text='Input File/Folder:', size_hint_x=None, width=150)
        self.input_file = TextInput(text='/home/', multiline=False)
        self.browse_button = Button(text='Browse', on_release=self.browse_file)
        self.input_layout.add_widget(self.input_label)
        self.input_layout.add_widget(self.input_file)
        self.input_layout.add_widget(self.browse_button)
        self.simple_layout.add_widget(self.input_layout)

        # Width
        self.width_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.width_label = Label(text='Width:', size_hint_x=None, width=150)
        self.width_input = TextInput(text='1500', multiline=False)
        self.width_layout.add_widget(self.width_label)
        self.width_layout.add_widget(self.width_input)
        self.simple_layout.add_widget(self.width_layout)

        # Grid
        self.grid_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.grid_label = Label(text='Grid:', size_hint_x=None, width=150)
        self.grid_input = TextInput(text='4x4', multiline=False)
        self.grid_layout.add_widget(self.grid_label)
        self.grid_layout.add_widget(self.grid_input)
        self.simple_layout.add_widget(self.grid_layout)

        # End Delay Percentage
        self.end_delay_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.end_delay_label = Label(text='End Delay Percentage:', size_hint_x=None, width=150)
        self.end_delay_input = TextInput(text='20', multiline=False)
        self.end_delay_layout.add_widget(self.end_delay_label)
        self.end_delay_layout.add_widget(self.end_delay_input)
        self.simple_layout.add_widget(self.end_delay_layout)

        # Output File
        self.output_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.output_label = Label(text='Output File:', size_hint_x=None, width=150)
        self.output_file = TextInput(text=os.path.join(os.path.expanduser("~"), "Pictures/routput.png"), multiline=False)
        self.output_layout.add_widget(self.output_label)
        self.output_layout.add_widget(self.output_file)
        self.simple_layout.add_widget(self.output_layout)

        # Run Button
        self.run_button = Button(text='Run', on_release=self.run_vcsi)
        self.simple_layout.add_widget(self.run_button)

        # Advanced Tab Content
        self.advanced_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.advanced_tab.content = self.advanced_layout

        # Add labels for Command and Value
        self.command_label_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.command_label = Label(text='Command', size_hint_x=None, width=150)
        self.value_label = Label(text='Value', size_hint_x=None, width=150)
        self.command_label_layout.add_widget(self.command_label)
        self.command_label_layout.add_widget(self.value_label)
        self.advanced_layout.add_widget(self.command_label_layout)

        self.command_entries = []
        self.add_command_entry()

    def add_command_entry(self, *args):
        command_entry_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        command_entry = TextInput(multiline=False)
        value_entry = TextInput(multiline=False)
        command_entry_layout.add_widget(command_entry)
        command_entry_layout.add_widget(value_entry)
        self.advanced_layout.add_widget(command_entry_layout)
        self.command_entries.append((command_entry, value_entry))

    def browse_file(self, instance):
        content = FileChooserIconView()
        popup = Popup(title='Select File', content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=self.file_selected)
        popup.open()

    def file_selected(self, instance, selection, touch):
        if selection:
            self.input_file.text = selection[0]

    def toggle_recursive_mode(self, checkbox, value):
        if value:
            self.output_label.opacity = 0
            self.output_file.opacity = 0
        else:
            self.output_label.opacity = 1
            self.output_file.opacity = 1

    def run_vcsi(self, instance):
        input_file = self.input_file.text
        width = self.width_input.text
        grid = self.grid_input.text
        end_delay_percentage = self.end_delay_input.text
        output_file = self.output_file.text

        command = [
            "vcsi", input_file,
            "-t",
            "-w", str(width),
            "-g", grid,
            "--end-delay-percent", end_delay_percentage,
            "-o", output_file
        ]

        for command_entry, value_entry in self.command_entries:
            cmd = command_entry.text.strip()
            value = value_entry.text.strip()
            if len(cmd) == 1 and value:
                command.append(f"-{cmd}")
                command.append(value)
            elif len(cmd) == 1:
                command.append(f"-{cmd}")
            elif cmd.startswith("--") and value:
                command.append(cmd)
                command.append(value)
            elif cmd.startswith("--"):
                command.append(cmd)

        subprocess.run(command)

class VCSIApp(App):
    def build(self):
        return VCSIGUI()

if __name__ == '__main__':
    VCSIApp().run()