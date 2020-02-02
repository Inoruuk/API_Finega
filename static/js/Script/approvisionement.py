from pymongo import MongoClient
from math import pi, pow
from copy import deepcopy
from json import dumps
from sys import argv as av
import re

client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production

pattern = '\(([\d, ]+)\)'


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
	nb_total = doc.count_documents({'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}}, {})
	if not nb_total:
		print({})
		return
	for item in query:
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

	x = res['Cumul']
	res.pop('Cumul')
	res['Cumul'] = x
	print(res)


if __name__ == '__main__':
	n, debut, fin, param, filtre_diam, filtre_long = av
	filtre_long = int(filtre_long)
	param = [int(x) for x in param.split(',')]
	param = [(x, y) for x, y in zip(param[::2], param[1::2])]
	filtre_diam = filtre_diam.split(',')
	filtre_diam = (int(filtre_diam[0]), int(filtre_diam[1]))
	appro(
		debut=debut,
		fin=fin,
		diams=param,
		filtre_diam=filtre_diam,
		filtre_long=filtre_long,
	)
