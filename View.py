# Kogu akende vaade, milline välja näeb
from datetime import datetime
from time import strptime
from tkinter import *
from tkinter import simpledialog, messagebox
import tkinter.font as font
from tkinter.tix import AUTO
from tkinter.ttk import Treeview


class View(Tk):
    def __init__(self, controller):
        super().__init__()  # Tk jaoks
        self.controller = controller
        self.__width = 600
        self.__height = 500
        self.default_font = font.Font(family="Verdana", size=14)  # Vidinate kirjastiil
        self.default_text_font = font.Font(family="Verdana", size=12)  # Vidinate kirjastiil

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

        # "Enter" klahvivajutus ja kas klikiti X nuppu
        self.bind('<Return>', self.controller.send_click)
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Klikk close

    def main(self):
        self.mainloop()

    def center_window(self, width, height):
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_top_frame(self):
        frame = Frame(self, bg="#D1EEEC", height=15)
        frame.pack(expand=True, fill=BOTH)
        return frame

    def create_bottom_frame(self):
        frame = Frame(self, bg="#D1EEEC")
        frame.pack(expand=True, fill=BOTH)
        return frame

    def create_frame_widgets(self):
        # Nupp Uus mäng
        btn_new_game = Button(self.top_frame, text="Uus mäng", bg="#bee0ec",
                              font=self.default_font, foreground="#2596be", border=0,
                              command=self.controller.new_game_click)  # () ei tohi olla lõpus
        btn_new_game.grid(row=0, column=0, padx=16, sticky="ew")

        # Tekst sisesta number
        lbl_info = Label(self.top_frame, text="Sisesta number", font=self.default_font, bg="#D1EEEC", border=0)
        lbl_info.grid(row=1, column=0, padx=16, pady=16)

        # Numbrisisestus lahter
        num_entry = Entry(self.top_frame, font=self.default_font, state=DISABLED, border=0)
        num_entry.grid(row=1, column=1, padx=16, pady=16)
        num_entry.focus()

        # Nupp sisesta
        btn_send = Button(self.top_frame, border=0, bg="#bee0ec", text="Sisesta", font=self.default_font, state=DISABLED,
                          command=self.controller.send_click)
        btn_send.grid(row=1, column=2, padx=16, pady=16, sticky=EW)

        # Tekstikast koos kerimisribaga
        text_box = Text(self.bottom_frame, font=self.default_text_font, state=DISABLED, border=0, padx=16, pady=16)
        scrollbar = Scrollbar(self.bottom_frame, orient=VERTICAL)
        scrollbar.config(command=text_box.yview)
        text_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_box.pack(expand=True, fill=BOTH, padx=16, pady=16)

        # Edetabeli nupp
        btn_scoreboard = Button(self.top_frame, bg="#bee0ec", border=0, text="Edetabel", font=self.default_font,
                                command=lambda: self.controller.scoreboard_click())
        btn_scoreboard.grid(row=0, column=2, padx=16, pady=16)
        return btn_new_game, num_entry, btn_send, text_box, btn_scoreboard

    def create_popup_window(self):
        top = Toplevel(self)
        top.title('Edetabel')
        top_width = 600
        top_height = 150
        x = (top.winfo_screenwidth() // 2) - (top_width // 2)
        y = (top.winfo_screenheight() // 2) - (top_height // 2)
        top.geometry(f"{top_width}x{top_height}+{x}+{y}")

        top.resizable(False, False)  # Ärme lase akna suurust muuta
        top.grab_set()  # Modal ei saa klikkida mängu põhiaknal
        top.focus()  # Fookus top aknale

        frame = Frame(top)  # Frame luuakse top aknale
        frame.pack(fill=BOTH, expand=True)

        return frame

    def generate_scoreboard(self, frame, data):
        my_table = Treeview(frame)

        # Paneme Scrollbari tööle:
        vsb = Scrollbar(frame, orient=VERTICAL, command=my_table.yview)  # Vertical Scroll Bar
        vsb.pack(side=RIGHT, fill=Y)
        my_table.configure(yscrollcommand=vsb.set)

        my_table['columns'] = ('name', 'steps', 'pc_nr', 'cheater', 'date_time')

        # Tabeli veeru seaded. Esimene veerg on peidetud #0
        my_table.column('#0', width=0, stretch=NO)
        my_table.column('name', anchor=W, width=200)
        my_table.column('steps', anchor=W, width=20)
        my_table.column('pc_nr', anchor=W, width=20)
        my_table.column('cheater', anchor=W, width=20)
        my_table.column('date_time', anchor=W, width=80)

        # Tabeli päis (heading)
        my_table.heading('#0', text='', anchor=W)
        my_table.heading('name', text='Nimi', anchor=W)
        my_table.heading('steps', text='Sammud', anchor=W)
        my_table.heading('pc_nr', text='PC Number', anchor=W)
        my_table.heading('cheater', text='Pettur', anchor=W)
        my_table.heading('date_time', text='Kuupäev', anchor=W)

        # Tabeli täitmine andmetega:
        x = 0
        for player in data:
            if player.cheater:
                cheater = "Jah"
            else:
                cheater = "Ei"

            date_time = datetime.strptime(player.date_time, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y - %H:%M:%S')
            my_table.insert(parent='', index='end', iid=x,
                            values=(player.name, player.steps, player.pc_nr, cheater, date_time))
            x += 1

        my_table.pack(fill=BOTH, expand=True)

    def on_close(self):
        if messagebox.askokcancel('Välju mängust', 'Kas soovid tõesti mängust väljuda?'):
            self.destroy()
