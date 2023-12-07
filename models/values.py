#Clase encargada de contener las variables que necesito ir moviendo entre los forms y los niveles 
#La clase fue creada con la finalidad de no utilizar variables globales
class Values:
    def __init__(self) -> None:
        self.music_volume = 0
        self.sound_volume = 0.2
        self.player_score = 0


        self.is_paused = False
        self.in_level = False
        self.reset_level = False

        self.lost = False
        self.win = False
        self.current_level = ""

        self.menu_music = "assets\img\Sounds\menu_music.mp3"
        