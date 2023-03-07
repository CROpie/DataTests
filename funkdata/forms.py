from django import forms

class NewFunctionForm(forms.Form):
     method_name = forms.CharField(max_length=64)
     arguments = forms.CharField(max_length=64)