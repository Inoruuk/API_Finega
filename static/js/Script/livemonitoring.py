from pymongo import MongoClient
from sys import argv as av


client = MongoClient('mongodb://localhost:27017/')
db = client.data
doc = db.live_monitoring


def livemonitoring(debut, fin, num, index, groupe, lib):
    query = doc.find(
        {
            'Date': {'$gte': debut, '$lt': fin},
            'Numero Controleur': int(num),
            'Index': int(index),
            'Groupe': int(groupe),
            'Libelle': lib,
        },
        {
            'Valeur': 1,
            '_id': 0
        }
    )
    res = []
    for item in query:
        try:
            res.append(item['Valeur'])
        except KeyError:
            pass
    print(res, end='')


if __name__ == '__main__':
    debut, fin, num, index, groupe, lib = av[1], av[2], av[3], av[4], av[5], av[6],
    livemonitoring(debut=debut, fin=fin, num=num, index=index, groupe=groupe, lib=lib)
