var casper = require('casper').create();
var fs = require('fs');

casper.start('http://www.188bet.com/en-gb/sports/football/competition/correct-score?competitionids=27166', function() {
    this.echo(this.getHTML());
    fs.write('/root/project/OkChym/javascript.txt', this.getHTML(), 'w');
});


casper.run();
