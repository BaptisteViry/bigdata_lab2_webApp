from django import forms

class Question (forms.Form):
    id=forms.IntegerField(label='Id',required=False)
    title=forms.CharField(label='Title',required=False)
    summary=forms.CharField(label='Summary',required=False)       
    