"""
Configuración de la aplicación Fusion
"""

import os

# Configuración de la aplicación
APP_CONFIG = {
    "app_name": "Ops Imagen-Fusion",
    "version": "1.0.0",
    "window_size": "600x700",
    "min_window_size": "500x600",
    "icon_path": "assets/icons/app_icon.ico",
    
    # Formatos de imagen soportados
    "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"],
    
    # Configuración por defecto
    "default_output_format": "PNG",
    "default_quality": 90,
    "default_spacing": 0,
    "default_background": "#FFFFFF",
    
    # Colores de la interfaz
    "colors": {
        "primary": "#3B82F6",      # Azul
        "secondary": "#6B7280",    # Gris
        "success": "#10B981",      # Verde
        "danger": "#EF4444",       # Rojo
        "warning": "#F59E0B",      # Amarillo
        "background": "#F8FAFC",   # Gris claro
    }
}

# Rutas de la aplicación
def get_base_path():
    """Obtener la ruta base del proyecto"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_asset_path(filename):
    """Obtener ruta completa de un asset"""
    return os.path.join(get_base_path(), "assets", filename)