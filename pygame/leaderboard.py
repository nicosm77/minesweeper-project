import pandas as pd
import sqlite3

class Leaderboard():
    def __init__(self):
        self.leaderboard_db = sqlite3.connect("leaderboard_db.sqlite")
        cmd = 'CREATE TABLE IF NOT EXISTS leaderboard (boardsize int, time float, name text(20))'
        cursor = self.leaderboard_db.cursor()
        cursor.execute(cmd)
    
    def add_score(self, boardsize, time, name):
            db = self.leaderboard_db
            cursor = db.cursor()
            cmd = \
            f"""
            INSERT INTO leaderboard
            VALUES ({boardsize}, {time}, "{name}");
            """
            cursor.execute(cmd)
            db.commit()

    def get_leaderboard(self):
            cmd = \
            f"""
            SELECT * FROM leaderboard ORDER BY boardsize, time;
            """
            with self.leaderboard_db as conn:
                leaderboard = pd.read_sql_query(cmd, conn)
            return leaderboard