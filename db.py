import sqlite3

class Database:

    def __init__(self, path):
        self.conn = sqlite3.connect(path)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()


    
    def get_games(self, team, season):
        data = self.select("""
        select teams.teamname, games.gamedate, case when teams.teamname = games.hometeam then games.awayteam else games.hometeam end as opponent,
        case when teams.teamname = games.hometeam then 'Home' else 'Away' end as location, gr.goalsTotal as GoalsScored,
        case when gr.win = 1 then 'W' else 'L' end as result
        from game_results gr
        join games on games.gameid = gr.gameid
        join teams on teams.teamid = gr.teamid
        where teams.teamid = ? and games.gamedate < date() and games.season = ?
        order by games.gamedate asc""", [team, season])
        return [{
            'team': d[0],
            'date': d[1],
            'opp': d[2],
            'loc': d[3],
            'goals': d[4],
            'result': d[5]
        } for d in data]


    def get_standings(self, season):
        data = self.select("""
        select gr.teamid, teams.teamname, sum(gr.win) as W, sum(gr.loss) as L, sum(gr.otl) as OTL, sum(gr.points) as Pts, teams.division, teams.conference  from game_results gr
        join teams on teams.teamid = gr.teamid
        join games on games.gameid = gr.gameid
        where games.season = ?
        group by gr.teamid, teams.teamname, teams.division, teams.conference
        order by teams.conference asc, teams.division asc, sum(gr.points) desc, sum(gr.loss) asc
        """, [season])
        return [{
            'team_id': d[0],
            'team_name': d[1],
            'w': d[2],
            'l': d[3],
            'otl': d[4],
            'pts': d[5],
            'div': d[6],
            'conf': d[7]
        } for d in data]

    def get_teams(self):
        data = self.select(
            'SELECT * FROM teams')
        return [{
            'id': d[0],
            'name': d[1],
            'division': d[2],
            'conference': d[3]
        } for d in data]

    def get_seasons(self):
        data = self.select(
            'SELECT distinct season from games')
        return [{
            'season': d[0]
        } for d in data]

    def get_stats(self, season):
        data = self.select("""
        with base as (
        select games.gameid,
            gr.teamid,
            teams.teamname,
            CASE 
            when teams.teamname = games.hometeam then games.AwayTeam 
            else games.HomeTeam 
            end as Opponent,
            CASE 
            when teams.teamname = games.hometeam then 'H' else 'A' end as Location,
            gr.goalsFirstPeriod,
            gr.goalsSecondPeriod,
            gr.goalsThirdPeriod,
            gr.goalsOvertime,
            gr.goalsTotal,
            gr.win,
            gr.loss,
            gr.otl,
            gr.points,
            teams.conference,
            teams.division,
            games.season,
            games.gamedate
        from game_results gr
        join games on games.gameid = gr.GameID 
        join teams on teams.teamid = gr.TeamID)
        select base.gameid,
            base.teamname,
            base.opponent,
            base.location,
            base.goalsFirstPeriod,
            base.goalsSecondPeriod,
            base.goalsThirdPeriod,
            base.goalsOvertime,
            base.goalsTotal,
            base.win,
            base.loss,
            base.otl,
            base.points,
            base.conference,
            base.division,
            base.season,
            base.gamedate,
            teams.conference as oppConference,
            teams.division as oppDivision,
            gr.goalsTotal as oppGoalsTotal
        from base
        join teams on teams.teamname = base.opponent
        join game_results gr on gr.gameid = base.gameid and gr.teamid = teams.teamid
        where base.season = ? and base.gamedate <= date()
        """, [season])
        return data


    def close(self):
        self.conn.close()
