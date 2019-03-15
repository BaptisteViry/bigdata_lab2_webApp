from django import forms

monthChoices = (('01','Enero'),('02','Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),
('07','Julio'),('08','Agosto'),('09','Septiembre'),('10','Octubre'), ('11','Noviembre'), ('12','Diciembre'))

dayChoices = (('1','Domingo'),('2','Lunes'),('3','Martes'),('4','Miercoles'),('5','Jueves'),('6','Viernes'),
('7','Sabado'))

class RF2Form (forms.Form):
    month=forms.ChoiceField(label='Mes', choices=monthChoices)    
    day=forms.ChoiceField(label='Dia', choices=dayChoices)
