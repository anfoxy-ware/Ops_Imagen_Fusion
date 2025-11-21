"""
Funciones utilitarias para la aplicación
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from config import APP_CONFIG

def select_files(parent):
    """Abrir diálogo para seleccionar archivos"""
    file_types = [
        ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff"),
        ("Todos los archivos", "*.*")
    ]
    
    files = filedialog.askopenfilenames(
        parent=parent,
        title="Seleccionar imágenes",
        filetypes=file_types
    )
    
    return list(files)

def select_save_location(parent, default_format="PNG"):
    """Abrir diálogo para guardar archivo"""
    file_types = [
        ("PNG", "*.png"),
        ("JPEG", "*.jpg"),
        ("WebP", "*.webp"),
        ("Todos los archivos", "*.*")
    ]
    
    # Encontrar el formato por defecto
    default_ext = next((ext for name, ext in file_types if default_format.upper() in name), "*.png")
    
    file_path = filedialog.asksaveasfilename(
        parent=parent,
        title="Guardar imagen combinada",
        defaultextension=default_ext.replace("*", ""),
        filetypes=file_types
    )
    
    return file_path

def show_error(parent, message):
    """Mostrar mensaje de error"""
    messagebox.showerror("Error", message, parent=parent)

def show_info(parent, message):
    """Mostrar mensaje informativo"""
    messagebox.showinfo("Información", message, parent=parent)

def show_warning(parent, message):
    """Mostrar mensaje de advertencia"""
    messagebox.showwarning("Advertencia", message, parent=parent)

def validate_file_path(file_path):
    """Validar si la ruta de archivo es válida"""
    if not file_path:
        return False
    
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            return True
        except:
            return False
    
    return True

def format_file_size(size_bytes):
    """Formatear tamaño de archivo en formato legible"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_unique_filename(file_path):
    """Obtener un nombre de archivo único si ya existe"""
    if not os.path.exists(file_path):
        return file_path
    
    base, ext = os.path.splitext(file_path)
    counter = 1
    
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1