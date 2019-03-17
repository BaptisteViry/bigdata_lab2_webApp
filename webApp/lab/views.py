from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess
import paramiko
import sys
import pandas as pd

from .forms import RF1Form
from .forms import RF2Form
from .forms import RF3Form



# Create your views here.
def index(request):
    return render(request, "lab/home.html")

def rf2(request):

    month=""
    day=""
    resultado=""

    def printOut(stdout):
        resultado=""
        for line in iter(lambda: stdout.readline(2048), ""):
            resultado+="  "+line
            print(line)




    if request.method=='POST':
        form=RF2Form(request.POST)

        if form.is_valid():
            month = form.cleaned_data['month']
            day = form.cleaned_data['day']
            output=""
            command = "baptiste/test/test.sh "+month+" "+day

            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname="bigdata-cluster1-ambari.virtual.uniandes.edu.co",username="bigdata10",password="cVCGoui239m")
            stdin,stdout,stderr=ssh_client.exec_command(command)
            resultado = printOut(stdout)
            stdin2,stdout2,stderr2=ssh_client.exec_command("hadoop fs -cat /tmp/taxis/2/*")

            for line in iter(lambda: stdout2.readline(2048), ""):
                output+="\n"+line

            x = output.split("\n")
            taxi1 = x[1].split("\t")
            taxi2 = x[3].split("\t")
            
            print(x)
            print(taxi1)
            print(taxi2)
            
            tipo1=taxi1[0]
            average1=taxi1[1].split(" ")[2]
            min1=taxi1[2].split(" ")[3]
            max1=taxi1[3].split(" ")[3]
            countTaxi1=taxi1[4].split(" ")[3]
             
            tipo2=taxi2[0]
            average2=taxi2[1].split(" ")[2]
            min2=taxi2[2].split(" ")[3]
            max2=taxi2[3].split(" ")[3]
            countTaxi2=taxi2[4].split(" ")[3]
            countTotal=taxi2[5].split(" ")[4]   

            context={'form': form,'day':day,'month':month, 'type1':tipo1,'average1':average1,'min1':min1,
            'max1':max1,'countTaxi1':countTaxi1,'type2':tipo2,'average2':average2,'min2':min2,
            'max2':max2,'countTaxi2':countTaxi2,'countTotal':countTotal}  
            
            print(taxi2[2].split(" ")[3])


            return render(request, 'lab/rf2.html', context)

    else:
        form=RF2Form()
        return render(request, 'lab/rf2.html', {'form': form,'day':day,'month':month, resultado:"stdout"})





    


    #out = subprocess.Popen(['sshpass', '-p','cVCGoui239m', 'ssh', 'bigdata10@bigdata-cluster1-ambari.virtual.uniandes.edu.co', 'uname','-a'], 
    #    universal_newlines=True,
    #    stdout=subprocess.PIPE, 
    #    stderr=subprocess.STDOUT,
	#    )
    #stdout,stderr = out.communicate()

   # return render(request, 'lab/rf2.html', {'resultado':"stdout.readlines()"})

def rf1(request):
    def printOut(stdout):
        resultado=""
        for line in iter(lambda: stdout.readline(2048), ""):
            resultado+="  "+line
            print(line)

    resultado=0
    zonas=pd.read_csv('zonas.csv')
    print(zonas.head())
    print(zonas.dtypes)
    if request.method=='POST':
        form=RF1Form(request.POST)

        if form.is_valid():
            year=form.cleaned_data['year']
            month = form.cleaned_data['month']
            horaInicio = form.cleaned_data['horaInicio']
            horaFin=form.cleaned_data['horaFin']
            
            output=""
            command = "pedro/runRF1.sh "+year+" "+month+" "+str(horaInicio)+" "+str(horaFin)

            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #ssh_client.connect(hostname="bigdata-cluster1-ambari.virtual.uniandes.edu.co",username="bigdata10",password="cVCGoui239m")
            ssh_client.connect(hostname="192.168.0.16",username="maria_dev",password="maria_dev",port=2222)
            stdin,stdout,stderr=ssh_client.exec_command(command)
          
            for line in iter(lambda: stdout.readline(2048), ""):
                output+="\n"+line
            print("err")

            printOut(stderr)

            print ("RTA____:\n"+output)

            #printOut(stderr)
            #output=output.replace("\n","<br>")
            #output=output.replace("\t","|")
            #print ("RTA:\n"+output)

            lineas=output.split("\n")
            print("Lineas: "+str(lineas))
            data=[]
            total=0
            zona='';
            
            for linea in lineas:
                if (len(linea)==0 or len(linea)==2):
                    continue
                cols=linea.split("\t")
                print("linea: "+linea+"->")
                print(cols)
                if (len(cols)==2):
                    total=cols[1]
                    continue
                data.append(Registro(cols[0],cols[1],cols[2],cols[3],cols[4]))

            data= pd.DataFrame.from_records([s.to_dict() for s in data])
            print('_______________')
            print (data.head())
            print (data.dtypes)
            data.LocationID=data.LocationID.astype('int64')            
            data=pd.merge(zonas,data,how='inner',on='LocationID')
            print (data.head())
            print (data.dtypes)
            #zona=data[0].Zone            
            context={'form': form,'data':data,'total':total,'zona':zona} 
            return render(request, 'lab/rf1.html', context)

    else:
        form=RF1Form()
    
   
    return render(request, 'lab/rf1.html', {'form': form,'resultado':resultado})

