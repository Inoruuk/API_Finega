from pymongo import MongoClient
from datetime import datetime, timedelta
from math import pi
import re
from sys import argv as av


client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production

pat = '(\d+):(\d+):(\d+)'


def subtime(t1, t2):
	try:
		return str(datetime.strptime(t1, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(t2, '%Y-%m-%dT%H:%M:%S'))
	except ValueError:
		return str(datetime.strptime(str(t1), '%H:%M:%S') - datetime.strptime(str(t2), '%H:%M:%S'))


# A ameliorer
def addtime(l: list):
	total = timedelta(hours=0, minutes=0, seconds=0)
	for time in l:
		t = re.findall(pat, time)[0]
		total += timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
	return str(total)


def check_config(conf, item):
	return (
			conf['LongueurDeCampagneMM'] == item['LongueurDeCampagneMM'] and
			conf['EpaisseurPrincipaleMultilame'] == item['EpaisseurPrincipaleMultilame'] and
			conf['HauteurProduitsMultilame'] == item['HauteurProduitsMultilame'] and
			conf['EpaisseurSecondaireMultilame'] == item['EpaisseurSecondaireMultilame'] and
			conf['NombreProduitsSecondaires'] == conf['NombreProduitsSecondaires'] and
			conf['NumeroConfiguration'] == item['NumeroConfiguration'] and
			conf['LargeurDeligneuse1'] == item['LargeurDeligneuse1'] and
			conf['LargeurDeligneuse2'] == item['LargeurDeligneuse2'] and
			conf['LargeurDeligneuse3'] == item['LargeurDeligneuse3'] and
			conf['LargeurDeligneuse4'] == item['LargeurDeligneuse4'] and
			conf['LargeurDeligneuse5'] == item['LargeurDeligneuse5'] and
			conf['HauteurDeligneuse'] == item['HauteurDeligneuse']
	)

"""
return une date dont l'heure correspond a la pause matin, midi et aprem
"""

def temps_sciage(debut, fin):
	res = {}
	nb_docs = doc.count_documents({'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}})
	query = doc.find(
		{'TempsDeCycle.Time': {'$gte': debut, '$lt': fin}},
		{
			'TempsDeCycle.Time': 1,
			'InfosCycleAutomate.FinSciage': 1,
			'InfosTempsDeCycle.HeureDepartTransfertTableVersIntermediaireOuPortique': 1,
			'InfoConfigurationLigne': 1,
			'MesureGrume': 1,
		}
	)
	res['duree du poste'] = '00:00:00'
	res['mise sous tension'] = '00:00:00'
	res['mise hors tension'] = '00:00:00'
	res['premiere grume'] = query[0]['TempsDeCycle']['Time']
	res['dernier grume'] = query[nb_docs -1]['TempsDeCycle']['Time']
	res['derniere grume avant pause matin'] = doc.find({'TempsDeCycle.Time': {'$lt': '2019-10-10T10:00:00'}}).sort([('_id', -1), ('TempsDeCycle.Time', -1)]).limit(1)[0]['TempsDeCycle']['Time']
	res['premiere grume apres pause matin'] = doc.find({'TempsDeCycle.Time': {'$gt': '2019-10-10T10:00:00'}}).limit(1)[0]['TempsDeCycle']['Time']
	res['derniere grume avant pause midi'] = doc.find({'TempsDeCycle.Time': {'$lt': '2019-10-10T12:00:00'}}).sort([('_id', -1), ('TempsDeCycle.Time', -1)]).limit(1)[0]['TempsDeCycle']['Time']
	res['premiere grume apres pause midi'] = doc.find({'TempsDeCycle.Time': {'$gt': '2019-10-10T12:00:00'}}).limit(1)[0]['TempsDeCycle']['Time']
	res['derniere grume avant pause aprem'] = doc.find({'TempsDeCycle.Time': {'$lt': '2019-10-10T15:30:00'}}).sort([('_id', -1), ('TempsDeCycle.Time', -1)]).limit(1)[0]['TempsDeCycle']['Time']
	res['premiere grume apres pause aprem'] = doc.find({'TempsDeCycle.Time': {'$gt': '2019-10-10T15:30:00'}}).limit(1)[0]['TempsDeCycle']['Time']
	res['dure production pause comprise'] = subtime(res['dernier grume'], res['premiere grume'])
	res['duree pause matin'] = subtime(res['premiere grume apres pause matin'], res['derniere grume avant pause matin'])
	res['duree pause midi'] = subtime(res['premiere grume apres pause midi'], res['derniere grume avant pause midi'])
	res['duree pause aprem'] = subtime(res['premiere grume apres pause aprem'], res['derniere grume avant pause aprem'])
	res['duree total pause'] = addtime([res['duree pause matin'], res['duree pause midi'], res['duree pause aprem']])
	# tps de prod - tps de pause
	res['temps de sciage effectif'] = subtime(res['dure production pause comprise'], res['duree total pause'])
	res['duree derniere plage'] = []
	res['duree changement prod hors pause'] = '00:00:00'
	# temps de sciage effectif(tps prod - cumul pause)
	res['temps de sciage effectif(minutes)']= 0
	res['temps total sciage / temps prdo(%)']= 0
	res['nombre total de grume']= nb_docs
	res['volume total marchand']= 0
	res['cumul longueur totale']= 0
	res['longueur moyenne billion(m)']= 0
	res['diametre moyen billion(mm)']= 0
	res['volume moyen billion(m3)']= 0
	res['temps de cycle moyen(s)']= 0
	res['prod moyenne / temps de sciage effectif(m3/h)']= 0

	campagne = query[0]['InfoConfigurationLigne']
	time = res['premiere grume']
	plages = []
	for item in query:
		"""
		Horaires: Duree derniere plage
		"""
		y = subtime(
			item['InfosCycleAutomate']['FinSciage'],
			item['InfosTempsDeCycle']['HeureDepartTransfertTableVersIntermediaireOuPortique']
		)
		plages.append(y)
		if y >= '0:01:30':
			res['duree derniere plage'].append(y)
		"""
		Horaires: duree changement prod hors pause
		"""
		if check_config(campagne, item['InfoConfigurationLigne']):
			time = item['TempsDeCycle']['Time']
		else:
			res['duree changement prod hors pause'] = addtime([
				res['duree changement prod hors pause'],
				subtime(item['TempsDeCycle']['Time'], time)]
			)
			campagne = item['InfoConfigurationLigne']
			time = item['TempsDeCycle']['Time']
		"""
		Cumul: Longueur total
		"""
		res['cumul longueur totale'] += item['MesureGrume']['LongueurReelleMM'] / 1000
		"""
		Donnees moyennes longueur et diametre
		"""
		res['longueur moyenne billion(m)'] += item['MesureGrume']['LongueurReelleMM']
		res['diametre moyen billion(mm)'] += item['MesureGrume']['DiametreMoyenMM']
	#fin for
	res['duree derniere plage'] = addtime(res['duree derniere plage'])
	res['cumul longueur totale'] = round(res['cumul longueur totale'], 1)

	res['temps de sciage effectif(minutes)'] = \
		round(sum(int(x) * 60 ** i for i, x in enumerate(reversed(res['temps de sciage effectif'].split(':')))) / 60, 1)
	res['longueur moyenne billion(m)'] /= res['nombre total de grume']
	res['diametre moyen billion(mm)'] /= float('%.2f' % res['nombre total de grume'])
	res['volume moyen billion(m3)'] = float('%.2f' % round(pi * pow(res['diametre moyen billion(mm)'] / 2 / 1000, 2) * res['longueur moyenne billion(m)'] / 1000, 2))
	plages = addtime(plages)
	res['temps de cycle moyen(s)'] = float('%.2f' % (sum(int(x) * 60 ** i for i, x in enumerate(reversed(plages.split(':')))) / nb_docs))
	res['prod moyenne / temps de sciage effectif(m3/h)'] = None
	print(res)


if __name__ == '__main__':
	#Need param pause matin, midi, soir
	n, debut, fin = av
	temps_sciage(debut=debut, fin=fin)

