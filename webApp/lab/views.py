from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess
import paramiko
import sys

from .forms import RF2Form


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
    return HttpResponse("rf1 page")

