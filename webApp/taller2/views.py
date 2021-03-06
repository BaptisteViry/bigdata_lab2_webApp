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
    """Tamaño de cada colección"""
    countVenezuela = collectionVenezuela.find({}).count()
    countMinga = collectionMinga.find({}).count()
    countJep = collectionJep.find({}).count()
    countCollections = { 'countVenezuela':countVenezuela, 'countMinga':countMinga, 'countJep':countJep}
    context = { 'countCollections':countCollections }

    return render(request, "taller2/presentacionDB.html", context)

def charts(request):
    """Obtiene la polaridad global de cada colección"""
    ctxJep=getPolaridad("jep")
    ctxMinga=getPolaridad("minga")
    ctxVenezuela=getPolaridad("venezuela")

    #context = {'dataPolarity': dataPolarity}
    context = {'jep': ctxJep,'minga':ctxMinga,'venezuela':ctxVenezuela}
    #print (context)
    return render(request, "taller2/charts.html", context)

def getPolaridad(coleccion):
    """"Obtiene la polaridad de la colección enviada por parámetro"""
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
        #print(r)
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
    #print(hashtagsArray)
    context = { "hashtags": hashtagsArray}
    return render(request, "taller2/hashtagWordCloud.html", context)

def getTopTuiteros(request):
    """Obtener las cuentas que más tuitean"""
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
    #print (context)
    return render(request,"taller2/toptuiteros.html",context)

def getLugares(request):
    """Obtener todos los lugares"""
    topjep=[]
    topminga=[]
    topvenezuela=[]
    
    #topCursor=collectionVenezuela.aggregate([{"$match":{"geo":{"$ne":None}}},{"$project":{"geo.coordinates":-1,"full_text":1}}])
    #topCursor=collectionVenezuela.aggregate([{"$match":{"geo":{"$ne":None}}},{"$project":{"geo.coordinates":-1}},{"$group" : {"_id" : "$geo.coordinates", "count" : {"$sum" : 1}}}])
    topCursor=collectionVenezuela.aggregate([{"$match":{"$and":[{"place.country":{"$ne":""}},{"place.country":{"$ne":None}}]}},{"$project":{"place.country":-1}},{"$group" : {"_id" : "$place.country", "count" : {"$sum" : 1}}}])
    for top in topCursor:

        x = top['_id'],top['count']
        topjep.append(x)

    context = { "jep": json.dumps(topjep),"minga":json.dumps(topminga),"venezuela":json.dumps(topvenezuela)}
    print (context)
    return render(request,"taller2/lugares.html",context)

def getTopLugares(request):
    """Obtener las cuentas que más tuitean"""
    topjep=[]
    topminga=[]
    topvenezuela=[]
    
    topCursor=collectionJep.aggregate([{"$match":{"user.location":{"$ne":""}}},{"$project" : {"user.location" : 1}},{"$group" : {"_id" : "$user.location", "count" : {"$sum" : 1}}},{"$sort" : {"count" : -1}},{"$limit" : 10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topjep.append(x)
      

    topCursor=collectionMinga.aggregate([{"$project" : {"user.location" : 1}},{"$group" : {"_id" : "$user.location", "count" : {"$sum" : 1}}},{"$sort" : {"count" : -1}},{"$limit" : 10}])
    for top in topCursor:
        x = top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topminga.append(x)
      

    topCursor=collectionVenezuela.aggregate([{"$project" : {"user.location" : 1}},{"$group" : {"_id" : "$user.location", "count" : {"$sum" : 1}}},{"$sort" : {"count" : -1}},{"$limit" : 10}])
    for top in topCursor:
        x =top["_id"],top['count'],'color: #{:06x}'.format(randint(0, 256**3))
        topvenezuela.append(x)
       

    
    context = { "jep": json.dumps(topjep),"minga":json.dumps(topminga),"venezuela":json.dumps(topvenezuela)}
    #print (context)
    return render(request,"taller2/toplugares.html",context)

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
    #print (context)
    return render(request,"taller2/palabrasclave.html",context)

def getApoyoCuenta(request, coleccion, screen_name):
    """Obtener apoyo o rechazo a una cuenta"""
      
    if (coleccion=="jep_1"):
        miColeccion=collectionJep
    elif (coleccion=="minga_1"):
        miColeccion=collectionMinga
    else :
        miColeccion=collectionVenezuela
    curPolaridad=miColeccion.aggregate([{"$match" : {"in_reply_to_screen_name" : screen_name } },{"$group" : {"_id": "$polaridad","count":{"$sum":1}}}])
    insulto=0
    negativo=0
    neutro=0
    positivo=0
    for r in curPolaridad:        
        #print(r)
        if (r.get("_id")=="Insulto"):
            insulto=r.get("count")
        elif (r.get("_id")=="Negativo"):
            negativo=r.get("count")
        elif (r.get("_id")=="Neutro"):
            neutro=r.get("count")
        elif (r.get("_id")=="Positivo"):
            positivo=r.get("count")
        
    dataPolarity = { 'Positivo':positivo, 'Neutro':neutro, 'Negativo':negativo, 'Insulto':insulto }   
    datos={'coleccion':coleccion,'screen_name':screen_name}
    context={'polaridad':dataPolarity,'datos':datos}
    #print (context)
    return render(request,"taller2/apoyocuenta.html",context)


def getPolaridadCuenta(request, coleccion, screen_name):
    """Obtener la polaridad de una cuenta en una colección"""

    
    if (coleccion=="jep_1"):
        miColeccion=collectionJep
    elif (coleccion=="minga_1"):
        miColeccion=collectionMinga
    else :
        miColeccion=collectionVenezuela
    curPolaridad=miColeccion.aggregate([{"$match" : {"user.screen_name" : screen_name } },{"$group" : {"_id": "$polaridad","count":{"$sum":1}}}])
    insulto=0
    negativo=0
    neutro=0
    positivo=0
    for r in curPolaridad:        
        #print(r)
        if (r.get("_id")=="Insulto"):
            insulto=r.get("count")
        elif (r.get("_id")=="Negativo"):
            negativo=r.get("count")
        elif (r.get("_id")=="Neutro"):
            neutro=r.get("count")
        elif (r.get("_id")=="Positivo"):
            positivo=r.get("count")
        
    dataPolarity = { 'Positivo':positivo, 'Neutro':neutro, 'Negativo':negativo, 'Insulto':insulto }

  
    
    datos={'coleccion':coleccion,'screen_name':screen_name}
    context={'polaridad':dataPolarity,'datos':datos}
    #print (context)
    return render(request,"taller2/polaridad.html",context)

def getApoyoGeneral(request):
    """Consulta la polaridad en las respuesta, por temas"""
    ctxJep=getApoyoTema("jep")
    ctxMinga=getApoyoTema("minga")
    ctxVenezuela=getApoyoTema("venezuela")

    #context = {'dataPolarity': dataPolarity}
    context = {'jep': ctxJep,'minga':ctxMinga,'venezuela':ctxVenezuela}
    #print("analizando retweets")
    #print (context)
    return render(request, "taller2/apoyo.html", context)


def getApoyoTema(coleccion):
    if (coleccion=="jep"):
        col=collectionJep
    elif(coleccion=="minga"):
        col=collectionMinga
    elif(coleccion=="venezuela"):
        col=collectionVenezuela
    resultado=col.aggregate([{"$match":{"in_reply_to_status_id_str" : {"$ne":None} }},{"$group":{"_id":"$polaridad","count":{"$sum":1}}}])
    insulto=0
    negativo=0
    neutro=0
    positivo=0
    for r in resultado:                
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
