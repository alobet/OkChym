var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,
        userAgent: 'Googlebot'
    }
});

casper.start('http://www.188bet.com/en-gb/sports/football/competition/correct-score?competitionids=27317');

casper.wait(5000, function(){
    fs.write('/root/project/OkChym/188bet/series_a_correctscore.txt', this.getHTML(), 'w');
});

casper.run();
