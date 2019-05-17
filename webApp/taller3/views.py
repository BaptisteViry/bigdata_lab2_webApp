from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
from SPARQLWrapper import SPARQLWrapper, JSON
import json 


from .forms import Question
# Create your views here.


#client = MongoClient('bigdata-mongodb-04.virtual.uniandes.edu.co', 8087)
client = MongoClient('localhost', 27017)
db = client.Grupo10_Taller3
entities = db.music_questions_entities

def index(request):
    questions=""
    if request.method=='POST':
        form=Question(request.POST)
        query=''
        if form.is_valid():
            id = form.cleaned_data['id']
            #id=request.GET.get('id')
            title=form.cleaned_data['title']
            ##title=request.GET.get('title')
            #print ('title---->'+str(title))
            summary = form.cleaned_data['summary']
            #summary = request.GET.get('summary')
            #print ('summary---->'+str(summary))
            if (id!=None):
                query={'type':'pregunta',"id":{"$regex":"q/"+str(id)+"$"}}                
            elif (title!=None):
                query={'type':'pregunta','title': {'$regex': '.*'+title+'.*','$options':'si'}}
            else:
                query={'type':'pregunta','summary': {'$regex': '.*'+summary+'.*','$options':'si'}}
            
            #print ("query===="+str(query))
            #questions= list( entities.find(query,{'id':1,'title':1,'summary':1}))   
            questions= list( entities.aggregate([{"$project":{"llave":"$_id","id":"$id","title":"$title","summary":"$summary","type":"$type"}},{"$match":query}]))   
            #print(str(questions))    
    else:
        form=Question()

    return render(request, 'taller3/index.html', {'form':form ,'questions': questions })

def question(request,id):
    query={'type':'pregunta',"_id":ObjectId(id)}
    
    q= list( entities.find(query,{'id':1,'title':1,'summary':1,'re_rank':1,'socialTags':1,'topics':1,'entities':1}))   
    print (str(q))
    return render(request,'taller3/question.html',{'questions':q})

def lugar(request, lugar):
    resultado=get_lugar(lugar)
    print (resultado)
    return render(request,'taller3/lugar.html',{'lugar':resultado})

def get_lugar(lugar):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
    prefix dbo: <http://dbpedia.org/ontology/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix : <http://dbpedia.org/resource/>

    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    SELECT * WHERE {
    ?x rdfs:label \""""+lugar+"""\"@en .
    OPTIONAL{?x dbo:country ?country }.  
    OPTIONAL{?x dbo:department ?department}.
    OPTIONAL{?x geo:lat ?geolat} .
    OPTIONAL{?x geo:long ?geolong} .

    } limit 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print (results)
    print ('---------------')
    resultado={}
    for result in results["results"]["bindings"]:
        try:
            resultado['x']=result['x']['value']
        except Exception as e:
            print (e)
        try:
            resultado['country']=result['country']['value']
        except Exception as e:
            print (e)
        try:
            resultado['department']=result['department']['value']
        except Exception as e:
            print (e)
        try:
            resultado['geolat']=result['geolat']['value']
        except Exception as e:
            print (e)
        try:
            resultado['geolong']=result['geolong']['value']
        except Exception as e:
            print (e)
        
        resultado['lugar']=lugar
       
    return resultado

def map(request,lugar):
    resultado=get_lugar(lugar)
   
    lugar=[]
    x=float(resultado['geolat']),float(resultado['geolong']),resultado["lugar"]
    lugar.append(x)
    print (lugar)
    return render(request,'taller3/mapa.html',{"lugar":json.dumps(lugar)})



    

 
