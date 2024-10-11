import tkinter as tk
from tkinter import Label, Entry
from PIL import Image, ImageTk  # Para trabajar con imágenes
from dfa_vending_machine import vm_dfa

# Diccionario de productos con imágenes y precios
products_list = {
    '0000': {'nombre': 'Monster', 'precio': 5000, 'img': './img/monster.jpg'},
    '0001': {'nombre': 'RedBull', 'precio': 5000, 'img': './img/reddbull.jpg'},
    '0010': {'nombre': 'Cola & Pola', 'precio': 3500, 'img': './img/cola-y-pola.jpg'},
    '0011': {'nombre': 'Four Loco', 'precio': 6000, 'img': './img/four-loco.png'},
    '0100': {'nombre': 'Vive 100', 'precio': 3500, 'img': './img/vive100.jpg'},
    '0101': {'nombre': '7up', 'precio': 3000, 'img': './img/7up.jpg'},
    '0110': {'nombre': 'Colombiana', 'precio': 3000, 'img': './img/colombiana.jpg'},
    '0111': {'nombre': 'Sprite', 'precio': 3000, 'img': './img/sprite.jpg'},
    '1000': {'nombre': 'Jugo Hit', 'precio': 3500, 'img': './img/jugo-hit.jpg'},
    '1001': {'nombre': 'Agua Cielo', 'precio': 2000, 'img': './img/agua.jpg'},
    '1010': {'nombre': 'Gatorade', 'precio': 4000, 'img': './img/gatorade.jpg'},
    '1011': {'nombre': 'Speed', 'precio': 3500, 'img': './img/speed.jpg'},
    '1110': {'nombre': 'Coca cola', 'precio': 3500, 'img': './img/coca-cola.jpg'},
}

img_vending_machine = './img/Vending_machine2.jpg'

class VendingMachine:
    def __init__(self):
        self.saldo = 0
        self.lista_productos = products_list
        self.root_img_vending_machine = img_vending_machine  # Ruta a la imagen de la máquina expendedora

    def show_window(self):
        self.window = tk.Tk()
        self.window.title('Máquina Expendedora')

        # Costado izquierdo (imagen de la máquina y producto comprado)
        left_frame = tk.Frame(self.window)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Mostrar la imagen de la máquina expendedora
        self.show_vending_machine_image(left_frame)

        self.img_producto = tk.Label(left_frame, text="")  # Recuadro para mostrar la imagen del producto
        self.img_producto.pack(pady=10)

        # Costado derecho (saldo, valor de monedas, instrucciones)
        right_frame = tk.Frame(self.window)
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        self.label_saldo = tk.Label(right_frame, text=f"Saldo: ${self.saldo}")
        self.label_saldo.pack(pady=10)

        self.label_monedas = tk.Label(right_frame, text="Monedas: 0=$500, 1=$1000")
        self.label_monedas.pack(pady=10)

        self.label_instrucciones = tk.Label(right_frame, text="Ingrese monedas o el código del producto:\n(Enter)\nIngrese solo el monto del producto.\n La maquina no da cambio.")
        self.label_instrucciones.pack(pady=10)

        self.input_entry = Entry(right_frame)
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.process_input)

        # Label dinámico para mostrar mensajes de error o saldo insuficiente
        self.label_dinamico = tk.Label(right_frame, text="", fg="red")
        self.label_dinamico.pack(pady=10)

        self.window.mainloop()

    def show_vending_machine_image(self, frame):
        """Función para mostrar la imagen de la máquina expendedora en el frame izquierdo."""
        try:
            image = Image.open(self.root_img_vending_machine)
            image = image.resize((300, 500))  # Ajustar el tamaño según sea necesario
            photo = ImageTk.PhotoImage(image)
            self.img_maquina = tk.Label(frame, image=photo)
            self.img_maquina.image = photo  # Guardar referencia de la imagen para evitar que se borre
            self.img_maquina.pack(pady=10)
        except Exception as e:
            self.img_maquina = tk.Label(frame, text=f"Error al cargar imagen: {e}")
            self.img_maquina.pack(pady=10)

    def process_input(self, event):
        entrada = self.input_entry.get()
        print(vm_dfa.accepts(entrada))

        # Procesar entrada de monedas
        if entrada == "0":
            self.saldo += 500
            self.label_dinamico.config(text="")  # Limpiar mensaje de error
        elif entrada == "1":
            self.saldo += 1000
            self.label_dinamico.config(text="")  # Limpiar mensaje de error
        elif entrada in self.lista_productos:
            self.buy_product(entrada)
        else:
            # Si el string no es reconocido por el autómata
            self.label_dinamico.config(text="El string no pertenece al autómata")

        self.update_saldo()

    def update_saldo(self):
        self.label_saldo.config(text=f"Saldo: ${self.saldo}")

    def buy_product(self, codigo):
        producto = self.lista_productos.get(codigo)
        if producto:
            if self.saldo >= producto['precio']:
                self.saldo -= producto['precio']
                # Cargar y mostrar la imagen del producto
                self.show_product_image(producto['img'])
                self.label_dinamico.config(text=f"Compraste: {producto['nombre']}")
                self.update_saldo()
            else:
                # Mostrar mensaje de saldo insuficiente
                self.label_dinamico.config(text="Saldo insuficiente\n El string pertenece al automata.")

    def show_product_image(self, img_path):
        """Función para mostrar la imagen del producto comprado en el recuadro."""
        try:
            image = Image.open(img_path)
            image = image.resize((150, 150))  # Redimensionar la imagen si es necesario
            photo = ImageTk.PhotoImage(image)
            self.img_producto.config(image=photo)
            self.img_producto.image = photo  # Guardar referencia a la imagen
        except Exception as e:
            self.label_dinamico.config(text=f"Error al cargar la imagen: {e}")
