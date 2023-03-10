from django import forms

class NewFunctionForm(models.Model):
    language = forms.CharField(max_length=64)
    function_type = forms.CharField(max_length=64)
    function_name = forms.CharField(max_length=64)
    syntax = forms.CharField(max_length=64)
    parameters = forms.CharField(max_length=64)
    return_value = forms.CharField(max_length=64)

    def __str__(self):
        return f"{self.syntax},{self.parameters},{self.return_value}"