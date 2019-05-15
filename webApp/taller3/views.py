from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId

from .forms import Question
# Create your views here.


client = MongoClient('bigdata-mongodb-04.virtual.uniandes.edu.co', 8087)
#client = MongoClient('localhost', 27017)
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
            print ('title---->'+str(title))
            summary = form.cleaned_data['summary']
            #summary = request.GET.get('summary')
            print ('summary---->'+str(summary))
            if (id!=None):
                query={'type':'pregunta',"id":{"$regex":"q/"+str(id)+"$"}}                
            elif (title!=None):
                query={'type':'pregunta','title': {'$regex': '.*'+title+'.*','$options':'si'}}
            else:
                query={'type':'pregunta','summary': {'$regex': '.*'+summary+'.*','$options':'si'}}
            
            print ("query===="+str(query))
            #questions= list( entities.find(query,{'id':1,'title':1,'summary':1}))   
            questions= list( entities.aggregate([{"$project":{"llave":"$_id","id":"$id","title":"$title","summary":"$summary","type":"$type"}},{"$match":query}]))   
            print(str(questions))    
    else:
        form=Question()

    return render(request, 'taller3/index.html', {'form':form ,'questions': questions })

def question(request,id):
    query={'type':'pregunta',"_id":ObjectId(id)}
    
    q= list( entities.find(query,{'id':1,'title':1,'summary':1}))   
    print (str(q))
    return render(request,'taller3/question.html',{'questions':q})


    

 