def rf3(request):
    def printOut(stdout):
        resultado=""
        for line in iter(lambda: stdout.readline(2048), ""):
            resultado+="  "+line
            print(line)

    resultado=0
    zonas=pd.read_csv('zonas.csv')
    if request.method=='POST':
        form=RF3Form(request.POST)

        if form.is_valid():
            year=form.cleaned_data['year']
            month = form.cleaned_data['month']
            horaInicio = form.cleaned_data['horaInicio']
            horaFin=form.cleaned_data['horaFin']
            day=form.cleaned_data['day']
            top=form.cleaned_data['top']
            
            output=""
            command = "mauricio/runRF3.sh "+year+" "+month+" "+str(horaInicio)+" "+str(horaFin) + " " + day + " " + str(top) 

            print(command)

            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname="bigdata-cluster1-ambari.virtual.uniandes.edu.co",username="bigdata10",password="cVCGoui239m")
            stdin,stdout,stderr=ssh_client.exec_command(command)
          
            print(stdout)

            for line in iter(lambda: stdout.readline(2048), ""):
                output+="\n"+line
           
            #print ("RTA____:\n"+output)

            lineas=output.split("\n")
            print("Lineas: "+str(lineas))
            data=[]
            dataTop=[]
            
            for linea in lineas:
                if (len(linea)==0 or len(linea)==2):
                    continue
                cols=linea.split("\t")
                print("linea: "+linea+"->")
                print(cols)
                print(len(cols))
                if ( len(cols) <= 2 ):
                    continue
                if( len(cols) == 5 ):
                    data.append(RegistroTop(cols[0],cols[2],cols[4]))
                if( len(cols) == 2 ):
                    dataTop.append(RegistroTop(cols[0],cols[4],cols[4]))
                print(dataTop)

            data= pd.DataFrame.from_records([s.to_dict() for s in data])
            data.LocationID=data.LocationID.astype('int64')            
            data=pd.merge(zonas,data,how='inner',on='LocationID')

            print(data)
            print(dataTop)

            dataTop= pd.DataFrame.from_records([s.to_dict() for s in dataTop])
            dataTop.LocationID=dataTop.LocationID.astype('int64')            
            dataTop=pd.merge(zonas,dataTop,how='inner',on='LocationID')

            
            context={'form': form,'data':data, 'datatop':dataTop } 
            return render(request, 'lab/rf3.html', context)

    else:
        form=RF3Form()

    return render(request, 'lab/rf3.html', {'form': form,'resultado':resultado})

class RegistroTop:
    def __init__(self, LocationID, mes, cantidad):
        self.LocationID = LocationID
        self.mes = mes
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'LocationID':self.LocationID,
            'mes':self.mes,
            'cantidad':self.cantidad
        }

class Registro:
    def __init__(self, LocationID, dia, hora, cantidad, tipo):
        self.LocationID = LocationID
        self.dia = dia
        self.hora = hora
        self.cantidad = cantidad
        self.tipo = tipo

    def to_dict(self):
        return {
            'LocationID':self.LocationID,
            'dia':self.dia,
            'hora':self.hora,
            'cantidad':self.cantidad,
            'tipo':self.tipo
        }