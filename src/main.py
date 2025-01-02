import customtkinter as ctk
import subprocess

def select_input_files():
    files = ctk.filedialog.askopenfilenames(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
    if files:
        input_files_entry.delete(0, ctk.END)
        input_files_entry.insert(0, ";".join(files))

def select_output_folder():
    folder = ctk.filedialog.askdirectory()
    if folder:
        output_folder_entry.delete(0, ctk.END)
        output_folder_entry.insert(0, folder)

def select_color(target):
    color = ctk.colorchooser.askcolor()[1]  # Returns a tuple, second value is the hex color
    if color:
        target.set(color)

def generate_contact_sheet():
    input_files = input_files_entry.get()
    output_folder = output_folder_entry.get()
    grid = f"{rows_var.get()}x{cols_var.get()}"
    quality = quality_slider.get()
    bg_color = background_color.get()
    show_timestamps = show_timestamps_var.get()
    end_delay_percent = end_delay_percent_entry.get()

    if not input_files or not output_folder:
        ctk.messagebox.showerror("Error", "Debes seleccionar archivos de entrada y salida.")
        return

    # Generar el comando (esto es solo un ejemplo, necesitarás adaptarlo)
    command = f"vcsi -o {output_folder} -g {grid} --quality {quality} --background-color {bg_color} --end-delay-percent {end_delay_percent}"
    if show_timestamps:
        command += " --show-timestamp"

    ctk.messagebox.showinfo("Comando Generado", f"Comando: {command}")

def open_file_dialog():
    selected_file = ctk.filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
    if selected_file:
        input_files_entry.delete(0, ctk.END)
        input_files_entry.insert(0, selected_file)

def open_folder_dialog():
    selected_folder = ctk.filedialog.askdirectory()
    if selected_folder:
        output_folder_entry.delete(0, ctk.END)
        output_folder_entry.insert(0, selected_folder)

# Configurar CustomTkinter
ctk.set_appearance_mode("System")  # Opciones: "System" (respeta la configuración del sistema), "Light", "Dark"
ctk.set_default_color_theme("green")  # Opciones: "blue", "dark-blue", "green"

# Crear ventana principal
root = ctk.CTk()
root.title("Video Contact Sheet Generator")
root.geometry("600x500")

# Configurar grid weights para hacer la interfaz responsiva
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(8, weight=1)

# Selección de archivos de entrada
ctk.CTkLabel(root, text="Archivos de entrada:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
input_files_entry = ctk.CTkEntry(root, width=400)
input_files_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkButton(root, text="Open File", command=open_file_dialog).grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Selección de carpeta de salida
ctk.CTkLabel(root, text="Carpeta de salida:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
output_folder_entry = ctk.CTkEntry(root, width=400)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkButton(root, text="Seleccionar", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

# Configuración de cuadrícula
ctk.CTkLabel(root, text="Filas:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
rows_var = ctk.IntVar(value=4)
ctk.CTkComboBox(root, values=[str(i) for i in range(1, 11)], variable=rows_var).grid(row=2, column=1, padx=10, pady=10, sticky="ew")

ctk.CTkLabel(root, text="Columnas:").grid(row=3, column=0, sticky="w", padx=10, pady=10)
cols_var = ctk.IntVar(value=4)
ctk.CTkComboBox(root, values=[str(i) for i in range(1, 11)], variable=cols_var).grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Configuración de calidad
ctk.CTkLabel(root, text="Calidad:").grid(row=4, column=0, sticky="w", padx=10, pady=10)
quality_slider = ctk.CTkSlider(root, from_=0, to=100, number_of_steps=100)
quality_slider.set(100)
quality_slider.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# Color de fondo
ctk.CTkLabel(root, text="Color de fondo:").grid(row=5, column=0, sticky="w", padx=10, pady=10)
background_color = ctk.StringVar(value="#000000FF")
ctk.CTkEntry(root, textvariable=background_color).grid(row=5, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkButton(root, text="Seleccionar", command=lambda: select_color(background_color)).grid(row=5, column=2, padx=10, pady=10)

# Mostrar timestamps
show_timestamps_var = ctk.BooleanVar(value=True)
ctk.CTkCheckBox(root, text="Mostrar timestamps", variable=show_timestamps_var).grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# End delay percent
ctk.CTkLabel(root, text="End Delay Percent:").grid(row=7, column=0, sticky="w", padx=10, pady=10)
def sync_end_delay_percent(value):
    end_delay_percent_slider.set(int(value))
    end_delay_percent_entry.delete(0, ctk.END)
    end_delay_percent_entry.insert(0, str(int(value)))

end_delay_percent_var = ctk.IntVar(value=20)
end_delay_percent_slider = ctk.CTkSlider(root, from_=0, to=100, number_of_steps=100, variable=end_delay_percent_var, command=sync_end_delay_percent)
end_delay_percent_slider.grid(row=7, column=2, padx=10, pady=10, sticky="ew")

end_delay_percent_entry = ctk.CTkEntry(root, textvariable=end_delay_percent_var)
end_delay_percent_entry.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

# Botones
ctk.CTkButton(root, text="Generar", command=generate_contact_sheet).grid(row=8, column=0, padx=10, pady=20, sticky="w")
ctk.CTkButton(root, text="Salir", command=root.quit).grid(row=8, column=2, padx=10, pady=20, sticky="e")

root.mainloop()
