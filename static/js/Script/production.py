from pymongo import MongoClient
from math import pi, pow
from copy import deepcopy
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.production


def create_res(ep, lar, long):
	res = {}
	lst = [(x, y) for x in ep for y in lar]
	for item in lst:

	return res


def prod_nb(debut: str, fin: str, epaisseur: list, largeur: list, longueur: list):
	res = create_res(epaisseur, largeur, longueur)



if __name__ == '__main__':
	prod_nb(
		debut='2019-12-02T00:00:00',
		fin='2019-12-02T23:59:59',
		epaisseur=[18, 80, 100],
		largeur=[40, 50 ,60],
		longueur=[],
	)