import os
from flask import Flask, g, json, jsonify, render_template, request
from db import Database
import pandas as pd
import numpy as np
import time

DATABASE_PATH = 'hockey.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(DATABASE_PATH)
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



def create_standings(data):
    combos = []
    for i in [[d['conf'], d['div']] for d in data]:
        if i not in combos:
            combos.append(i)
    cur_conf = combos[0][0]
    html = f"""<h1>{cur_conf}</h1>"""
    for c in combos:
        this_data = [d for d in data if d['conf'] == c[0] and d['div'] == c[1]]
        if this_data[0]['conf'] != cur_conf:
            cur_conf = this_data[0]['conf']
            html = html + f"""<h1>{cur_conf}</h1>"""
        html = html + f"""<h2>{c[1]}</h2><table class="table is-fullwidth">
                    <thead>
                    <tr>
                    <th>Team</th>
                    <th>W</th>
                    <th>L</th>
                    <th>OTL</th>
                    <th>Pts</th>
                    </tr>
                    </thead>"""
        for td in this_data:
            html = html + f"""
                <tr>
                <td>{td['team_name']}</td>
                    <td>{td['w']}</td>
                    <td>{td['l']}</td>
                    <td>{td['otl']}</td>
                    <td>{td['pts']}</td>
                </tr>
            """
        html = html + "</table>"
    return html



def stats(df, split):
    df = pd.DataFrame(df, columns=['gameid', 'teamname', 'Opponent', 'Location', 'goalsFirstPeriod', 'goalsSecondPeriod',
     'goalsThirdPeriod', 'goalsOvertime', 'goalsTotal', 'win', 'loss', 'otl', 'points', 'conference', 'division', 'season',
      'gamedate', 'oppConference', 'oppDivision', 'oppGoalsTotal'])
    df['gamesPlayed'] = 1
    if split == 'vs Division':
        df['Split'] = np.where(df['division'] == df['oppDivision'], 'Division', 'Non-Division')
        splits = ['Division', 'Non-Division']
    elif split == 'vs Conference':
        df['Split'] = np.where(df['conference'] == df['oppConference'], 'Conference', 'Non-Conference')
        splits = ['Conference', 'Non-Conference']
    elif split == 'Home vs Away':
        df['Split'] = np.where(df['Location'] == 'H', ' Home', 'Away')
        splits = ['Home', 'Away']
        
    
    res = df.groupby(['teamname', 'Split']).sum().reset_index()
    res['GoalsFor/Game'] = round(res['goalsTotal'] / res['gamesPlayed'],2)
    res['GoalsAgainst/Game'] = round(res['oppGoalsTotal'] / res['gamesPlayed'],2)
    res['Record'] = res['win'].astype(str) + '-' + res['loss'].astype(str) + '-' + res['otl'].astype(str)
    res = res[['teamname', 'Split', 'gamesPlayed', 'Record', 'points', 'GoalsFor/Game', 'GoalsAgainst/Game']]
    res.columns = ['Team', 'Split', 'Games', 'Record', 'Pts', 'GoalsFor/Game', 'GoalsAgainst/Game']
    res = res.set_index(['Team','Split']).unstack(level=-1).reset_index()
    res.columns = res.columns.swaplevel(0, 1)
    res.sort_index(axis=1, level=0, inplace=True)
    res = res.fillna("")

    html = f"""
            <table class="table" id="team-stats">
            <thead>
            <tr>
            <th> </th>
            <th colspan="5" style="text-align:center;border-right: 2px solid black;">{splits[0]}</th>
            <th colspan="5" style="text-align:center;">{splits[1]}</th>
            </tr>
            <tr>
            <th>Team</th>
            <th>Games</th>
            <th>GoalsAgainst/Game</th>
            <th>GoalsFor/Game</th>
            <th>Pts</th>
            <th style="border-right: 2px solid black;">Record</th>
            <th>Games</th>
            <th>GoalsAgainst/Game</th>
            <th>GoalsFor/Game</th>
            <th>Pts</th>
            <th>Record</th>
            </thead>
    """
    for d in res.itertuples():
        html = html + f"""
                <tr>
                <td>{d[1]}</td>
                <td>{d[2]}</td>
                <td>{d[3]}</td>
                <td>{d[4]}</td>
                <td>{d[5]}</td>
                <td style="border-right: 2px solid black;">{d[6]}</td>
                <td>{d[7]}</td>
                <td>{d[8]}</td>
                <td>{d[9]}</td>
                <td>{d[10]}</td>
                <td>{d[11]}</td>
                </tr>"""
    html = html + "</table> <script>$('#team-stats').DataTable( {responsive: true});</script>"
    return html
 

@app.route('/')
def home():
    return render_template('index.html', teams=get_db().get_teams(), seasons=get_db().get_seasons())
    


@app.route('/api/get_games', methods=['GET', 'POST'])
def api_get_games():
    team_id = request.form.get('team_id')
    season = request.form.get('season')
    return jsonify({
        'games': get_db().get_games(team_id, season)
    })


@app.route('/api/get_standings', methods=['GET', 'POST'])
def api_get_standings():
    season = request.form.get('season')
    return jsonify({
        'standings': create_standings(get_db().get_standings(season))
    })

@app.route('/api/get_stats', methods=['GET', 'POST'])
def api_get_stats():
    season = request.form.get('season')
    split = request.form.get('split')
    return jsonify({
        'stats': stats(get_db().get_stats(season), split)
    })

@app.route('/api/get_teams', methods=['GET'])
def api_get_teams():
    return jsonify({
        'teams': get_db().get_teams()
    })



if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
