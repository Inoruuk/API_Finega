const livemonitoringModel = require('../Models/livemonitoringModel');
const { exec } = require('child_process');

// function livemonitoringService(body) {
//     const promise = new Promise((resolve, reject) => {
//         var request = JSON.parse(JSON.stringify(body));
//         request.Date = {
//             $gte: body.DateDebut,
//             $lt: body.DateFin
//         };
//         delete request.DateDebut;
//         delete request.DateFin;
//         livemonitoringModel.find(request, (err, result) => {
//             if (err) {
//                 console.log(err);
//                 reject({status: 500, err});
//             } else {
//                 console.log(result);
//                 resolve({status: 200, result});
//             }
//         });
//     });
//     return promise
// }

function livemonitoringService(body) {
    const promise = new Promise((resolve, reject) => {
        var str = '"' + body.DateDebut + '" "' + body.DateFin + '" "' + body.NumeroControleur + '" "' + body.Index + '" "' + body.Groupe + '" "' + body.Libelle + '"';
        var string = 'python3 Script/livemonitoring.py ' + str;
        // console.log(str, string);
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

module.exports = livemonitoringService;