const router = require('express').Router();
const mongoose = require('mongoose');
var stringify = require('json-stringify-safe');

router.post('/', (req, res) => {
  res.json({
    status: 'OK',
  });
});


////--------- LIVEMONITORING

const livemonitoringService = require('../Services/liveMonitoringService');

router.route('/livemonitoring/').post((req, res) => {
    livemonitoringService(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});

////---------PRODUCTION

const productionService = require('../Services/productionService');

router.route('/production/temps_sciage').post((req, res) => {
    productionService.tempsSciage(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});

router.route('/production/cycle').post((req, res) => {
    productionService.tempsCycles(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});

router.route('/production/supply').post((req, res) => {
    productionService.approvisionement(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            console.log(err)
            res.json(err.err).status(err.status).end();
        })
});

router.route('/production/production').post((req, res) => {
    productionService.production(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            console.log(err)
            res.json(err.err).status(err.status).end();
        })
});


module.exports = router;