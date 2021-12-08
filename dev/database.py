import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_teams(conn, team):
    """
    Create a new team into the teams table
    :param conn:
    :param teams:
    :return:
    """
    sql = ''' INSERT INTO teams(TeamID,TeamName,Conference,Division)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, team)
    conn.commit()
    return cur.lastrowid


def create_games(conn, game):
    """
    Create a new game
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO games(GameID,GameDate,HomeTeam,AwayTeam,Season)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, game)
    conn.commit()
    return cur.lastrowid

def create_results(conn, result):
    """
    Create a new game
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO game_results(GameID,TeamID,goalsFirstPeriod,goalsSecondPeriod,
    goalsThirdPeriod,goalsOvertime,goalsTotal,win,loss,otl,points)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, result)
    conn.commit()
    return cur.lastrowid

def main():
    database = "/Users/kmf229/Documents/Drexel/INFO-606/FinalProject/myCode/hockey.db"
    
    
    sql_create_teams_table = """ CREATE TABLE IF NOT EXISTS teams (
                                        TeamID text PRIMARY KEY,
                                        TeamName text NOT NULL,
                                        Conference text NOT NULL,
                                        Division text NOT NULL
                                    ); """

    sql_create_games_table = """CREATE TABLE IF NOT EXISTS games (
                                    GameID text PRIMARY KEY,
                                    GameDate date NOT NULL,
                                    HomeTeam text NOT NULL,
                                    AwayTeam text NOT NULL,
                                    Season integer NOT NULL
                                );"""

    sql_create_results_table = """CREATE TABLE IF NOT EXISTS game_results (
                                    GameID text NOT NULL,
                                    TeamID text NOT NULL,
                                    goalsFirstPeriod integer,
                                    goalsSecondPeriod integer,
                                    goalsThirdPeriod integer,
                                    goalsOvertime integer,
                                    goalsTotal integer,
                                    win integer,
                                    loss integer,
                                    otl integer,
                                    points integer,
                                    PRIMARY KEY (GameID,TeamID)
                                    FOREIGN KEY (GameID) REFERENCES games (GameID)
                                    FOREIGN KEY (TeamID) REFERENCES teams (TeamID)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create teams table
        create_table(conn, sql_create_teams_table)

        # create games table
        create_table(conn, sql_create_games_table)
        
        # create games resulst table
        create_table(conn, sql_create_results_table)
        
    else:
        print("Error! cannot create the database connection.")
    
    with conn:
        #Insert teams csv
        team = pd.read_csv('nhl_teams.csv')
        for row in team.values.tolist():
            create_teams(conn, row)

        # insert games csv
        game = pd.read_csv('nhl_games.csv')
        for gm in game.values.tolist():
            create_games(conn, gm)
        
        #create game stats
        stats = pd.read_csv('nhl_gamestats.csv')
        for stat in stats.values.tolist():
            create_results(conn, stat)


if __name__ == '__main__':
    main()