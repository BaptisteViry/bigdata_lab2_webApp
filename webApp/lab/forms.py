from django import forms

monthChoices = (('01','Enero'),('02','Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),
('07','Julio'),('08','Agosto'),('09','Septiembre'),('10','Octubre'), ('11','Noviembre'), ('12','Diciembre'))

dayChoices = (('1','Domingo'),('2','Lunes'),('3','Martes'),('4','Miercoles'),('5','Jueves'),('6','Viernes'),
('7','Sabado'))

yearChoices=(('2017','2017'),('2018','2018'))

class RF2Form (forms.Form):
    month=forms.ChoiceField(label='Mes', choices=monthChoices)    
    day=forms.ChoiceField(label='Dia', choices=dayChoices)

class RF1Form (forms.Form):
    year=forms.ChoiceField(label='Año',choices=yearChoices)
    month=forms.ChoiceField(label='Mes', choices=monthChoices)
    horaInicio=forms.IntegerField(label='Hora Inicio')       
    horaFin=forms.IntegerField(label='Hora Fin')

class RF3Form (forms.Form):
    year=forms.ChoiceField(label='Año',choices=yearChoices)
    month=forms.ChoiceField(label='Mes', choices=monthChoices)
    horaInicio=forms.IntegerField(label='Hora Inicio')       
    horaFin=forms.IntegerField(label='Hora Fin')
    day=forms.ChoiceField(label='Día',choices=dayChoices)
    top=forms.IntegerField(label='Defina top N')  
