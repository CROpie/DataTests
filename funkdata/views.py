from django.shortcuts import render
from .models import Language, FunctionType, FunctionInfo
from json import dumps

# Create your views here.

def index2(request):
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
    



def index(request):
    languages = Language.objects.all()
    # Since foreign keys are being used, need to use a contains command to trace back the string.
    #JS_function_types = FunctionType.objects.filter(language__unique_language__contains="javascript")
    language_function_types = {}
    for language in languages:
        language_functions = FunctionType.objects.filter(language__unique_language__contains=language.unique_language)
        function_types = []
        for function in language_functions:
            # Without str() the funtion gets added as a Queryset
            function_types.append(str(function))
        language_function_types[language.unique_language] = function_types
    print(language_function_types)

    LFTJSON = dumps(language_function_types)
    print(LFTJSON)
    return render(request, "funkdata/index.html", {
        #"language_database": languages,
        "LFTJson": LFTJSON,
        "LFTDjango": language_function_types,

    })

    # Two foreign keys so two contains
    #JS_numbers_functions = FunctionInfo.objects.filter(language__unique_language__contains="javascript", function_type__unique_function_type__contains="numbers")
    #JS_strings_functions = FunctionInfo.objects.filter(language__unique_language__contains="javascript", function_type__unique_function_type__contains="strings")

def test(request):
    return render(request, "funkdata/testing.html")