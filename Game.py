from Controller import Controller


class Game:
    def __init__(self):
        game = Controller()
        game.view.main()  # Teeb põhiakna nähtavaks


if __name__ == "__main__":  # Googelda ise, raibe!
    Game()

