import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style, ttk
import subprocess

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Video Processing Application")

        self.style = Style(theme="darkly")
        self.style.configure("TLabel", padding=6, font=("Helvetica", 12), background="#2c2c2c", foreground="#ffffff")
        self.style.configure("TButton", padding=6, font=("Helvetica", 12), bootstyle="success-outline")
        self.style.configure("TEntry", padding=6, font=("Helvetica", 12), fieldbackground="#2c2c2c", foreground="#ffffff")
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), foreground="#ffffff", background="#2c2c2c")
        self.style.configure("TFrame", background="#2c2c2c")

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid to be responsive
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Title Label
        title_label = ttk.Label(main_frame, text="Video Processing Application", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Input File
        ttk.Label(main_frame, text="Input File:").grid(row=1, column=0, sticky="W")
        self.input_file = ttk.Entry(main_frame, width=50)
        self.input_file.grid(row=1, column=1, padx=5, pady=5, sticky="EW")
        self.browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_file, bootstyle="success-outline")
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        # Width
        ttk.Label(main_frame, text="Width:").grid(row=2, column=0, sticky="W")
        self.width_var = tk.IntVar(value=1500)
        self.width_scale = ttk.Scale(main_frame, from_=500, to=2000, orient=tk.HORIZONTAL, variable=self.width_var, command=self.update_width_entry)
        self.width_scale.grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        self.width_entry = ttk.Entry(main_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=2, column=2, padx=5, pady=5, sticky="EW")

        # Grid
        ttk.Label(main_frame, text="Grid:").grid(row=3, column=0, sticky="W")
        self.grid = ttk.Entry(main_frame, width=10)
        self.grid.insert(0, "4x4")
        self.grid.grid(row=3, column=1, padx=5, pady=5, sticky="EW")

        # End Delay Percentage
        ttk.Label(main_frame, text="End Delay Percentage:").grid(row=4, column=0, sticky="W")
        self.end_delay_percentage = ttk.Entry(main_frame)
        self.end_delay_percentage.insert(0, "20")
        self.end_delay_percentage.grid(row=4, column=1, padx=5, pady=5, sticky="EW")

        # Output File
        ttk.Label(main_frame, text="Output File:").grid(row=5, column=0, sticky="W")
        self.output_file = ttk.Entry(main_frame)
        self.output_file.insert(0, "output.png")
        self.output_file.grid(row=5, column=1, padx=5, pady=5, sticky="EW")

        # Run Button
        self.run_button = ttk.Button(main_frame, text="Run", command=self.run_vcsi, bootstyle="success-outline")
        self.run_button.grid(row=6, column=0, columnspan=3, pady=20)

    def update_width_entry(self, event):
        self.width_var.set(int(self.width_scale.get()))

    def browse_file(self):
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.input_file.delete(0, 'end')
            self.input_file.insert(0, filename)

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

        subprocess.run(command)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()