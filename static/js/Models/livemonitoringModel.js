const mongoose = require('mongoose');

const livemonitoringSchema = new mongoose.Schema(
    {
        Theme: String,
        Numero_Controleur: Number,
        Index: Number,
        Groupe: Number,
        Repere: String,
        Libelle: String,
        Type: String,
        Date: Date,
        Valeur: Number
    }    
);


const livemonitoringModel = mongoose.model('livemonitoringModel', livemonitoringSchema, 'live_monitoring');

module.exports = livemonitoringModel;