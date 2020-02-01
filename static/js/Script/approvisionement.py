from pymongo import MongoClient
from math import pi, pow
from copy import deepcopy
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production


def create_res(long, diam):
	res = {
		'Cumul': {
			'nb': 0,
			'nb %': 0,
			'vol grume(m3)': 0,
			'vol prod(m3)': 0,
			'%': 0,
			'vol multi(m3)': 0,
			'vol multi(%)': 0,
			'vol delign(m3)': 0,
			'vol delign(%)': 0
		}
	}
	for x in long:
		res[x] = {}
		for y in diam:
			res[x][str(y)] = deepcopy(res['Cumul'])
	return res


def get_d(item, diam):
	for t in diam:
		if t[0] <= item < t[1]:
			return str(t)
	return 0


def appro(debut, fin, diam: list, long: list, filtre_long: int = None, filtre_diam: tuple = None):
	"""
	:param debut: debut de la plage de temps a selectionner sous forme de 'yyyy-mm-ddThh:mm:ss'
	:param fin: fin de la plage de temps a selectionner sous forme de 'yyyy-mm-ddThh:mm:ss'
	:param diam: list de tuple de filtre de diametres
	:param long: list de tuple de filtre de longueur
	:return: nuting
	"""
	query = doc.find(
		{'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}},
		{'MesureGrume': 1, 'InfosSciage': 1, '_id': 0}
	)
	res = create_res(long, diam)
	res['Cumul']['nb %'] = 100
	for item in query:
		l = item['MesureGrume']['LongueurMarchandeMM']
		d = get_d(item['MesureGrume']['DiametreCubageMM'], diam)
		diam_cub = item['MesureGrume']['DiametreCubageMM'] / 10 / 2
		long_cub = item['MesureGrume']['LongueurCubageMM'] / 10
		vol = (pi * pow(diam_cub, 2) * long_cub) / 1000000
		res[l][d]['vol grume(m3)'], res['Cumul']['vol grume(m3)'] = res[l][d]['vol grume(m3)'] + vol, res['Cumul']['vol grume(m3)'] + vol
		res[l][d]['nb'], res['Cumul']['nb'] = res[l][d]['nb'] + 1, res['Cumul']['nb'] + 1
		for x in item['InfosSciage']['InfosSciage']:
			if x['NombreProduits'] != 0:
				if x['Info'] & 1 == 1:
					res[l][d]['vol multi(m3)'] += x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000
					res['Cumul']['vol multi(m3)'] += x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000
				elif x['Info'] & 4 == 4:
					res[l][d]['vol delign(m3)'] += x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000
					res['Cumul']['vol delign(m3)'] += x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000
				res[l][d]['vol prod(m3)'] +=  x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000
				res['Cumul']['vol prod(m3)'] +=  x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000

	res['Cumul']['%'] = round(res['Cumul']['vol prod(m3)'] * 100 / res['Cumul']['vol grume(m3)'], 1)
	res['Cumul']['vol multi(%)'] = round((res['Cumul']['vol multi(m3)'] * 100 / res['Cumul']['vol prod(m3)']), 1)
	res['Cumul']['vol delign(%)'] = round((res['Cumul']['vol delign(m3)'] * 100 / res['Cumul']['vol prod(m3)']), 1)
	for item in res:
		if item != 'Cumul':
			for second in res[item]:
				res[item][second]['nb %'] = round(res[item][second]['nb'] * 100 / res['Cumul']['nb'], 1)
				res[item][second]['vol grume(m3)'] = round(res[item][second]['vol grume(m3)'], 1)
				res[item][second]['vol multi(%)'] = round(res[item][second]['vol multi(%)'], 1)
				res[item][second]['vol delign(%)'] = round(res[item][second]['vol delign(%)'], 1)
				res[item][second]['%'] = round(res[item][second]['vol prod(m3)'] * 100 / res['Cumul']['vol grume(m3)'], 1)
				res[item][second]['vol multi(%)'] = round(res[item][second]['vol multi(m3)'] * 100 / res['Cumul']['vol prod(m3)'], 1)
				res[item][second]['vol delign(%)'] = round(res[item][second]['vol delign(m3)'] * 100 / res['Cumul']['vol prod(m3)'], 1)

	if filtre_long and not filtre_diam:
		res = {x:res[x] for x in res if x == 'Cumul' or x == filtre_long}
	elif not filtre_long and filtre_diam:
		pass
	elif filtre_diam and filtre_long:
		res = {x:res[x] for x in res if x == 'Cumul' or x == filtre_long}
		res[filtre_long] = {x:res[filtre_long][x] for x in res[filtre_long] if x == str(filtre_diam)}
	print(json.dumps(res, indent=4))


if __name__ == '__main__':
	appro(
		'2019-12-02T00:00:00',
		'2019-12-02T23:59:59',
		[(0, 240), (240, 260), (260, 280), (280, 300), (300, 320), (320, 340), (340, 360), (360, 380), (380, 400), (400, 600)],
		[2600, 2800, 3000],
		filtre_diam=(300, 320),
		filtre_long=2800,
	)
