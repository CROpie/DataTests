from django import forms

class NewBeerForm(forms.Form):
     beername = forms.CharField(max_length=64)
     beerstyle = forms.CharField(max_length=64)