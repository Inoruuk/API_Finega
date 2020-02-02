const productionModel = require('../Models/productionModel');
const { exec } = require('child_process');


function tempsSciage(body) {
    const promise = new Promise((resolve, reject) => {
        var string = "python3 Script/temps_sciage.py" + body;
        exec(string, (err, stdout, stderr) => {
        if (err) {
            console.log(stderr);
            console.error(err);
             reject({status: 500, err});
        } else {
            const result = JSON.parse(JSON.stringify(stdout, null, 4));
            // console.log(res);
            resolve({status: 200, result});
        }
        });
    });
    return promise
}


function tempsCycles(body) {
    const promise = new Promise((resolve, reject) => {
        var string = "python3 Script/cycles.py" + body;
        exec(string, (err, stdout, stderr) => {
        if (err) {
            console.log(stderr);
            console.error(err);
             reject({status: 500, err});
        } else {
            const result = JSON.parse(JSON.stringify(stdout, null, 4));
            // console.log(res);
            resolve({status: 200, result});
        }
        });
    });
    return promise
}


function approvisionement(body) {
    const promise = new Promise((resolve, reject) => {
        var str = '"' + body.DateDebut + '" "' + body.DateFin + '" "' + body.NumeroControleur + '" "' + body.Index + '" "' + body.Groupe + '" "' + body.Libelle + '"';
        var string = 'python3 Script/livemonitoring.py ' + str;
        exec(string, (err, stdout, stderr) => {
        if (err) {
            console.log(stderr);
             reject({status: 500, err});
        } else {
            console.log(stdout);
            const result = JSON.parse(JSON.stringify(stdout, null, 4));
            resolve({status: 200, result});
        }
        });
    });
    return promise
}

module.exports = {
    tempsSciage,
    tempsCycles,
    approvisionement,

};
