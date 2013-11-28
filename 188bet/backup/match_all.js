var casper = require('casper').create({
    pageSettings: {
            verbose: true,
            logLevel: 'debug',
            loadImages:  false,
            userAgent: 'Googlebot'
        }
});

var fs = require('fs');
casper.start('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=26726');

casper.wait(5000, function(){
    fs.write('/root/project/OkChym/188bet/premier_league.txt', this.getHTML(), 'w');
});
casper.thenOpen('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=27166', function() {
    casper.on('load.finished', function(status){
        if('success' === status) {
            fs.write('/root/project/OkChym/188bet/champion_league.txt', this.getHTML(), 'w');
        }
    });
});

casper.thenOpen('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=27317', function() {
    casper.on('load.finished', function(status){
        if('success' === status) {
            fs.write('/root/project/OkChym/188bet/series_a.txt', this.getHTML(), 'w');
        }
    });
});

casper.thenOpen('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=27068', function() {
    casper.on('load.finished', function(status){
        if('success' === status) {
            fs.write('/root/project/OkChym/188bet/spain.txt', this.getHTML(), 'w');
        }
    });
});

casper.thenOpen('http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=28301', function() {
    casper.on('load.finished', function(status){
        if('success' === status) {
            fs.write('/root/project/OkChym/188bet/europa_league.txt', this.getHTML(), 'w');
        }
    });
});

casper.run();
