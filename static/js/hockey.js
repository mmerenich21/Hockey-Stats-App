function Hockey() {
    const that = this;

    this.updateGameResults = function (games) {
        $('#gameResults').empty();
        
        //set up the gameResults table
        const table = $('<table class="table" id="game-results"></tbody></table>');
        const header = $(`
                    <thead>
                    <tr>
                    <th>Team</th>
                    <th>Date</th>
                    <th>Opponent</th>
                    <th>Location</th>
                    <th>Goals Scored</th>
                    <th>Result</th>
                    </tr>
                    </thead>
                    <tbody>
                `);
        //add the table header to the table
        $(table).append(header);
        //built out the table rows from the database
        for (var row = 0; row < games.length; row++) {
            const game = games[row];
            const tr = $(`
                <tr>
                    <td>${game.team}</td>
                    <td>${game.date}</td>
                    <td>${game.opp}</td>
                    <td>${game.loc}</td>
                    <td>${game.goals}</td>
                    <td>${game.result}</td>
                </tr>
            `);
            //add the table rows to the table
            $(table).append(tr);
        }
       //Add the data into the gameResults table
        $('#gameResults').append(table);

        $('#game-results').DataTable( {
            //add ability for user to reorder columns
             colReorder: true,
             //add ability for table to be responsive
             responsive: true
          });

    }


    //load the server data for the tables
    this.load = function () {
        this.loadGameResults();
        this.loadStandings();
        this.loadStats();

        $('#teamDropDown').change(function () {
            that.loadGameResults();
        });

        $('#seasonDropDown').change(function () {
            that.loadGameResults();
           
        });

        $('#standingsSeasonDropDown').change(function () {
            that.loadStandings();
        });
        $('#statsSeasonDropDown').change(function () {
            that.loadStats();
        });

        $('#statsSplits').change(function () {
            that.loadStats();
        });

    }
    //Update the standings table
    this.updateStandings = function (standings) {
        $('#standings').empty();
        
        $('#standings').append(standings);

    }
   //Send user input data back to the database
    this.loadStandings = function () {
        $.post('/api/get_standings', {season: $("#standingsSeasonDropDown").val()}, function (data) {
            that.updateStandings(data.standings);
        });
    }
    //Send user input data back to the database
    this.loadGameResults = function () {
        $.post('/api/get_games', {team_id: $("#teamDropDown").val(), season: $("#seasonDropDown").val()}, function (data) {
            that.updateGameResults(data.games);
        });
    }
    //Update the stats table
    this.updateStats = function (stats) {
        $("#stats").empty();
        
        $("#stats").append(stats);
    }
    //Send user input data back to the database
    this.loadStats = function () {
        $.post('/api/get_stats', {season: $("#statsSeasonDropDown").val(), split: $("#statsSplits").val()}, function (data) {
            that.updateStats(data.stats);
        });
    }

}
