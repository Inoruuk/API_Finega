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

//{"DateDebut":  "2020-01-08T00:00:00","DateFin": "2020-01-08T23:00:50","NumeroControleur": 0,"Index": 2,"Groupe": 0,"Libelle": "Position"}
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

//{"Debut": "2019-12-02T07:41:49","Fin": "2019-12-02T23:50:00"}
router.route('/production/temps_sciage').post((req, res) => {
    productionService.tempsSciage(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});

//{"Debut":"2019-12-02T00:00:00", "Fin": "2019-12-02T23:59:59", "Cycles": [[0, 25], [26, 30], [31, 35], [36, 40], [41, 50], [51, 60], [61, 90], [91, 36000]]}
router.route('/production/cycle').post((req, res) => {
    productionService.tempsCycles(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            res.json(err.err).status(err.status).end();
        })
});

//{ "DateDebut":  "2019-12-02T00:00:00", "DateFin": "2019-12-02T23:00:50", "param_diam": [[0, 240], [240, 260], [260, 280], [280, 300], [300, 320], [320, 340], [340, 360],  [360, 380], [380, 400], [400, 600]], "filtre_diam":"300,320", "filtre_longueur": 2800 }
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

//{"Debut":"2019-12-02T00:00:00","Fin":"2019-12-02T23:59:59","Sections": [[18, 80], [18, 100], [20, 80], [60, 80], [80, 80]],"Filtre_longueur": 0}
router.route('/production/production_produits').post((req, res) => {
    productionService.productionProduits(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            console.log(err)
            res.json(err.err).status(err.status).end();
        })
});

//{"Debut":"2019-12-02T00:00:00","Fin":"2019-12-02T23:59:59","Sections": [[18, 80], [18, 100], [20, 80], [60, 80], [80, 80]],"Filtre_longueur": 0}
router.route('/production/production_volume').post((req, res) => {
    productionService.productionVolume(req.body)
        .then((data) => {
            res.json(data.result).status(data.status).end();
        })
        .catch((err) => {
            console.log(err)
            res.json(err.err).status(err.status).end();
        })
});


module.exports = router;