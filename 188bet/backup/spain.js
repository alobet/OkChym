var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,
        userAgent: 'Googlebot'
    }
});

casper.start('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=27068');

casper.wait(5000, function(){
    fs.write('/root/project/OkChym/188bet/spain.txt', this.getHTML(), 'w');
});

casper.run();
