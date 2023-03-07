from django.shortcuts import render
from .models import Language, FunctionType, FunctionInfo
from json import dumps

# Create your views here.

def showHowToSendJSON(request):
    # create data dictionary
    dataDictionary = {
        'hello': 'world',
        'geeks': 'forgeeks',
        'ABC': 123,
        'list': ['geeks', 4, 'geeks']
    }
    # dump data
    dataJSON = dumps(dataDictionary)
    return render(request, "funkdata/index.html", {
        'data': dataJSON})
    


# Makes a dictionary consisting of {language: [function_type-0, ... function_type-n], }, which can be utilized in django loops
# Also sends a JSON dump of the same dictionary, which is used by javascript

def index(request):
    language_function_types = {}
    languages = Language.objects.all()

    # Since foreign keys are being used, need to use a contains command to trace back the string.
    #JS_function_types = FunctionType.objects.filter(language__unique_language__contains="javascript")
    
    for language in languages:
        function_types = []

        language_functions = FunctionType.objects.filter(language__unique_language__contains=language.unique_language)

        for function in language_functions:
            function_types.append(str(function))
        language_function_types[language.unique_language] = function_types
         # Without str(), the function gets added as a Queryset, which causes issues down the line

    LFTJSON = dumps(language_function_types)
    return render(request, "funkdata/index.html", {
        "LFTJson": LFTJSON,
        "LFTDjango": language_function_types,

    })

    # Two foreign keys so two contains
    #JS_numbers_functions = FunctionInfo.objects.filter(language__unique_language__contains="javascript", function_type__unique_function_type__contains="numbers")
    #JS_strings_functions = FunctionInfo.objects.filter(language__unique_language__contains="javascript", function_type__unique_function_type__contains="strings")

def test(request):
    return render(request, "funkdata/testing.html")