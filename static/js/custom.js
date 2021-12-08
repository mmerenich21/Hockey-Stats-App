//control the tab elements of the navigation
function tabbing(evt, tabName) {
  var i, x, tablinks;
  x = document.getElementsByClassName("tabContent");
  for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" is-active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " is-active";
}
//end tab code


/*All of this code is either for items that did not make it into the final version of the app or was only for testing purposes

//display the correct fields for Game Results form based on the radio selection
function teamDate() {
  if (document.getElementById('team-choice').checked) {
      document.getElementById('teamSection').style.display = 'block';
      document.getElementById('dateSection').style.display = 'none';
     // document.getElementById('teamDateSubmission').style.display = 'block';
  } else {
    document.getElementById('teamSection').style.display = 'none';
   // document.getElementById('resultsTeamName').value = '';
    document.getElementById('dateSection').style.display = 'block';
    //document.getElementById('teamDateSubmission').style.display = 'block';
  }
}

//Create a constant of all NHL team names for error checking
const teamNames = ['tampa bay lightning','lightning','florida panthers','panthers','carolina hurricanes',
'hurricanes','chicago blackhawks','blackhawks','columbus blue jackets','blue jackets','nashville predators',
'predators','dallas stars','stars','detroit red wings','red wings','new york islanders','islanders',
'washington capitals','capitals','boston bruins','bruins','philadelphia flyers','flyers','pittsburgh penguins',
'penguins','new york rangers','rangers','new jersey devils','devils','buffalo sabres','sabres','toronto maple leafs',
'maple leafs','winnipeg jets','jets','montreal canadiens','canadiens','edmonton oilers','oilers','calgary flames',
'flames','vancouver canucks','canucks','ottawa senators','senators','vegas golden knights','golden knights',
'st. louis blues','st louis blues','blues','colorado avalanche','avalanche','minnesota wild','wild','arizona coyotes',
'coyotes','los angeles kings','kings','anaheim ducks','ducks','san jose sharks','sharks']

//get the input values from the Game Results by team
function teamGameResults() {
  //turn input values into variables
  var team = document.getElementById('resultsTeamName').value;
  var resultsSeason = document.getElementById('teamGameResultsSeason').value;
  //make user input letter case not matter for matching data
  var teamLowerCase = team.toLowerCase();

//check if the entered team name matches an actual team
//input transformed to lowercase to make case not matter for the user
  if (teamNames.includes(teamLowerCase)) {
    console.log(team); 
    console.log(resultsSeason)
    //clear error message since there's a valid result
    document.getElementById("teamError").innerHTML = '';
  } else {
    //display error message
    document.getElementById("teamError").innerHTML = 'Please enter a valid team name'; 
  }
} 
//end teamGameResults
  
//get user input for game results by date
function dateGameResults() {
  //turn input values into variables
  //var startDate = new Date(document.getElementById('resultsStartDate').value);
  //var endDate = new Date(document.getElementById('resultsEndDate').value);
  var startDate = document.getElementById('resultsStartDate').value;
  var endDate = document.getElementById('resultsEndDate').value;

  //determine if the user date input is a valid format
  var dateRegex = /^(0?[1-9]|1[0-2])\/(0?[1-9]|1\d|2\d|3[01])\/(20)\d{2}$/;
  
 
  if (!dateRegex.test(startDate) ||!dateRegex.test(endDate) ) {
    document.getElementById("dateError").innerHTML = 'Please enter a valid date in the DD/MM/YYYY format'; 
 } else {
    document.getElementById("dateError").innerHTML = '';
    console.log('Start date: ' + startDate);
    console.log('End date: ' + endDate);
    //console.log(startDate.getTime());
 }
 
}

//get input valuees from the Team Standings question
function teamStandings() {
  console.log(document.getElementById('teamStandingsSeason').value);
}

//get input valuees from the Team stats question
function teamStats() {
  console.log(document.getElementById('teamStats').value);
}

//get input valuees from the Team stats question
function playerStats() {
  console.log(document.getElementById('playerStats').value);
}
*/