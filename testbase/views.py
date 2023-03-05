from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

from .models import Beer

beers = []

class NewBeerForm(forms.Form):
     beername = forms.CharField(max_length=64)
     beerstyle = forms.CharField(max_length=64)

# Create your views here.

def index(request):
    return render(request, "testbase/index.html")

def addbeer(request):
    return render(request, "testbase/new_beer.html", {
                  "form": NewBeerForm()
    })
                

"""
the beers variable stores the entire database
this is sent to show_beer.html
"beerslist" is the string which is required in show_beer.html
ie {% for beer in beerslist %}

"""
def showbeer(request):
    beers = Beer.objects.all()
    return render(request, "testbase/show_beer.html", {
        "beerslist": beers,
    })

"""
(perhaps not dictionary, but QuerySet or something like that..)
print() will print to the command line where the server is running
print(form) gives a whole lot of info, as well as a dictionary containing the info of the new beer.
<input type="text" name="beername" value="rogers" maxlength="64" required id="id_beername">
<input type="text" name="beerstyle" value="Stout" maxlength="64" required id="id_beerstyle">
"beername" and "beerstyle" are automatically made into the key of the dictionary, these come from the NewBeerForm class
form = form.cleaned_data will remove everything but the form
values from the dictionary can be stored as variables (maybe can do simultaneously in next step?)
A new variable of the model/class in models.py is fed the values
When this is saved, a new entry is made in the database with id automatically +1

HttpResponseRedirect sends the user to a page after running to script. Good practice to include, to prevent re-submitting data

**** HttpReponse() can't print out things like form or dictionaries, goodbye ~3 hours! Oops

"""

def submitbeer(request):
    form = NewBeerForm(request.POST)
    if request.method == 'POST':
        form = NewBeerForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            print(form)
            beername = form["beername"]
            beerstyle = form["beerstyle"]
            beer = Beer (
                name=beername,
                style=beerstyle,
            )
            beer.save()
            return HttpResponseRedirect("new_beer")
        