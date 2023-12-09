from gui.main_window import MainWindow
from tkinter import Tk
def main():
    root = Tk()
    root.title("Proyecto Visión Artificial")
    root.geometry("800x600")
    root.resizable(True, True)  # Permitir redimensionar la ventana

    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()