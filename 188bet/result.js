var fs = require('fs');
var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,
        userAgent: 'Googlebot'
    }
});

casper.start('http://sb.188bet.com/en-gb/info-centre/sportsbook-info/results');

casper.wait(10000, function(){
    fs.write('/root/project/OkChym/188bet/result.txt', this.getHTML(), 'w');
});

casper.run();
