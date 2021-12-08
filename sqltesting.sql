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
where base.season = '2020-2021' and base.gamedate <= date()
