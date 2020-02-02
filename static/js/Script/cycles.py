from datetime import datetime
from pymongo import MongoClient
from json import dumps
from sys import argv as av

client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production


def subtime(t1, t2):
	try:
		return (datetime.strptime(t1, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(t2, '%Y-%m-%dT%H:%M:%S')).total_seconds()
	except ValueError:
		return (datetime.strptime(str(t1), '%H:%M:%S') - datetime.strptime(str(t2), '%H:%M:%S')).total_seconds()


def cycles(debut, fin, plages: list):
	"""
	debut, fin : journee entiere pour la query
	plages: liste de tuple des plages en parametre
	"""
	res = {
		'Cumul':{
			'Nombre de grume': 0,
			'% Grume par plage': 0,
			'Cumul de temps de cycle': 0
		}
	}
	query = doc.find(
		{'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}},
		{'InfosCycleAutomate.FinSciage', 'InfosTempsDeCycle.HeureDepartTransfertTableVersIntermediaireOuPortique'}
	)
	for y in range(len(plages)):
		res['Plage ' + str(y)] = {
			'Nombre de grume' : 0,
			'% Grume par plage': 0,
			'Cumul de temps de cycle': 0,
			'%Temps de cycle/Temps de sciage effectif': 0,
			'Temps de cycle moyen': 0
		}
	for item in query:
		plage = subtime(
			item['InfosCycleAutomate']['FinSciage'],
			item['InfosTempsDeCycle']['HeureDepartTransfertTableVersIntermediaireOuPortique']
		)
		for x, time in enumerate(plages):
			if time[0] <= plage <= time[1]:
				res['Plage ' + str(x)]['Cumul de temps de cycle'] += plage
				res['Plage ' + str(x)]['Nombre de grume'] += 1
				res['Cumul']['Cumul de temps de cycle'] += plage
				res['Cumul']['Nombre de grume'] += 1
	for item in res:
		res[item]['% Grume par plage'] = int(res[item]['Nombre de grume'] * 100 / res['Cumul']['Nombre de grume'])
		res[item]['Temps de cycle moyen'] = int(res[item]['Cumul de temps de cycle'] / res[item]['Nombre de grume']) if res[item]['Nombre de grume'] else 0
		res[item]['Cumul de temps de cycle'] = '%d:%d:%d' % (res[item]['Cumul de temps de cycle']/3600, res[item]['Cumul de temps de cycle'] / 60 % 60, res[item]['Cumul de temps de cycle'] // 60 % 60)
	print(res)


if __name__ == '__main__':
	n, debut, fin, param = av
	param = [int(x) for x in param.split(',')]
	param = [(x, y) for x, y in zip(param[::2], param[1::2])]
	print(param)
	cycles(debut, fin, param)
