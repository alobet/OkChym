var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages: false,
        userAgent: 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    },
    verbose: true
});

casper.start('http://www.188bet.com/en-gb/sports/football/competition/correct-score?competitionids=27166');

casper.then(function(){
    /*
    if (this.exists('a#text_ddlOFmt')){
        this.echo('chym');
        //this.echo(this.getHTML());
        //this.sendKeys('#txtNameMask', 'alobet');
        //this.sendKeys('#txtPassMask', 'P@$$vv0rd:', {keepFocus: true});
    }*/
    this.waitForSelector(".period", function(){
        //casper.capture('chym.png');
        this.echo('TOP NAV');
        //casper.capture('chym.png');
        fs.write('/root/project/OkChym/188bet/abc.txt', this.getHTML(), 'w');
    }, 10000);
});

casper.run();
