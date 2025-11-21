"""
Módulo para procesamiento y combinación de imágenes
"""

from PIL import Image
import os
from config import APP_CONFIG

class ImageProcessor:
    """Clase para manejar el procesamiento de imágenes"""
    
    def __init__(self):
        self.supported_formats = APP_CONFIG["supported_formats"]
    
    def validate_image(self, file_path):
        """Validar si un archivo es una imagen soportada"""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            return ext in self.supported_formats
        except:
            return False
    
    def open_image(self, file_path):
        """Abrir una imagen y convertir a RGB"""
        try:
            image = Image.open(file_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            raise Exception(f"Error al abrir la imagen {file_path}: {str(e)}")
    
    def combine_images_vertical(self, images, spacing=0, background_color="#FFFFFF"):
        """Combinar imágenes verticalmente"""
        if not images:
            raise ValueError("No hay imágenes para combinar")
        
        # Calcular dimensiones totales
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images) + (spacing * (len(images) - 1))
        
        # Crear imagen resultante
        if background_color.upper() == "TRANSPARENT":
            result = Image.new('RGBA', (max_width, total_height), (0, 0, 0, 0))
        else:
            result = Image.new('RGB', (max_width, total_height), background_color)
        
        # Pegar imágenes
        y_offset = 0
        for img in images:
            x_offset = (max_width - img.width) // 2  # Centrar horizontalmente
            result.paste(img, (x_offset, y_offset))
            y_offset += img.height + spacing
        
        return result
    
    def combine_images_horizontal(self, images, spacing=0, background_color="#FFFFFF"):
        """Combinar imágenes horizontalmente"""
        if not images:
            raise ValueError("No hay imágenes para combinar")
        
        # Calcular dimensiones totales
        total_width = sum(img.width for img in images) + (spacing * (len(images) - 1))
        max_height = max(img.height for img in images)
        
        # Crear imagen resultante
        if background_color.upper() == "TRANSPARENT":
            result = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))
        else:
            result = Image.new('RGB', (total_width, max_height), background_color)
        
        # Pegar imágenes
        x_offset = 0
        for img in images:
            y_offset = (max_height - img.height) // 2  # Centrar verticalmente
            result.paste(img, (x_offset, y_offset))
            x_offset += img.width + spacing
        
        return result
    
    def combine_images_grid(self, images, spacing=0, background_color="#FFFFFF"):
        """Combinar imágenes en cuadrícula (2 columnas)"""
        if not images:
            raise ValueError("No hay imágenes para combinar")
        
        # Calcular dimensiones de la cuadrícula
        cols = 2
        rows = (len(images) + cols - 1) // cols
        
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        
        total_width = (max_width * cols) + (spacing * (cols - 1))
        total_height = (max_height * rows) + (spacing * (rows - 1))
        
        # Crear imagen resultante
        if background_color.upper() == "TRANSPARENT":
            result = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        else:
            result = Image.new('RGB', (total_width, total_height), background_color)
        
        # Pegar imágenes en cuadrícula
        for i, img in enumerate(images):
            row = i // cols
            col = i % cols
            
            x_offset = col * (max_width + spacing)
            y_offset = row * (max_height + spacing)
            
            # Centrar la imagen en su celda
            x_center = x_offset + (max_width - img.width) // 2
            y_center = y_offset + (max_height - img.height) // 2
            
            result.paste(img, (x_center, y_center))
        
        return result
    
    def save_image(self, image, file_path, format="PNG", quality=95):
        """Guardar imagen en el formato especificado"""
        try:
            if format.upper() == "PNG" and image.mode == 'RGBA':
                image.save(file_path, format.upper(), compress_level=9)
            else:
                image.save(file_path, format.upper(), quality=quality)
            return True
        except Exception as e:
            raise Exception(f"Error al guardar la imagen: {str(e)}")
    
    def get_image_info(self, file_path):
        """Obtener información básica de una imagen"""
        try:
            with Image.open(file_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'size_kb': os.path.getsize(file_path) // 1024
                }
        except:
            return None