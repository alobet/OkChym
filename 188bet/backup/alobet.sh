#!/bin/bash
export PHANTOMJS_EXECUTABLE="/usr/local/bin/phantomjs"
/usr/local/bin/casperjs /root/project/OkChym/188bet/champion_league.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/champion_league_1half.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/champion_league_correctscore.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/premier_league.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/premier_league_1half.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/premier_league_correctscore.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/series_a.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/series_a_1half.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/series_a_correctscore.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/spain.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/spain_1half.js
/usr/local/bin/casperjs /root/project/OkChym/188bet/spain_correctscore.js
/root/project/OkChym/188bet/alobet_matchbethis.py premier_league.txt spain.txt series_a.txt champion_league.txt
/root/project/OkChym/188bet/alobet_firstbethis.py premier_league_1half.txt spain_1half.txt series_a_1half.txt champion_league_1half.txt
/root/project/OkChym/188bet/alobet_matchscorebet.py premier_league_correctscore.txt spain_correctscore.txt series_a_correctscore.txt champion_league_correctscore.txt
