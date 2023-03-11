from django import forms

# Not currently using forms, since the values to be entered come from a mixture of drop-downs and input fields
# May try to include them by using hidden input field = value of the dropdown...
# the attribute form-id in textfield etc may be useful..

class NewFunctionForm(forms.Form):
    language = forms.CharField(max_length=64)
    function_type = forms.CharField(max_length=64)
    function_name = forms.CharField(max_length=64)
    syntax = forms.CharField(max_length=64)
    parameters = forms.CharField(max_length=64)
    return_value = forms.CharField(max_length=64)

    def __str__(self):
        return f"{self.syntax},{self.parameters},{self.return_value}"