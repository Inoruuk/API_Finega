const productionModel = require('../Models/productionModel');
const { exec } = require('child_process');


function tempsSciage(body) {
    const promise = new Promise((resolve, reject) => {
        var string = "python3 Script/temps_sciage.py  " + body.Debut + '  ' + body.Fin;
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


function tempsCycles({Debut, Fin, Cycles}) {
    const promise = new Promise((resolve, reject) => {
        var string = "python3 Script/cycles.py " + Debut + ' ' + Fin + ' ' + Cycles;
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


function approvisionement({DateDebut, DateFin, param_diam, filtre_diam, filtre_longueur}) {
    const promise = new Promise((resolve, reject) => {
       var str = DateDebut + ' ' + DateFin + ' ' + param_diam + ' ' + filtre_diam + ' ' + filtre_longueur;
        var string = 'python3 Script/approvisionement.py ' + str;
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

function productionProduits({Debut, Fin, Sections}) {
    const promise = new Promise((resolve, reject) => {
       var str = Debut + ' ' + Fin + ' ' + Sections;
        var string = 'python3 Script/production.py ' + str;
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
    productionProduits,

};
