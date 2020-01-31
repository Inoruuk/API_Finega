const productionModel = require('../Models/productionModel');
const { exec } = require('child_process');


function tempsSciage(Date) {
    const promise = new Promise((resolve, reject) => {
        Date = '';
        var string = "python3 Script/temps_sciage.py" + Date;
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


function tempsCycles(Date, Cycles) {
    const promise = new Promise((resolve, reject) => {
        Date = '';
        var string = "python3 Script/cycles.py" + Date;
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

module.exports = {
    tempsSciage,
    tempsCycles,

};
