import sqlite3

def create_db():
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
    with sqlite3.connect("models/db_score.db") as conection:
        try:
            conection.execute("insert into player (name, total_score) values (?,?)", (name,total_score))
            conection.commit()
            print("Se creo la fila correctamente")
        except Exception as e:
            print(f"Error al insertar datos en la db {e}")

def get_player_id(player_name):
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
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "UPDATE player SET total_score = ? WHERE id = ?"
            connection.execute(query, (new_total_score, player_id))

            connection.commit()
            print(f"Datos actualizados para el jugador con ID {player_id}")
        except Exception as e:
            print(f"Error al actualizar datos en la db: {e}")

def get_top_3_players():
    with sqlite3.connect("models/db_score.db") as connection:
        try:
            query = "SELECT name, total_score FROM player ORDER BY total_score DESC LIMIT 3"
            result = connection.execute(query)

            
            return result.fetchall()
        except Exception as e:
            print(f"Error al obtener los mejores jugadores: {e}")