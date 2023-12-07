#Clase encargada de contener las variables que necesito ir moviendo entre los forms y los niveles 
#La clase fue creada con la finalidad de no utilizar variables globales
class Values:
    def __init__(self) -> None:
        self.music_volume = 0.1
        self.sound_volume = 0.2
        
        self.player_name = ""
        self.current_level = ""

        self.is_paused = False
        self.in_level = False
        self.reset_level = False


        self.player_score = {}


        self.menu_music = "assets\img\Sounds\menu_music.mp3"
        
    def create_player_score_dict(self,score = 0):
        '''
        Brief:
        Este método de clase crea un diccionario para almacenar la puntuación de un jugador en diferentes etapas del juego, así como su puntuación total.

        Parametros:
        - score: Puntuación inicial del jugador (por defecto, 0).

        Retorno: 
        No retorna ningún valor.

        '''
        self.player_score ={
            self.player_name: {
                "Stage_1": 0,
                "Stage_2": 0,
                "Stage_3": 0,
                "Total_score": score
            }
        }

    def obtain_total_score(self):
        '''
        Brief:
        Este método de clase calcula y devuelve la puntuación total de un jugador sumando las puntuaciones de las diferentes etapas del juego.

        Parametros:
        No tiene parámetros.

        Retorno: 
        La puntuación total del jugador.
        '''
        total_score = self.player_score[self.player_name]["Stage_1"] + self.player_score[self.player_name]["Stage_2"] + self.player_score[self.player_name]["Stage_3"]
        self.player_score[self.player_name]["Total_score"] = total_score
        return total_score
    
    def set_value_in_score_dict(self, score):
        '''
        Brief:
        Este método de clase actualiza la puntuación de un jugador en la etapa actual del juego si la puntuación proporcionada es mayor que la existente.

        Parametros:
        - score: Nueva puntuación a establecer en la etapa actual del juego.

        Retorno: 
        No retorna ningún valor.
        '''
        if self.player_score[self.player_name][self.current_level] < score:
            self.player_score[self.player_name][self.current_level] = score
