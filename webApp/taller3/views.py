from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
from SPARQLWrapper import SPARQLWrapper, JSON
import json 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import threading


from .forms import Question

# Create your views here.


client = MongoClient('bigdata-mongodb-04.virtual.uniandes.edu.co', 8087)
#client = MongoClient('localhost', 27017)
db = client.Grupo10_Taller3
entities = db.music_questions_entities
tweets=db.music_twitter




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
            print ("--->"+str(id)+","+str(title)+","+str(summary))
            if (id!=None):
                query={'type':'pregunta',"id":{"$regex":"q/"+str(id)+"$"}}                
            elif (len(title)!=0):
                query={'type':'pregunta','title': {'$regex': '.*'+title+'.*','$options':'si'}}
            else:
                #query={'type':'pregunta','summary': {'$regex': '.*'+summary+'.*','$options':'si'}}
                 query={'$text': { '$search': summary }}
            
            print ("query===="+str(query))
            #questions= list( entities.find(query,{'_id':1,'id':1,'title':1,'summary':1,'type':1}))
            questions= list( entities.aggregate([{"$match":query},{"$project":{"llave":"$_id","id":"$id","title":"$title","summary":"$summary","type":"$type"}}]))   
            #print(str(questions))    
    else:
        form=Question()

    return render(request, 'taller3/index.html', {'form':form ,'questions': questions })

def question(request,id):
    #query={'type':'pregunta',"_id":ObjectId(id)}
    query={"_id":ObjectId(id)}
    
    q= list( entities.find(query,{'id':1,'title':1,'summary':1,'re_rank':1,'socialTags':1,'topics':1,'entities':1}))   
    print (str(q))

    queryrespuesta={'type':'respuesta',"preguntaId":q[0]['id']}
    print (str(queryrespuesta))
    q2= list( entities.aggregate([{'$project':{"llave":"$_id","id":"$id","title":"$title","summary":"$summary","re_rank":"$re_rank","socialTags":"$socialTags","topics":"$topics","entities":"$entities","type":"$type","preguntaId":"$preguntaId"}},{"$match":queryrespuesta}]))   
    print ("__________________________________________")
    print(str(q2))
    print ("__________________________________________")

    return render(request,'taller3/question.html',{'question':q[0],'answers':q2})

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
    print ("Resultado: "+str(resultado))
    return resultado

    
def queryPersona( name ):

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
    prefix dbo: <http://dbpedia.org/ontology/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix : <http://dbpedia.org/resource/>

    SELECT ?name ?birthName ?birth ?birthPlace ?spouse ?ubicacion ?person ?artistas
    WHERE {      
            ?person foaf:name ?name .
            ?person foaf:name \""""+name+"""\"@en .
            OPTIONAL{?person dbo:birthDate ?birth}
            OPTIONAL{?person dbo:birthName ?birthName}
            OPTIONAL{?person dbo:birthPlace ?birthPlace}
            OPTIONAL{?person dbo:spouse ?spouse}
			OPTIONAL{?person dbo:partner ?spouse}
			OPTIONAL{?person dbo:residence ?ubicacion}
			  
       } LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def queryRelacionados( name ):

    name = name.replace(" ", "_")
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
    prefix dbo: <http://dbpedia.org/ontology/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix : <http://dbpedia.org/resource/>

    SELECT * WHERE { dbr:"""+name+"""^dbo:associatedMusicalArtist ?variable. }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def map(request,lugar):
    resultado=get_lugar(lugar)
   
    lugar=[]
    x=float(resultado['geolat']),float(resultado['geolong']),resultado["lugar"]
    lugar.append(x)
    print (lugar)
    return render(request,'taller3/mapa.html',{"lugar":json.dumps(lugar)})

def persona(request,persona):
    datospersona=queryPersona(persona)["results"]["bindings"]
    if (datospersona):
        datospersona=datospersona[0]        
    datosrelacionados=queryRelacionados(persona)["results"]["bindings"]
    if (datosrelacionados):
        datosrelacionados=datosrelacionados[0]
    #print ('datospersona'+str(datospersona))
    #print ('datosrelacionados'+str(datosrelacionados))
    dataSpotify = artistSpotify(persona)
    return render(request,'taller3/person.html',{"persona":datospersona,"relacionados":datosrelacionados,"dataSpotify":dataSpotify})


def buscartopic(request, topic):
    resultado=list(entities.aggregate([{"$project":{ "_id":0,  "llave":"$_id",  "title":"$title",  "summary":"$summary",  "re_rak":"$re_rank",  "topics":"$topics"}},{"$match":{"topics":topic}}]))
    #print ("Resultado: "+str(resultado))
    return render(request,'taller3/buscartopic.html',{"resultados":resultado})

def artistSpotify(name):
    #app IDs spotify API
    client_id = "cadc150f1756478182ad73e997a16c93"
    client_secret = "0064a9f31d284866a4afd6cc86001d03"

    #verification of the IDs
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    #connection spotify API
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.search(q='artist:' + name, type='artist')
    if(results["artists"]["items"] != []):
        dataSpotify = results["artists"]["items"][0]
        return dataSpotify

 
def strTwitter(request, searchText):
    thread1 = threading.Thread(target = lanzarcreacion, args = (searchText,))
    thread1.start()
    #lanzarcreacion(searchText)
    print ("se inició el hilo de recuperación de datos")
    return render(request, 'taller3/streamTwitter.html')

def lanzarcreacion(searchText):
    CONSUMER_KEY = "nqWae4EAcs4xSn9rVK4T0gZzS" 
    CONSUMER_SECRET = "ekuALYxFHFxMxR7yQitc8fCg0XcWuaI3flMaBdNgyKnZtcsGJ7"
    ACCESS_TOKEN = "4546199003-O19nOXfirpmgzMSuWJotbMNGYgAdHNpM7uyPqGz"
    ACCESS_SECRET = "n2DQkLg0QLUprm1bgR9NrvRF6F3oLWL2CuEmK4pKBDZ5J" 

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    #searchText = " Michael  Jackson "
    print ("se va a iniciar el listener..........")

    lisRead  =  listener()
    twitterStream = Stream(auth, lisRead, lang='en', tweet_mode='extended')
    twitterStream.filter(track=[searchText])

def socialtag(request, tag):
    query={'$text': { '$search': tag }}
    print (str (query))
    mytweets= list( tweets.aggregate([{"$match":query},{"$project":{"llave":"$_id","full_text":"$full_text","name":"$user.name","date":"$created_at"}}]))       
    print(str(mytweets))
    return render(request, 'taller3/tag.html',{"tweets":mytweets})
 
class listener(StreamListener):

    limit = 5
    count = 0
    datos = []

    
    def __init__(self, lim=10):        
        self.limit=lim


    def on_status(self, status):
        print ("status...."+ status.text)
        self.count+=1
        return False if self.count == self.limit else True

    def on_data(self, data):

        print(data)
        self.datos.append(json.loads(data))    
        print ("creando.......")
        tweets.insert_one(json.loads(data))        
        print (".......Dato creado: ")
        self.count+=1
        if self.count == self.limit:
            print("SALIDA POR LIMITE")
        return False if self.count == self.limit else True

    def on_error(self, status):
        print(status)
        return(False)
