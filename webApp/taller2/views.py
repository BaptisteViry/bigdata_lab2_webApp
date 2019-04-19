from django.shortcuts import render
from django.http import HttpResponse

from pymongo import MongoClient

import json, random
from random import randint

client = MongoClient('bigdata-mongodb-04.virtual.uniandes.edu.co', 8087)
#client = MongoClient('localhost', 27017)
db = client.Grupo10
collectionVenezuela = db.venezuela_1
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
    ctxJep=getPolaridad("jep")
    ctxMinga=getPolaridad("minga")
    ctxVenezuela=getPolaridad("venezuela")

    #context = {'dataPolarity': dataPolarity}
    context = {'jep': ctxJep,'minga':ctxMinga,'venezuela':ctxVenezuela}
    print (context)
    return render(request, "taller2/charts.html", context)

def getPolaridad(coleccion):
    if (coleccion=="jep"):
        col=collectionJep
    elif(coleccion=="minga"):
        col=collectionMinga
    elif(coleccion=="venezuela"):
        col=collectionVenezuela
    resultado=col.aggregate([{"$group":{"_id":"$polaridad","count":{"$sum":1}}}])
    insulto=0
    negativo=0
    neutro=0
    positivo=0
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
    return dataPolarity

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
def getTopTuiteros(request):
    topjep=[]
    topminga=[]
    topvenezuela=[]
    
    topCursor=collectionJep.aggregate([{"$project" : {"user.screen_name" : 1}},{"$group" : {"_id" : "$user.screen_name", "count" : {"$sum" : 1}}},{"$sort" : {"count" : -1}},{"$limit" : 10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topjep.append(x)
      

    topCursor=collectionMinga.aggregate([{"$project" : {"user.screen_name" : 1}},{"$group" : {"_id" : "$user.screen_name", "count" : {"$sum" : 1}}},{"$sort" : {"count" : -1}},{"$limit" : 10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topminga.append(x)
      

    topCursor=collectionVenezuela.aggregate([{"$project" : {"user.screen_name" : 1}},{"$group" : {"_id" : "$user.screen_name", "count" : {"$sum" : 1}}},{"$sort" : {"count" : -1}},{"$limit" : 10}])
    for top in topCursor:
        x =top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topvenezuela.append(x)
       

    
    context = { "jep": json.dumps(topjep),"minga":json.dumps(topminga),"venezuela":json.dumps(topvenezuela)}
    print (context)
    return render(request,"taller2/toptuiteros.html",context)

def getPalabrasClave(request):
    '''Metodo para extraer las palabras clave'''
    topjep=[]
    topminga=[]
    topvenezuela=[]

    topCursor=collectionJep.aggregate([{"$project": {"words": { "$split": ["$full_text_sw", " "] }}},{"$unwind": {"path": "$words"}},{"$group": {"_id": "$words","count": { "$sum": 1 }}},{"$sort":{"count":-1}},{"$limit":10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topjep.append(x)
    
    topCursor=collectionMinga.aggregate([{"$project": {"words": { "$split": ["$full_text_sw", " "] }}},{"$unwind": {"path": "$words"}},{"$group": {"_id": "$words","count": { "$sum": 1 }}},{"$sort":{"count":-1}},{"$limit":10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topminga.append(x)

    topCursor=collectionVenezuela.aggregate([{"$project": {"words": { "$split": ["$full_text_sw", " "] }}},{"$unwind": {"path": "$words"}},{"$group": {"_id": "$words","count": { "$sum": 1 }}},{"$sort":{"count":-1}},{"$limit":10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topvenezuela.append(x)
    
    context = { "jep": json.dumps(topjep),"minga":json.dumps(topminga),"venezuela":json.dumps(topvenezuela)}
    print (context)
    return render(request,"taller2/palabrasclave.html",context)
    
