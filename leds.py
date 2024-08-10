import tkinter as tk
from PIL import Image, ImageTk # type: ignore
import serial

class HomeLightingApp:
    def __init__(self, root):

        self.serial_connection = serial.Serial('COM3', 9600)

        self.root = root
        self.root.title("Control de Focos de la Casa")

        self.foco_size = (50, 50) 

        self.lights = {
            "Cocina": False,
            "Sala": False,
            "Cochera": False,
            "Baño": False
        }

        self.room_buttons = {}

        self.color_on = "green"
        self.color_off = "red"

        self.background_image = Image.open("casa.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.foco_apagado_image = Image.open("foco_apagado.png").resize(self.foco_size)
        self.foco_apagado_photo = ImageTk.PhotoImage(self.foco_apagado_image)
        self.foco_encendido_image = Image.open("foco_encendido.png").resize(self.foco_size)
        self.foco_encendido_photo = ImageTk.PhotoImage(self.foco_encendido_image)

        self.canvas = tk.Canvas(root, width=self.background_photo.width(), height=self.background_photo.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        self.draw_lights()

        self.create_buttons()

    def send_command(self, command):

        if self.serial_connection.is_open:
            self.serial_connection.write(command.encode())
        else:
            print("La conexión serial no está abierta.")    

    def draw_lights(self):
        self.canvas.delete("foco")  
        positions = {
            "Cocina": (725, 400),
            "Sala": (600, 400),
            "Cochera": (700, 100),
            "Baño": (500, 160)
        }
        for room, (x, y) in positions.items():
            image = self.foco_encendido_photo if self.lights[room] else self.foco_apagado_photo
            self.canvas.create_image(x, y, anchor="center", image=image, tags=("foco", room))
            self.canvas.create_text(x, y+40, text=room, font=('Helvetica', 12, 'bold'), fill="white", tags=("foco", room))
            self.canvas.tag_bind(room, "<Button-1>", lambda event, r=room: self.toggle_light(r))

    def create_buttons(self):
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        for room in self.lights:
            color = self.color_on if self.lights[room] else self.color_off
            button_text = f"{room} {'ON' if self.lights[room] else 'OFF'}"
            button = tk.Button(self.button_frame, text=button_text, width=10, command=lambda r=room: self.toggle_light(r), fg=color)
            button.pack(side="left", padx=10)
            self.room_buttons[room] = button

        self.button_all = tk.Button(self.button_frame, text="Todos", width=10, command=self.toggle_all_lights)
        self.button_all.pack(side="left", padx=10)

        button_exit = tk.Button(self.button_frame, text="Salir", width=10, command=self.root.destroy)
        button_exit.pack(side="left", padx=10)
        
    def send_command(self, command):
        if self.serial_connection.is_open:
            self.serial_connection.write(command.encode())
        else:
            print("La conexión serial no está abierta.")


    def toggle_light(self, room):
        self.lights[room] = not self.lights[room]  
        self.draw_lights()

        if room in self.room_buttons:
            color = self.color_on if self.lights[room] else self.color_off
            self.room_buttons[room].config(text=f"{room} {'ON' if self.lights[room] else 'OFF'}", fg=color)

        commands = {
            "Cocina": 'C' if self.lights["Cocina"] else 'c',
            "Sala": 'S' if self.lights["Sala"] else 's',
            "Cochera": 'O' if self.lights["Cochera"] else 'o',
            "Baño": 'B' if self.lights["Baño"] else 'b'
         }
        self.send_command(commands[room])

    def toggle_all_lights(self):
        all_on = all(self.lights.values())
        new_state = not all_on

        for room in self.lights:
            self.lights[room] = new_state

        self.draw_lights()

        for room in self.room_buttons:
            color = self.color_on if self.lights[room] else self.color_off
            self.room_buttons[room].config(text=f"{room} {'ON' if self.lights[room] else 'OFF'}", fg=color)

        if new_state:
            self.button_all.config(text="Todos ON", fg=self.color_on)
            commands = 'C'
        else:
            self.button_all.config(text="Todos OFF", fg=self.color_off)
            commands = 'c'

        self.send_command(commands)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeLightingApp(root)
    root.mainloop()
