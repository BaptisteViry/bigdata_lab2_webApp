from django.shortcuts import render
from django.http import HttpResponse

from pymongo import MongoClient

import json, random

#client = MongoClient('bigdata-mongodb-04.virtual.uniandes.edu.co', 8087)
client = MongoClient('localhost', 27017)
db = client.Grupo10
collectionVenezuela = db.Venezuela_1
collectionMinga = db.minga_1
collectionJep = db.jep_1

def index(request):
    return render(request, "taller2/index.html")

def presentacionDB(request):
    #first consult
    countVenezuela = collectionVenezuela.find({}).count()
    countMinga = collectionMinga.find({}).count()
    countJep = collectionJep.find({}).count()
    countCollections = { 'countVenezuela':countVenezuela, 'countMinga':countMinga, 'countJep':countJep}
    context = { 'countCollections':countCollections }

    return render(request, "taller2/presentacionDB.html", context)

def charts(request):
    resultado=collectionMinga.aggregate([{"$group":{"_id":"$polaridad","count":{"$sum":1}}}])
    insulto=-1
    negativo=-1
    neutro=-1
    positivo=-1
    for r in resultado:        
        print(r)
        if (r.get("_id")=="Insulto"):
            insulto=r.get("count")
        elif (r.get("_id")=="Negativo"):
            negativo=r.get("count")
        elif (r.get("_id")=="Neutro"):
            neutro=r.get("count")
        elif (r.get("_id")=="Positivo"):
            positivo=r.get("count")
        
    dataPolarity = { 'Positivo':positivo, 'Neutro':neutro, 'Negativo':negativo, 'Insulto':insulto }

    context = {'dataPolarity': dataPolarity}
    return render(request, "taller2/charts.html", context)

def hashtagWordCloud(request):
    #groupBy hashtags
    i = 10
    hashtagsArray = []
    hashtagsCursor = collectionVenezuela.aggregate([{'$unwind': '$entities.hashtags'}, { '$group': { '_id': '$entities.hashtags.text', 'count': {'$sum': 1}}}, { '$sort': { 'count': -1 }},{ '$limit': 10 }])
    for h in hashtagsCursor:
        x = {"hashtag": h["_id"], "count": h["count"], "rank": i}
        hashtagsArray.append(x)
        i -= 1 

    random.shuffle(hashtagsArray)
    print(hashtagsArray)


    context = { "hashtags": hashtagsArray}
    return render(request, "taller2/hashtagWordCloud.html", context)