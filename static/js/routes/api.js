const router = require('express').Router();
const mongoose = require('mongoose');
var stringify = require('json-stringify-safe');

router.get('/', (req, res) => {
  res.json({
    status: 'OK',
  });
});


////---------LIVEMONITORING

const livemonitoringService = require('../Services/liveMonitoringService');

router.route('/livemonitoring/').get((req, res) => {
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

router.route('/production/temps_sciage').get((req, res) => {
    productionService.tempsSciage(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});

router.route('/production/cycle').get((req, res) => {
    productionService.tempsCycles(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});


module.exports = router;