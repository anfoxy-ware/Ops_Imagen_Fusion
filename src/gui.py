"""
Módulo de la interfaz gráfica para Image Merger Tool - INTERFAZ COMPACTA
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
import threading

class ImageProcessor:
    """Clase completa de procesamiento de imágenes"""
    
    def __init__(self):
        self.supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]
    
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
    
    def create_thumbnail(self, image_path, size=(60, 45)):
        """Crear miniatura para preview"""
        try:
            image = Image.open(image_path)
            image.thumbnail(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            placeholder = Image.new('RGB', size, color='lightgray')
            return ImageTk.PhotoImage(placeholder)
    
    def combine_images_vertical(self, images, spacing=0, background_color="#FFFFFF"):
        """Combinar imágenes verticalmente"""
        if not images:
            raise ValueError("No hay imágenes para combinar")
        
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images) + (spacing * (len(images) - 1))
        
        if background_color.upper() == "TRANSPARENT":
            result = Image.new('RGBA', (max_width, total_height), (0, 0, 0, 0))
        else:
            result = Image.new('RGB', (max_width, total_height), background_color)
        
        y_offset = 0
        for img in images:
            x_offset = (max_width - img.width) // 2
            result.paste(img, (x_offset, y_offset))
            y_offset += img.height + spacing
        
        return result
    
    def combine_images_horizontal(self, images, spacing=0, background_color="#FFFFFF"):
        """Combinar imágenes horizontalmente"""
        if not images:
            raise ValueError("No hay imágenes para combinar")
        
        total_width = sum(img.width for img in images) + (spacing * (len(images) - 1))
        max_height = max(img.height for img in images)
        
        if background_color.upper() == "TRANSPARENT":
            result = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))
        else:
            result = Image.new('RGB', (total_width, max_height), background_color)
        
        x_offset = 0
        for img in images:
            y_offset = (max_height - img.height) // 2
            result.paste(img, (x_offset, y_offset))
            x_offset += img.width + spacing
        
        return result
    
    def combine_images_grid(self, images, spacing=0, background_color="#FFFFFF"):
        """Combinar imágenes en cuadrícula"""
        if not images:
            raise ValueError("No hay imágenes para combinar")
        
        cols = 2
        rows = (len(images) + cols - 1) // cols
        
        max_width = max(img.width for img in images)
        max_height = max(img.height for img in images)
        
        total_width = (max_width * cols) + (spacing * (cols - 1))
        total_height = (max_height * rows) + (spacing * (rows - 1))
        
        if background_color.upper() == "TRANSPARENT":
            result = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        else:
            result = Image.new('RGB', (total_width, total_height), background_color)
        
        for i, img in enumerate(images):
            row = i // cols
            col = i % cols
            
            x_offset = col * (max_width + spacing)
            y_offset = row * (max_height + spacing)
            
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

class MainWindow:
    """Ventana principal de la aplicación - INTERFAZ COMPACTA"""
    
    def __init__(self, root):
        self.root = root
        self.processor = ImageProcessor()
        self.image_paths = []
        self.thumbnails = []
        
        self.setup_ui()
        self.setup_styles()
    
    def setup_styles(self):
        """Configurar estilos visuales"""
        style = ttk.Style()
        style.configure("Modern.TFrame", background="white")
        style.configure("Title.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50")
        style.configure("Card.TFrame", relief="solid", borderwidth=1, background="white")
    
    def setup_ui(self):
        """Configurar la interfaz de usuario compacta"""
        self.root.title("🖼️ Ops Imagen-Fusion")
        self.root.geometry("700x690")
        self.root.minsize(500, 610)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10", style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # HEADER COMPACTO
        self.create_compact_header(main_frame)
        
        # CONTENEDOR PRINCIPAL CON 2 COLUMNAS
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # COLUMNA IZQUIERDA: Lista de imágenes
        left_column = ttk.Frame(content_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_image_section(left_column)
        
        # COLUMNA DERECHA: Opciones y controles
        right_column = ttk.Frame(content_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        
        self.create_controls_section(right_column)
        
        # FOOTER COMPACTO
        self.create_compact_footer(main_frame)
    
    def create_compact_header(self, parent):
        """Crear encabezado compacto"""
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        content = ttk.Frame(header_frame)
        content.pack(fill=tk.X, padx=10, pady=8)
        
        # Título e ícono
        title_frame = ttk.Frame(content)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        title_row = ttk.Frame(title_frame)
        title_row.pack(anchor="w")
        icon_label = ttk.Label(title_row)
        icon_label.pack(side=tk.LEFT)
        
        ttk.Label(title_row, font=("Arial", 16)).pack(side=tk.LEFT)
        ttk.Label(
            title_row,
            text="Ops Imagen-Fusion",
            style="Title.TLabel"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(
    
    text="Combinador de imágenes - Área de Operaciones",
    style="Subtitle.TLabel",
    font=("Arial", 10)
    ).pack(pady=(0, 15))
        
        # Contador
        self.counter_label = ttk.Label(
            content,
            text="0 imágenes",
            font=("Arial", 9, "bold"),
            foreground="#27ae60",
            background="#d5f4e6",
            relief="solid",
            borderwidth=1,
            padding=(10, 3)
        )
        self.counter_label.pack(side=tk.RIGHT)
    
    def create_image_section(self, parent):
        """Crear sección de imágenes (izquierda)"""
        # Botones de carga
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(
            button_frame,
            text="📂 Seleccionar Archivos",
            command=self.select_images,
            width=22
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="🔄 Carpeta",
            command=self.select_folder,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_frame,
            text="🗑️ Limpiar",
            command=self.clear_all,
            width=15
        ).pack(side=tk.RIGHT, padx=2)
        
        # Lista de imágenes con scroll
        list_frame = ttk.LabelFrame(parent, text=" 📋 Imágenes Cargadas ", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas con scroll
        self.canvas = tk.Canvas(list_frame, bg="white")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Modern.TFrame")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Estado vacío
        self.show_empty_state()
    
    def create_controls_section(self, parent):
        """Crear sección de controles (derecha)"""
        parent.config(width=350)
        
        # DISPOSICIÓN
        disp_frame = ttk.LabelFrame(parent, text=" ⚙️ Disposición ", padding="10")
        disp_frame.pack(fill=tk.X, pady=5)
        
        self.combination_mode = tk.StringVar(value="vertical")
        
        ttk.Radiobutton(
            disp_frame, text="⬇️ Vertical",
            variable=self.combination_mode, value="vertical"
        ).pack(anchor="w", pady=2)
        
        ttk.Radiobutton(
            disp_frame, text="➡️ Horizontal",
            variable=self.combination_mode, value="horizontal"
        ).pack(anchor="w", pady=2)
        
        ttk.Radiobutton(
            disp_frame, text="🔲 Cuadrícula",
            variable=self.combination_mode, value="grid"
        ).pack(anchor="w", pady=2)
        
        # ESPACIADO
        spacing_frame = ttk.LabelFrame(parent, text=" 📏 Espaciado ", padding="10")
        spacing_frame.pack(fill=tk.X, pady=5)
        
        spacing_control = ttk.Frame(spacing_frame)
        spacing_control.pack(fill=tk.X)
        
        self.spacing_var = tk.StringVar(value="0")
        self.spacing_scale = ttk.Scale(
            spacing_control,
            from_=0, to=100,
            variable=tk.DoubleVar(value=0),
            orient="horizontal",
            command=self.on_spacing_change
        )
        self.spacing_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.spacing_label = ttk.Label(spacing_control, text="0 px", width=5)
        self.spacing_label.pack(side=tk.RIGHT, padx=5)
        
        # FONDO
        bg_frame = ttk.LabelFrame(parent, text=" 🎨 Color de Fondo ", padding="10")
        bg_frame.pack(fill=tk.X, pady=5)
        
        self.bg_color = tk.StringVar(value="Blanco")
        bg_combo = ttk.Combobox(
            bg_frame,
            textvariable=self.bg_color,
            values=["Blanco", "Negro", "Transparente", "Gris claro"],
            state="readonly",
            width=18
        )
        bg_combo.pack(fill=tk.X)
        
        # FORMATO Y CALIDAD
        output_frame = ttk.LabelFrame(parent, text=" 💾 Formato de Salida ", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_format = tk.StringVar(value="PNG")
        
        format_row = ttk.Frame(output_frame)
        format_row.pack(fill=tk.X, pady=2)
        
        ttk.Radiobutton(
            format_row, text="PNG",
            variable=self.output_format, value="PNG"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            format_row, text="JPEG",
            variable=self.output_format, value="JPEG"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            format_row, text="WebP",
            variable=self.output_format, value="WebP"
        ).pack(side=tk.LEFT, padx=5)
        
        # Calidad
        ttk.Label(output_frame, text="Calidad:", font=("Arial", 9)).pack(anchor="w", pady=(8, 2))
        
        quality_control = ttk.Frame(output_frame)
        quality_control.pack(fill=tk.X)
        
        self.quality_var = tk.IntVar(value=95)
        ttk.Scale(
            quality_control,
            from_=10, to=100,
            variable=self.quality_var,
            orient="horizontal",
            command=self.on_quality_change
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.quality_label = ttk.Label(quality_control, text="95%", width=4)
        self.quality_label.pack(side=tk.RIGHT, padx=5)
        
        # OPCIONES ADICIONALES
        opts_frame = ttk.LabelFrame(parent, text=" 🔧 Opciones ", padding="10")
        opts_frame.pack(fill=tk.X, pady=5)
        
        self.compress_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            opts_frame, text="Comprimir imagen",
            variable=self.compress_var
        ).pack(anchor="w", pady=2)
        
        self.keep_meta_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            opts_frame, text="Mantener metadatos",
            variable=self.keep_meta_var
        ).pack(anchor="w", pady=2)
    
    def create_compact_footer(self, parent):
        """Crear pie de página compacto"""
        footer_frame = ttk.Frame(parent, style="Card.TFrame")
        footer_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Barra de progreso
        self.progress_frame = ttk.Frame(footer_frame)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="Procesando...",
            font=("Arial", 8)
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, pady=2)
        self.progress_frame.pack_forget()
        
        # Botón principal
        self.merge_button = ttk.Button(
            footer_frame,
            text="🚀 COMBINAR Y GUARDAR",
            command=self.merge_and_save
        )
        self.merge_button.pack(fill=tk.X, padx=10, pady=8)
    
    def show_empty_state(self):
        """Mostrar estado vacío"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        empty = ttk.Frame(self.scrollable_frame)
        empty.pack(fill=tk.BOTH, expand=True, pady=50)
        
        ttk.Label(
            empty,
            text="🎯",
            font=("Arial", 32),
            background="white"
        ).pack(pady=5)
        
        ttk.Label(
            empty,
            text="No hay imágenes cargadas",
            font=("Arial", 10, "bold"),
            foreground="#1900ff",
            background="white"
        ).pack()
        
        ttk.Label(
            empty,
            text="Usa los botones de arriba para agregar",
            font=("Arial", 8),
            foreground="#1900ff",
            background="white"
        ).pack()
    
    def on_spacing_change(self, value):
        """Manejar cambio en espaciado"""
        spacing = int(float(value))
        self.spacing_label.config(text=f"{spacing} px")
        self.spacing_var.set(str(spacing))
        self.update_info()
    
    def on_quality_change(self, value):
        """Manejar cambio en calidad"""
        quality = int(float(value))
        self.quality_label.config(text=f"{quality}%")
    
    def select_images(self):
        """Seleccionar imágenes"""
        file_types = [
            ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
            ("Todos los archivos", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=file_types
        )
        
        if files:
            self.add_images(files)
    
    def select_folder(self):
        """Seleccionar carpeta"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta")
        if folder:
            image_files = []
            for ext in self.processor.supported_formats:
                image_files.extend([
                    os.path.join(folder, f) for f in os.listdir(folder)
                    if f.lower().endswith(ext)
                ])
            
            if image_files:
                self.add_images(image_files)
            else:
                messagebox.showinfo("Información", "No se encontraron imágenes")
    
    def add_images(self, file_paths):
        """Agregar imágenes"""
        valid = [p for p in file_paths if self.processor.validate_image(p)]
        
        if not valid:
            messagebox.showerror("Error", "No se encontraron imágenes válidas")
            return
        
        self.image_paths.extend(valid)
        self.update_image_list()
        self.update_info()
    
    def update_image_list(self):
        """Actualizar lista de imágenes"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.image_paths:
            self.show_empty_state()
            self.counter_label.config(text="0 imágenes")
            return
        
        for i, path in enumerate(self.image_paths):
            self.create_image_item(path, i)
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.counter_label.config(text=f"{len(self.image_paths)} imágenes")
    
    def create_image_item(self, image_path, index):
        """Crear item de imagen compacto"""
        item = ttk.Frame(self.scrollable_frame, relief="solid", borderwidth=1)
        item.pack(fill=tk.X, pady=1, padx=2)
        
        # Miniatura
        thumb = self.processor.create_thumbnail(image_path)
        self.thumbnails.append(thumb)
        
        thumb_label = ttk.Label(item, image=thumb)
        thumb_label.pack(side=tk.LEFT, padx=3, pady=2)
        
        # Info
        info = ttk.Frame(item)
        info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        
        name = os.path.basename(image_path)
        if len(name) > 30:
            name = name[:27] + "..."
        
        ttk.Label(info, text=name, font=("Arial", 8, "bold")).pack(anchor="w")
        ttk.Label(info, text=f"#{index + 1}", font=("Arial", 7), foreground="#7f8c8d").pack(anchor="w")
        
        # Botones
        btn_frame = ttk.Frame(item)
        btn_frame.pack(side=tk.RIGHT, padx=2)
        
        ttk.Button(
            btn_frame, text="↑", width=2,
            command=lambda: self.move_image_up(index)
        ).pack(side=tk.LEFT, padx=1)
        
        ttk.Button(
            btn_frame, text="↓", width=2,
            command=lambda: self.move_image_down(index)
        ).pack(side=tk.LEFT, padx=1)
        
        ttk.Button(
            btn_frame, text="×", width=2,
            command=lambda: self.remove_image(index)
        ).pack(side=tk.LEFT, padx=1)
    
    def move_image_up(self, index):
        """Mover imagen arriba"""
        if index > 0:
            self.image_paths[index], self.image_paths[index-1] = \
                self.image_paths[index-1], self.image_paths[index]
            self.update_image_list()
            self.update_info()
    
    def move_image_down(self, index):
        """Mover imagen abajo"""
        if index < len(self.image_paths) - 1:
            self.image_paths[index], self.image_paths[index+1] = \
                self.image_paths[index+1], self.image_paths[index]
            self.update_image_list()
            self.update_info()
    
    def remove_image(self, index):
        """Eliminar imagen"""
        if 0 <= index < len(self.image_paths):
            self.image_paths.pop(index)
            self.update_image_list()
            self.update_info()
    
    def clear_all(self):
        """Limpiar todo"""
        if self.image_paths:
            self.image_paths.clear()
            self.thumbnails.clear()
            self.update_image_list()
            self.update_info()
    
    def update_info(self):
        """Actualizar información"""
        if not self.image_paths:
            self.info_label.config(text="Agrega imágenes\npara comenzar")
            return
        
        mode = self.combination_mode.get()
        count = len(self.image_paths)
        
        mode_text = {
            "vertical": "⬇️ Vertical",
            "horizontal": "➡️ Horizontal",
            "grid": "🔲 Cuadrícula"
        }
        
        info = f"Modo: {mode_text.get(mode, mode)}\n"
        info += f"Imágenes: {count}\n"
        info += f"Espaciado: {self.spacing_var.get()} px"
        
        self.info_label.config(text=info)
    
    def show_progress(self, show=True):
        """Mostrar/ocultar progreso"""
        if show:
            self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
            self.progress_bar.start()
            self.merge_button.config(state="disabled")
        else:
            self.progress_frame.pack_forget()
            self.progress_bar.stop()
            self.merge_button.config(state="normal")
    
    def merge_and_save(self):
        """Combinar y guardar"""
        if not self.image_paths:
            messagebox.showerror("Error", "No hay imágenes para combinar")
            return
        
        if len(self.image_paths) < 2:
            messagebox.showerror("Error", "Se necesitan al menos 2 imágenes")
            return
        
        try:
            mode = self.combination_mode.get()
            spacing = int(self.spacing_var.get())
            
            bg_map = {
                "Blanco": "white",
                "Negro": "black",
                "Transparente": "transparent",
                "Gris claro": "#f0f0f0"
            }
            background = bg_map.get(self.bg_color.get(), "white")
            
            output_format = self.output_format.get()
            quality = self.quality_var.get()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Configuración inválida: {str(e)}")
            return
        
        file_types = [
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("WebP", "*.webp")
        ]
        
        save_path = filedialog.asksaveasfilename(
            title="Guardar imagen combinada",
            defaultextension=".png",
            filetypes=file_types
        )
        
        if not save_path:
            return
        
        self.show_progress(True)
        self.progress_label.config(text="Procesando imágenes...")
        
        def process():
            try:
                images = []
                for i, path in enumerate(self.image_paths):
                    self.root.after(0, lambda i=i: self.progress_label.config(
                        text=f"Procesando {i+1}/{len(self.image_paths)}..."
                    ))
                    images.append(self.processor.open_image(path))
                
                self.root.after(0, lambda: self.progress_label.config(text="Combinando..."))
                
                if mode == "vertical":
                    result = self.processor.combine_images_vertical(images, spacing, background)
                elif mode == "horizontal":
                    result = self.processor.combine_images_horizontal(images, spacing, background)
                else:
                    result = self.processor.combine_images_grid(images, spacing, background)
                
                final_quality = max(40, quality - 30) if self.compress_var.get() else quality
                
                self.root.after(0, lambda: self.progress_label.config(text="Guardando..."))
                self.processor.save_image(result, save_path, output_format, final_quality)
                
                self.root.after(0, lambda: self.show_success(
                    output_format, quality, len(images), result.size, save_path
                ))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", f"Error al procesar:\n{str(e)}"
                ))
            finally:
                self.root.after(0, lambda: self.show_progress(False))
        
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def show_success(self, format, quality, count, size, path):
        """Mostrar mensaje de éxito"""
        msg = (
            f"✅ ¡Éxito!\n\n"
            f"Formato: {format}\n"
            f"Calidad: {quality}%\n"
            f"Imágenes: {count}\n"
            f"Tamaño: {size[0]} × {size[1]} px\n\n"
            f"Guardado en:\n{path}"
        )
        
        messagebox.showinfo("¡Completado!", msg)


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()