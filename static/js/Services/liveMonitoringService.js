const livemonitoringModel = require('../Models/livemonitoringModel');
const { exec } = require('child_process');

function livemonitoringService(body) {
    const promise = new Promise((resolve, reject) => {
        var str = '"' + body.DateDebut + '" "' + body.DateFin + '" "' + body.NumeroControleur + '" "' + body.Index + '" "' + body.Groupe + '" "' + body.Libelle + '"';
        var string = 'python3 Script/livemonitoring.py ' + str;
        exec(string, (err, stdout, stderr) => {
        if (err) {
            console.log(stderr);
             reject({status: 500, err});
        } else {
            var result = JSON.parse(JSON.stringify(stdout, null, 4));
            result = result.split("'").join('"');
            console.log(result);

            resolve({status: 200, result});
        }
        });
    });
    return promise
}

module.exports = livemonitoringService;