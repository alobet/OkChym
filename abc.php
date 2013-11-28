<?php
    $ch = curl_init();
 
    $url = 'http://www.188bet.com/en-gb/Service/OddsService?GetOdds&_=1382945051631&Tab=Competition&UIBetType=ftahou&SportId=1&IsInplay=false&OddsType=3&SortBy=1&IsFirstLoad=true';
   
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_REFERER, 'http://www.188bet.com/en-gb/sports/football/competition/full-time-asian-handicap-and-over-under?competitionids=26726');
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1');
    curl_setopt($ch, CURLOPT_COOKIESESSION, true);
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Cookie:__utma=206930963.1406735620.1381196282.1382935188.1382945051.3; __utmz=206930963.1381196282.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); lan=en-gb; timeZone=420; dst=0; filterStatus=inplay=&noninplay=f1btn|1,f2btn|1; __utmb=206930963.16.10.1382945051; ASP.NET_SessionId=rcz5r2jxojda3z3nwgdq31v3; sscd=rd546o00000000000000000000ffffac152183o80; HighlightedSport=FOOTBALL|False; __utmc=206930963; BS@Cookies='
    ));
   
    $result = curl_exec ($ch);
    var_dump($result); // output?
    curl_close($ch);
    
    exit();
    
    ?>
