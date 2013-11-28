var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,
        userAgent: 'Googlebot'
    }
});

casper.start('http://sb.188bet.com/en-gb/sports/football/competition/correct-score?competitionids=27166');

casper.wait(5000, function(){
    fs.write('/root/project/OkChym/188bet/champion_league_correctscore.txt', this.getHTML(), 'w');
});

casper.run();
