import sqlite3

def create_db():
    '''
    Brief:
    Esta función crea una base de datos SQLite llamada "db_score.db" con una tabla llamada "player" que tiene tres columnas: id, name y total_score.

    Parametros:
    No tiene parámetros.

    Retorno: 
    No retorna ningún valor.
    '''
    with sqlite3.connect("models/db_score.db") as conection:
        try:
            query = '''create table player
                            (
                                id integer primary key autoincrement,
                                name text,
                                total_score integer
                            )
                        '''
            conection.execute(query)
            print("Se creo la db")
        except sqlite3.OperationalError:
            print("La db ya existe")

def insert_row_into_db(name,total_score):
    '''
    Brief:
    Esta función inserta una fila en la tabla "player" de la base de datos "db_score.db" con los valores proporcionados para el nombre (name) y la puntuación total (total_score).

    Parametros:
    - name: Nombre del jugador a insertar en la base de datos.
    - total_score: Puntuación total del jugador a insertar en la base de datos.

    Retorno: 
    No retorna ningún valor.
    '''
    with sqlite3.connect("models/db_score.db") as conection:
        try:
            conection.execute("insert into player (name, total_score) values (?,?)", (name,total_score))
            conection.commit()
            print("Se creo la fila correctamente")
        except Exception as e:
            print(f"Error al insertar datos en la db {e}")

def get_player_id(player_name):
    '''
    Brief:
    Esta función busca en la tabla "player" de la base de datos "db_score.db" el ID del jugador cuyo nombre coincida con el proporcionado.

    Parametros:
    - player_name: Nombre del jugador del cual se quiere obtener el ID.

    Retorno: 
    El ID del jugador si se encuentra, o None si no se encuentra.

    '''
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "SELECT id FROM player WHERE name = ?"
            result = connection.execute(query, (player_name,))
            row = result.fetchone()

            if row:
                return row[0]
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el player_id: {e}")

def update_row_in_db(player_id, new_total_score):
    '''
    Brief:
    Esta función actualiza la puntuación total (total_score) de un jugador en la base de datos "db_score.db" mediante la identificación del jugador por su ID.

    Parametros:
    - player_id: ID del jugador cuya puntuación total se va a actualizar.
    - new_total_score: Nueva puntuación total que se asignará al jugador.

    Retorno: 
    No retorna ningún valor.
    '''
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "UPDATE player SET total_score = ? WHERE id = ?"
            connection.execute(query, (new_total_score, player_id))

            connection.commit()
            print(new_total_score)
            print(type(new_total_score))
            print(f"Datos actualizados para el jugador con ID {player_id}")
        except Exception as e:
            print(f"Error al actualizar datos en la db: {e}")

def get_top_3_players():
    '''
    Brief:
    Esta función obtiene los nombres y puntuaciones totales de los tres mejores jugadores de la base de datos "db_score.db", ordenados de mayor a menor puntuación.

    Parametros:
    No tiene parámetros.

    Retorno: 
    Una lista de tuplas que contiene los nombres y puntuaciones totales de los tres mejores jugadores.

    '''
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "SELECT name, total_score FROM player ORDER BY total_score DESC LIMIT 3"
            result = connection.execute(query)

            
            return result.fetchall()
        except Exception as e:
            print(f"Error al obtener los mejores jugadores: {e}")

def exist_name_in_db(name):
    '''
    Brief:
    Esta función verifica si un nombre de jugador ya existe en la base de datos "db_score.db".

    Parametros:
    - name: Nombre de jugador que se desea verificar.

    Retorno: 
    True si el nombre existe en la base de datos, False en caso contrario.
    '''
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "SELECT COUNT(*) FROM player WHERE name = ?"
            result = connection.execute(query, (name,))

            count = result.fetchone()[0]

            return count > 0
        except Exception as e:
            print(f"Error al verificar la existencia del nombre en la db: {e}")
            return False 

def obtain_score_with_id(player_id):
    '''    
    Brief:
    Esta función obtiene la puntuación total de un jugador mediante su ID en la base de datos "db_score.db".

    Parametros:
    - player_id: ID del jugador del cual se desea obtener la puntuación total.

    Retorno: 
    La puntuación total del jugador si se encuentra, o None si no se encuentra.
    '''
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "SELECT total_score FROM player WHERE id = ?"
            result = connection.execute(query, (player_id,))
            score = result.fetchone()

            if score is not None:
                return score[0]
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el puntaje por ID en la db: {e}")
            return None