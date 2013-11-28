var sys = require('sys');
var exec = require('child_process').exec;
var child;
child = exec("/usr/bin/python /root/project/OkChym/alobet_OU.py", function (error, stdout, stderr) {
    sys.print('stdout: ' + stdout);
    sys.print('stderr: ' + stderr);
});
