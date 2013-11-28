var casper = require('casper').create();
var fs = require('fs');

casper.start('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=26726', function() {
    this.echo(this.getHTML());
    fs.write('/root/project/OkChym/handicap_premierleague.txt', this.getHTML(), 'w');
});


casper.run();
