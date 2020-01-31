const livemonitoringModel = require('../Models/livemonitoringModel');

function livemonitoringService(body) {
    const promise = new Promise((resolve, reject) => {
        var request = JSON.parse(JSON.stringify(body));
        request.Date = {
            $gte: body.DateDebut,
            $lt: body.DateFin
        };
        delete request.DateDebut;
        delete request.DateFin;
        livemonitoringModel.find(request, (err, result) => {
            if (err) {
                reject({status: 500, err});
            } else {
                resolve({status: 200, result});
            }
        });
    });
    return promise
}

module.exports = livemonitoringService;