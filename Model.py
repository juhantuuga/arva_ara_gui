# Määrab ära, mis juhtub kui mäng toimub
import sqlite3
from datetime import datetime
from random import randint
from Score import Score


class Model:
    def __init__(self):
        self.__database = "scoreboard.db"  # Andmebaasi fail kettal
        self.__table = "scoreboard"  # Tabeli nimi andmebaasis
        # Mänguga seotud muutujad:
        self.__pc_nr = randint(1, 100)
        self.__steps = 0
        self.__game_over = False
        self.__cheater = False
        self.__name = None
        print(f'Loodi mudel, arvuti mõtles numbri {self.__pc_nr}')  # TEST

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
        self.__pc_nr = randint(1, 100)
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
            # elif user_input == self.__pc_nr:
            else:
                self.__game_over = True
                return f"\nJuhuu, ära arvasid! Õige number oli {self.__pc_nr} ja arvasid ära {self.__steps} sammuga.\n"
        elif user_input == "backdoor":
            self.__steps += 1
            self.__cheater = True
            return f"Leidsid tagaukse. Arvutinumber on {self.__pc_nr}."
        else:
            self.__steps += 1
            return f'Tühi käik. +1 sammu. Tahame numbrit, sina sisestasid : "{user_input}" '

    def add_or_not_database(self):
        connection = None
        if self.__name:
            try:
                connection = sqlite3.connect(self.__database)
                today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # INSERT INTO scoreboard (name, steps, pc_nr, cheater, date_time)
                # VALUES ('Marko', 10, 87, 1, '2024-02-02 03:59:59')
                sql = 'INSERT INTO ' + self.__table + ' (name, steps, pc_nr, cheater, date_time) VALUES (?, ?, ?, ?, ?)'
                connection.execute(sql, (self.__name, self.__steps, self.__pc_nr, self.__cheater, today))
                connection.commit()  # Salvestab andmebaasi
            except sqlite3.Error as error:
                print(f'Viga ühendusega andmebaasiga {self.__database}. {error}')
            finally:  # Lõpuks alati tee see osa:
                if connection:
                    connection.close()  # Sulge ühendus

    def read_from_table(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM ' + self.__table + ' ORDER BY steps, name, date_time DESC;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()

            result = []
            for row in data:
                # NB! row[0] on id, mida ei soovi
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))
            return result

        except sqlite3.Error as error:
            print(f'Viga ühendusega andmebaasiga {self.__database}. {error}')
        finally:
            if connection:
                connection.close()
