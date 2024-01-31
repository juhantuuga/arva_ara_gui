from random import randint


class Model:
    def __init__(self):
        self.__database = "scoreboard.db"  # Andmebaasi fail kettal
        self.__table = "scoreboard.db"  # Tabeli nimi andmebaasis
        # Mänguga seotud muutujad:
        self.__pc_nr = randint(1,100)
        self.__steps = 0
        self.__game_over = False
        self.__cheater = False
        self.__name = None
        print(f"Loodi mudel, arvuti mõtles numbri {self.__pc_nr}")  # TEST

    # GETTER JAANI, et muutuja väärtusi kätte saada
    @property
    def pc_nr(self):
        return self.__pc_nr

    @property
    def steps(self):
        return self.__steps

    @property
    def game_over(self):
        return self.__game_over

    @property
    def cheater(self):
        return self.__cheater

    @property
    def name(self):
        return self.__name

    # SETTER JAANI
    @name.setter
    def name(self, value):
        if value:  # Kui on nimi, siis
            self.__name = value  # omista uus väärtus nimele

    @staticmethod
    def is_number(user_input):
        try:
            int(user_input)
            return True
        except ValueError:
            return False

    def start_new_game(self):
        self.__pc_nr = randint(1,100)
        self.__steps = 0
        self.__game_over = False
        self.__cheater = False
        self.__name = None


    def get_user_input(self, user_input):
        # Mida sisaldab muutuja user_input ehk kasutaja sisestus
        if self.is_number(user_input):
            user_input = int(user_input)
            self.__steps += 1
            if user_input > self.__pc_nr:
                return f"Väiksem kui {user_input}"
            elif user_input < self.__pc_nr:
                return f"Suurem kui {user_input}"
            #elif user_input == self.__pc_nr:
            else:
                self.__game_over = True
                return f"Juhuu, ära arvasid! Õige number oli {self.__pc_nr} ja arvasid ära {self.__steps} sammuga."
        elif user_input == "backdoor":
            self.__steps += 1
            self.__cheater = True
            return f"Leidsid tagaukse, õige number on {self.__pc_nr}, pettur."
        else:
            self.__steps += 1
            return f'Tühi käik. +1 sammu. Tahame numbrit, sina sisestasid : "{user_input}" '