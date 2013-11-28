var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,
        userAgent: 'Googlebot'
    }
});

casper.start('http://sb.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=26726');

casper.wait(5000, function(){
    fs.write('/root/project/OkChym/188bet/premier_league.txt', this.getHTML(), 'w');
});

casper.run();
