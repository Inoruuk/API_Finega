const lifetimeModel = require('../Models/lifetimeModel');

function lifetimeService(Date) {
    const promise = new Promise((resolve, reject) => {
        lifetimeModel.find({Date}, (err, result) => {
            if (err) {
                reject({status: 500, err});
                return;
            }
            console.log(Date);
            resolve({status: 200, result});
        });
    });
}

module.exports = lifetimeService;