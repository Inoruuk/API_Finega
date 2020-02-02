from pymongo import MongoClient
from math import pi, pow
from copy import deepcopy
from json import dumps
from sys import argv as av

client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production


def get_diam(item, diam):
	for t in diam:
		if t[0] <= item < t[1]:
			return str(t)
	return 0


def create_res(diams: list, filtre_diam: tuple = None):
	"""

	:param diams: list of diameters
	:param filtre_diam: diameters filter
	:return:
	"""
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
	if filtre_diam:
		res[str(filtre_diam)] = deepcopy(res['Cumul'])
	else:
		for diam in diams:
			res[str(diam)] = deepcopy(res['Cumul'])
	return res


def appro(debut, fin, diams: list = None, filtre_long: int = None, filtre_diam: tuple = None):
	"""
	:param debut: debut de la plage de temps a selectionner sous forme de 'yyyy-mm-ddThh:mm:ss'
	:param fin: fin de la plage de temps a selectionner sous forme de 'yyyy-mm-ddThh:mm:ss'
	:param diam: list de tuple de filtre de diametres
	:return: nuting
	"""
	query = doc.find(
		{'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}},
		{'MesureGrume': 1, 'InfosSciage': 1, '_id': 0}
	)
	res = create_res(diams, filtre_diam)
	res['Cumul']['nb %'] = 100
	nb_total = doc.find({'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}}, {}).count()
	for item in query:
		# l = item['MesureGrume']['LongueurMarchandeMM']
		if filtre_long and filtre_long != item['MesureGrume']['LongueurMarchandeMM']:
			continue
		diam = get_diam(item['MesureGrume']['DiametreCubageMM'], diams)
		if diam in res:
			diam_cub = item['MesureGrume']['DiametreCubageMM'] / 10 / 2
			long_cub = item['MesureGrume']['LongueurCubageMM'] / 10
			vol = (pi * pow(diam_cub, 2) * long_cub) / 1000000
			res[diam]['vol grume(m3)'], res['Cumul']['vol grume(m3)'] = res[diam]['vol grume(m3)'] + vol, res['Cumul']['vol grume(m3)'] + vol
			res[diam]['nb'], res['Cumul']['nb'] = res[diam]['nb'] + 1, res['Cumul']['nb'] + 1
			for x in item['InfosSciage']['InfosSciage']:
				vol = x['Epaisseur'] * x['Longueur'] * x['Largeur'] * x['NombreProduits'] / 1000000000
				if x['NombreProduits'] != 0:
					if x['Info'] & 1 == 1:
						res[diam]['vol multi(m3)'], res['Cumul']['vol multi(m3)'] = res[diam]['vol multi(m3)'] + vol, res['Cumul']['vol multi(m3)'] + vol
					else:
						res[diam]['vol delign(m3)'], res['Cumul']['vol delign(m3)'] = res[diam]['vol delign(m3)'] + vol, res['Cumul']['vol delign(m3)'] + vol
					res[diam]['vol prod(m3)'] += vol
					res['Cumul']['vol prod(m3)'] += vol
	for item in res:
		res[item]['nb %'] = round(res[item]['nb'] * 100 / nb_total)
		res[item]['vol grume(m3)'] = round(res[item]['vol grume(m3)'], 2)
		res[item]['vol multi(%)'] = round(res[item]['vol multi(%)'], 2)
		res[item]['vol delign(%)'] = round(res[item]['vol delign(%)'], 2)
		res[item]['%'] = round(res[item]['vol prod(m3)'] * 100 / res['Cumul']['vol grume(m3)'])
		res[item]['vol multi(%)'] = round(res[item]['vol multi(m3)'] * 100 / res['Cumul']['vol prod(m3)'])
		res[item]['vol delign(%)'] = round(res[item]['vol delign(m3)'] * 100 / res['Cumul']['vol prod(m3)'])

	print(dumps(res, indent=4))


if __name__ == '__main__':
	for x in av:
		print(x)
	appro(
		'2019-12-02T00:00:00',
		'2019-12-02T23:59:59',
		[(0, 240), (240, 260), (260, 280), (280, 300), (300, 320), (320, 340), (340, 360), (360, 380), (380, 400), (400, 600)],
		filtre_diam=(300, 320),
		filtre_long=2800,
	)
