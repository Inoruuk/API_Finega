from pymongo import MongoClient
from copy import deepcopy
from sys import argv as av

client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production


def create_res(param):
	res = {
		'Total': {
			'T': 0,
			'M': 0,
			'D': 0,
		},
		'Total %': {
			'T': 0,
			'M': 0,
			'D': 0,
		},
	}
	for item in param:
		res[item] = deepcopy(res['Total'])
	return res


def get_section(item):
	return item['Epaisseur'], item['Largeur']


def prod_nb(debut: str, fin: str, param: list, filtre_long: int=0):
	res = create_res(param)
	query = doc.find({'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}}, {'InfosSciage.InfosSciage': 1, '_id': 0})
	nb_total = 0
	for item in query:
		for sections in item['InfosSciage']['InfosSciage']:
			nb_total += sections['NombreProduits']
			if filtre_long and sections['Longueur'] != filtre_long:
				continue
			if sections['NombreProduits']:
				section = get_section(sections)
				if section in param:
					if sections['Info'] & 1:
						res[section]['M'] += sections['NombreProduits']
					else:
						res[section]['D'] += sections['NombreProduits']
	for item in res:
		res[item]['T'] = res[item]['D'] + res[item]['M']
		res['Total']['T'] += res[item]['T']
		res['Total']['D'] += res[item]['D']
		res['Total']['M'] += res[item]['M']
	res['Total %']['D'] = round(res['Total']['D'] * 100 / nb_total)
	res['Total %']['M'] = round(res['Total']['M'] * 100 / nb_total)
	res['Total %']['T'] = res['Total %']['D'] + res['Total %']['M']
	print(res)


if __name__ == '__main__':
	n, debut, fin, param , filtre_long = av
	param = [int(x) for x in param.split(',')]
	param = [(x, y) for x, y in zip(param[::2], param[1::2])]
	filtre_long = int(filtre_long)
	prod_nb(
		debut=debut,
		fin=fin,
		param=param,
		filtre_long=filtre_long
	)
