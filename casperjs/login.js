var links = [];
var casper = require('casper').create();
casper.start('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=26726', function(){
    this.fillSelectors('form',{
    'input[name="txtNameMask"]': 'alobet',
    'input[name="txtPassMask"]': 'P@$$vv0rd:'}, true);
});

casper.run();
