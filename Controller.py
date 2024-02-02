# Käivitab nupud õigel ajal, et saaks mängida.
from tkinter import simpledialog
from Model import Model
from View import View


class Controller:
    def __init__(self):
        self.model = Model()  # Self laseb meil neid muutujaid kasutada globaalselt. Kui selfi ei kasuta, siis ei saa.
        self.view = View(self)  # Anname viewle selle sama kontolleri kaasa

    def new_game_click(self):
        self.model.start_new_game()
        self.view.btn_new_game["state"] = "disabled"  # Ei saa klikkida
        self.view.num_entry["state"] = "normal"  # Saab sisestada
        self.view.btn_send["state"] = "normal"  # Saab klikkida
        #self.view.num_entry

    def send_click(self, event=None):
        input = self.model.get_user_input(self.view.num_entry.get().strip())
        # input on tekst, mida näidata kasutajale
        self.view.num_entry.delete(0, "end")  # Tühjendab sisestuskasti
        self.view.text_box.config(state="normal")  # Tekstikasti saab kirjutada
        self.view.text_box.insert("insert", input + "\n")  # Kirjuta tulemus kasti
        self.view.text_box.see("end")  # Aken liigub tulemusega kaasa
        self.view.text_box.config(state="disabled")  # Tekstikasti ei saa kirjutada
        if self.model.game_over:
            self.view.btn_new_game["state"] = "normal"  # Saab klikkida
            self.view.num_entry["state"] = "disabled"
            self.view.btn_send["state"] = "disabled"
            if not self.model.cheater:  # Kui ei ole cheater, siis
                self.ask_name()  # küsi mängija nime
                self.model.add_or_not_database()  # Lisa mängija edetabelisse (database table)

    def ask_name(self):
        name = simpledialog.askstring("Nimi", "Kuidas on sinu nimi?")
        self.model.name = name

    def scoreboard_click(self):
        frame = self.view.create_popup_window()
        data = self.model.read_from_table()
        self.view.generate_scoreboard(frame, data)
