# main.py
from tkinter import Frame, Label, Menu, filedialog, Toplevel, Scale, HORIZONTAL, Button
from PIL import Image, ImageTk
from image_processing.image import ImageProcessor
import cv2

class MainWindow(Frame):
    """Ventana principal de la aplicación de procesamiento de imágenes."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.image_processor = ImageProcessor()
        self.image_label = Label(self)
        self.image_label.pack()
        self.brightness_window = None
        self.contrast_window = None
        self.init_window()

    def init_window(self):
        """Inicializa la ventana y sus componentes."""
        self.master.title("Image Processing App")
        self.pack(fill='both', expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        # Menú Archivo
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.load_image)
        file_menu.add_command(label="Save", command=self.save_image)

        # Menú Imagen
        image_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Image", menu=image_menu)
        image_menu.add_command(label="Rotate Right", command=lambda: self.rotate_image(-90))
        image_menu.add_command(label="Rotate Left", command=lambda: self.rotate_image(90))
        image_menu.add_command(label="Detect Face", command=self.detect_face)
        image_menu.add_command(label="Change Brightness", command=self.change_brightness)
        image_menu.add_command(label="Change Contrast", command=self.change_contrast)

    def load_image(self):
        """Carga una imagen desde un archivo."""
        print("Opening file dialog to load an image...")  # Depuración
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Loading image from {file_path}")  # Depuración
            self.image_processor.load(file_path)
            self.update_image()

    def save_image(self):
        """Guarda la imagen en un archivo."""
        print("Opening file dialog to save the image...")  # Depuración
        file_path = filedialog.asksaveasfilename()
        if file_path:
            print(f"Saving image to {file_path}")  # Depuración
            self.image_processor.save(file_path)

    def rotate_image(self, angle):
        """Rota la imagen."""
        print(f"Rotating image by {angle} degrees")  # Depuración
        self.image_processor.rotate(angle)
        self.update_image()
        self.image_processor.apply_changes()

    def detect_face(self):
        """Detecta rostros en la imagen."""
        print("Detecting faces...")  # Depuración
        self.image_processor.detect_face()
        self.update_image()
        self.image_processor.apply_changes() 

    def change_brightness(self):
        """Abre una ventana para ajustar el brillo de la imagen."""
        self.brightness_window = Toplevel(self.master)
        self.brightness_window.title("Change Brightness")

        # Inicializar el deslizador en 0, que representa el brillo actual de la imagen.
        brightness_slider = Scale(self.brightness_window, from_=-255, to=255, orient=HORIZONTAL)
        brightness_slider.set(0)
        brightness_slider.pack()

        # El evento 'set_brightness' se llama cuando el deslizador se suelta.
        brightness_slider.bind('<ButtonRelease-1>', self.set_brightness)
        self.brightness_window.protocol("WM_DELETE_WINDOW", self.on_brightness_window_close)

    def set_brightness(self, event):
        """Establece el brillo de la imagen cuando se suelta el deslizador."""
        brightness_value = int(event.widget.get())
        print(f"Setting brightness to: {brightness_value}")  # Imprimir valor para depuración
        self.image_processor.change_brightness(brightness_value)
        self.update_image()
    
    def change_contrast(self):
        """Abre una ventana para ajustar el contraste de la imagen."""
        self.contrast_window = Toplevel(self.master)
        self.contrast_window.title("Change Contrast")

        # Inicializar el deslizador. El valor 1.0 representa el contraste original.
        contrast_slider = Scale(self.contrast_window, from_=0.5, to=1.5, resolution=0.01, orient=HORIZONTAL)
        contrast_slider.set(1.0)  # Valor por defecto es 1.0 (sin cambio)
        contrast_slider.pack()

        # El evento 'set_contrast' se llama cuando el deslizador se suelta.
        contrast_slider.bind('<ButtonRelease-1>', self.set_contrast)
        contrast_slider.protocol("WM_DELETE_WINDOW", self.on_contrast_window_close)


    def set_contrast(self, event):
        """Establece el contraste de la imagen cuando se suelta el deslizador."""
        contrast_value = float(event.widget.get())
        print(f"Setting contrast to: {contrast_value}")  # Imprimir valor para depuración
        self.image_processor.change_contrast(contrast_value)
        self.update_image()

    def on_brightness_window_close(self):
        print("Window closed")
        self.image_processor.apply_changes()
        self.update_image()
        self.image_processor.apply_changes()
        self.brightness_window.destroy()

    def on_contrast_window_close(self):
        print("Window closed")
        self.image_processor.apply_changes()
        self.update_image()
        self.image_processor.apply_changes()
        self.contrast_window.destroy()

    def update_image(self):
        """Actualiza la imagen en la etiqueta de la GUI."""
        print("Updating image on GUI...")  # Depuración
        cv_image = self.image_processor.get_image()
        if cv_image is not None:
            try:
                # Intenta convertir la imagen y actualizar la GUI.
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv_image)
                tk_image = ImageTk.PhotoImage(pil_image)
                self.image_label.config(image=tk_image)
                self.image_label.image = tk_image
                print("Image updated successfully on the GUI.")  # Confirma que la imagen se actualizó.
            except Exception as e:
                print(f"Error updating image on the GUI: {e}")  # Imprime cualquier error que ocurra.

# Si este archivo es el script principal ejecutado, crea y lanza la ventana principal.
if __name__ == "__main__":
    root = Tk()
    root.title("Proyecto Visión Artificial")
    root.geometry("800x600")
    root.resizable(True, True)