from tkinter import *
from tkinter import simpledialog, messagebox
import tkinter.font as font
from tkinter.ttk import Treeview


class View(Tk):
    def __init__(self, controller):
        super().__init__()  # Tk jaoks
        self.controller = controller
        self.__width = 550
        self.__height = 500
        self.default_font = font.Font(family="Verdana", size=14)  # Vidinate kirjastiil

        # Aknaomadused
        self.title("Arva ära mäng")
        self.center_window(self.__width, self.__height)

        # Loome kaks Frame'i
        self.top_frame = self.create_top_frame()
        self.bottom_frame = self.create_bottom_frame()

        # Widgets
        (self.btn_new_game,
         self.num_entry,
         self.btn_send,
         self.text_box,
         self.btn_scoreboard) = self.create_frame_widgets()

    def main(self):
        self.mainloop()


    def center_window(self, width, height):
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


    def create_top_frame(self):
        frame = Frame(self, bg="LIGHTBLUE", height=15)
        frame.pack(expand=True, fill=BOTH)
        return frame


    def create_bottom_frame(self):
        frame = Frame(self, bg="LIGHTYELLOW")
        frame.pack(expand=True, fill=BOTH)
        return frame


    def create_frame_widgets(self):
        # Nupp Uus mäng
        btn_new_game = Button(self.top_frame, text="Uus mäng",
                              font=self.default_font, command=self.controller.new_game_click)  # () ei tohi olla lõpus
        btn_new_game.grid(row=0, column=0, padx=5, sticky="ew")
        # Tekst sisesta number
        lbl_info = Label(self.top_frame, text="Sisesta number", font=self.default_font)
        lbl_info.grid(row=1, column=0, padx=5, pady=5)
        # Numbrisisestus lahter
        num_entry = Entry(self.top_frame, font=self.default_font, state=DISABLED)
        num_entry.grid(row=1, column=1, padx=5, pady=5)
        num_entry.focus()
        # Nupp sisesta
        btn_send = Button(self.top_frame, text="Sisesta", font=self.default_font, state=DISABLED, command=self.controller.send_click)
        btn_send.grid(row=1, column=2, padx=5, pady=5, sticky=EW)
        # Tekstikast koos kerimisribaga
        text_box = Text(self.bottom_frame, font=self.default_font, state=DISABLED)  # Et ei saaks ise teksti muuta
        scrollbar = Scrollbar(self.bottom_frame, orient=VERTICAL)
        scrollbar.config(command=text_box.yview)
        text_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_box.pack(expand=True, fill=BOTH, padx=5, pady=5)
        # Edetabeli nupp
        btn_scoreboard = Button(self.top_frame, text="Edetabel", font=self.default_font)
        btn_scoreboard.grid(row=0, column=2, padx=5, pady=5)
        return btn_new_game, num_entry, btn_send, text_box, btn_scoreboard
