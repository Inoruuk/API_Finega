const mongoose = require('mongoose');

const lifetimeSchema = new mongoose.Schema(
    {
	Composant : {
		Designation : String,
		Cle : Number,
		Reference :  String,
		ReferenceConstructeur :  String,
		ImageComposant :  String,
		TypeComposant : Number,
		Repere : String,
		Unite : Number
	},
	Parametres : {
		Unite : Number,
		Seuil1 : Number,
		Seuil2 : Number
	},
	Etat : {
		Valeur : Number
	},
	Changements : {
		Changements : [ ]
	}
}
);


const lifetimeModel = mongoose.model('lifetimeModel', lifetimeSchema, 'lifetime');

module.exports = lifetimeModel;