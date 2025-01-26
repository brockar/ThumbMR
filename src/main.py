import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
import subprocess
import webbrowser
import os

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("VSCI GUI")

        self.style = Style(theme="darkly")
        self.style.configure("TLabel", padding=6, font=("Helvetica", 12), background="#2c2c2c", foreground="#ffffff")
        self.style.configure("TButton", padding=6, font=("Helvetica", 12), bootstyle="success-outline")
        self.style.configure("TEntry", padding=6, font=("Helvetica", 12), fieldbackground="#2c2c2c", foreground="#ffffff")
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), foreground="#ffffff", background="#2c2c2c")
        self.style.configure("TFrame", background="#2c2c2c")

        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        notebook = ttk.Notebook(self.master)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Simple Tab
        simple_tab = ttk.Frame(notebook)
        notebook.add(simple_tab, text="Simple Tab")

        # Advanced Tab
        advanced_tab = ttk.Frame(notebook)
        notebook.add(advanced_tab, text="Advanced Tab")

        # Main Frame for Simple Tab
        main_frame = ttk.Frame(simple_tab, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid to be responsive
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Title Label
        title_label = ttk.Label(main_frame, text="VCSI GUI", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Recursive Mode
        self.recursive_var = tk.BooleanVar()
        self.recursive_check = ttk.Checkbutton(main_frame, text="Recursive Mode", variable=self.recursive_var, command=self.toggle_recursive_mode)
        self.recursive_check.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        # Input File
        ttk.Label(main_frame, text="Input File/Folder:").grid(row=2, column=0, sticky="W")
        self.input_file = ttk.Entry(main_frame, width=50)
        self.input_file.insert(0, "/home/")
        self.input_file.grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        self.browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_file, bootstyle="success-outline")
        self.browse_button.grid(row=2, column=2, padx=5, pady=5)

        # Width
        ttk.Label(main_frame, text="Width:").grid(row=3, column=0, sticky="W")
        self.width_var = tk.IntVar(value=1500)
        self.width_scale = ttk.Scale(main_frame, from_=500, to=2000, orient=tk.HORIZONTAL, variable=self.width_var, command=self.update_width_entry)
        self.width_scale.grid(row=3, column=1, padx=5, pady=5, sticky="EW")
        self.width_entry = ttk.Entry(main_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=3, column=2, padx=5, pady=5, sticky="EW")

        # Grid
        ttk.Label(main_frame, text="Grid:").grid(row=4, column=0, sticky="W")
        self.grid = ttk.Entry(main_frame, width=10)
        self.grid.insert(0, "4x4")
        self.grid.grid(row=4, column=1, padx=5, pady=5, sticky="EW")

        # End Delay Percentage
        ttk.Label(main_frame, text="End Delay Percentage:").grid(row=5, column=0, sticky="W")
        self.end_delay_percentage = ttk.Entry(main_frame)
        self.end_delay_percentage.insert(0, "20")
        self.end_delay_percentage.grid(row=5, column=1, padx=5, pady=5, sticky="EW")

        # Output File
        self.output_label = ttk.Label(main_frame, text="Output File:")
        self.output_label.grid(row=6, column=0, sticky="W")
        self.output_file = ttk.Entry(main_frame)
        output_path = os.path.join(os.path.expanduser("~"), "Pictures/routput.png")
        self.output_file.insert(0, output_path)
        self.output_file.grid(row=6, column=1, padx=5, pady=5, sticky="EW")

        # Run Button
        self.run_button = ttk.Button(main_frame, text="Run", command=self.run_vcsi, bootstyle="success-outline")
        self.run_button.grid(row=7, column=0, columnspan=3, pady=20)

        # Advanced Tab Content
        self.advanced_frame = ttk.Frame(advanced_tab, padding="20 20 20 20")
        self.advanced_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.advanced_frame.grid_columnconfigure(1, weight=1)

        # Add labels for Command and Value
        ttk.Label(self.advanced_frame, text="Command").grid(row=0, column=1, padx=2, pady=2, sticky="EW")
        ttk.Label(self.advanced_frame, text="Value").grid(row=0, column=2, padx=2, pady=2, sticky="EW")

        self.command_entries = []
        self.add_command_entry()

        commands_info_button = ttk.Button(self.advanced_frame, text="Commands info", command=self.open_commands_info, bootstyle="info-outline")
        commands_info_button.grid(row=0, column=3, columnspan=3, padx=5, pady=5, sticky="E")

        add_command_button = ttk.Button(self.advanced_frame, text="Add Command", command=self.add_command_entry, bootstyle="success-outline")
        add_command_button.grid(row=1, column=3, columnspan=3, padx=5, pady=5, sticky="E")

    def add_command_entry(self):
        row = len(self.command_entries) + 1
        command_label = ttk.Label(self.advanced_frame, text=f"Command {row}:")
        command_label.grid(row=row, column=0, sticky="W")
        command_entry = ttk.Entry(self.advanced_frame, width=25)
        command_entry.grid(row=row, column=1, padx=5, pady=5, sticky="EW")
        value_entry = ttk.Entry(self.advanced_frame, width=25)
        value_entry.grid(row=row, column=2, padx=5, pady=5, sticky="EW")
        self.command_entries.append((command_entry, value_entry))

    def open_commands_info(self):
        webbrowser.open("https://github.com/amietn/vcsi?tab=readme-ov-file#usage")

    def update_width_entry(self, event):
        self.width_var.set(int(self.width_scale.get()))

    def browse_file(self):
        initial_dir = "/home"
        if self.recursive_var.get():
            directory = filedialog.askdirectory(initialdir=initial_dir)
            if directory:
                self.input_file.delete(0, 'end')
                self.input_file.insert(0, directory)
        else:
            filetypes = [
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm"),
                ("All files", "*.*")
            ]
            file = filedialog.askopenfilename(initialdir=initial_dir, filetypes=filetypes)
            if file:
                self.input_file.delete(0, 'end')
                self.input_file.insert(0, file)

    def toggle_recursive_mode(self):
        if self.recursive_var.get():
            self.output_label.grid_remove()
            self.output_file.grid_remove()
        else:
            self.output_label.grid()
            self.output_file.grid()

    def run_vcsi(self):
        input_file = self.input_file.get()
        width = self.width_var.get()
        grid = self.grid.get()
        end_delay_percentage = self.end_delay_percentage.get()
        output_file = self.output_file.get()

        command = [
            "vcsi", input_file,
            "-t",
            "-w", str(width),
            "-g", grid,
            "--end-delay-percent", end_delay_percentage,
            "-o", output_file
        ]

        for command_entry, value_entry in self.command_entries:
            cmd = command_entry.get().strip()
            value = value_entry.get().strip()
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

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()