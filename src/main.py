#!/usr/bin/env python3
"""
Image Merger Tool - Aplicación principal
"""

import tkinter as tk
from gui import MainWindow

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Configurar la ventana principal
        root.title("Ops Imagen-Fusion")
        root.geometry("600x700")
        root.resizable(True, True)
        
        # Inicializar la interfaz gráfica
        app = MainWindow(root)
        
        print("✅ Aplicación iniciada correctamente")
        
        # Iniciar el loop principal
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()