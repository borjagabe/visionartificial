import cv2
import numpy as np
import os

class ImageProcessor:
    """Clase para el procesamiento de imágenes con OpenCV."""

    def __init__(self):
        self.original_image = None  # La imagen original sin cambios
        self.current_image = None   # La imagen con los cambios aplicados

    def load(self, file_path):
        """Carga una imagen desde una ruta de archivo y guarda la original."""
        self.original_image = cv2.imread(file_path)
        if self.original_image is not None:
            self.current_image = self.original_image.copy()

    def save(self, file_path):
        """Guarda la imagen actual en una ruta de archivo."""
        if self.current_image is not None:
            cv2.imwrite(file_path, self.current_image)

    def detect_face(self):
        """Detecta rostros en la imagen usando haarcascades."""
        cascade_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.current_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    def rotate(self, angle):
        """Rota la imagen un ángulo especificado."""
        if self.current_image is not None:
            (h, w) = self.current_image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.current_image = cv2.warpAffine(self.current_image, M, (w, h))

    def change_brightness(self, value):
        """Ajusta el brillo de la imagen original."""
        if self.original_image is not None:
            hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = np.clip(v.astype(int) + value, 0, 255).astype(np.uint8)
            final_hsv = cv2.merge((h, s, v))
            self.current_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    def get_image(self):
        """Devuelve la imagen actual."""
        return self.current_image
    def change_contrast(self, value):
        """
        Ajusta el contraste de la imagen.
        :param value: Valor de contraste, donde 1.0 es el contraste original, 
                      valores menores a 1.0 reducen el contraste,
                      y valores mayores a 1.0 aumentan el contraste.
        """
        if self.original_image is not None:
            # Convertir la imagen a flotante para evitar problemas de desbordamiento o recorte
            f_image = self.original_image.astype(float)

            # Ajustar el contraste
            # La fórmula es: resultado = alfa * imagen + beta
            # donde 'alfa' es el factor de contraste y 'beta' es cero en este caso
            contrasted_image = cv2.multiply(f_image, np.array([value]))

            # Asegurarse de que los valores permanezcan en el rango correcto [0, 255]
            contrasted_image = np.clip(contrasted_image, 0, 255)

            # Convertir de vuelta a uint8
            self.current_image = contrasted_image.astype(np.uint8)
    def apply_changes(self):
        """Aplica los cambios a la imagen original."""
        print("Applying changes...")
        self.original_image = self.current_image.copy()