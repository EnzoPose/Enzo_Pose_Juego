#Clase encargada de contener las variables que necesito ir moviendo entre los forms y los niveles 
#La clase fue creada con la finalidad de no utilizar variables globales
class Values:
    def __init__(self) -> None:
        self.music_volume = 0
        self.sound_volume = 0.2
        
        self.player_name = ""
        self.current_level = ""

        self.is_paused = False
        self.in_level = False
        self.reset_level = False


        self.player_score = {}


        self.menu_music = "assets\img\Sounds\menu_music.mp3"
        
    def create_player_score_dict(self):
        self.player_score ={
            self.player_name: {
                "Stage_1": 0,
                "Stage_2": 0,
                "Stage_3": 0
            }
        }

    def obtain_total_score(self):
        total_score = 0
        for stage,score in self.player_score[self.player_name].items():
            total_score += score
        return total_score
