from django.shortcuts import render
from .models import Language, FunctionType, FunctionInfo
from json import dumps

# Create your views here.

def index(request):
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
    



def index2(request):
    languages = Language.objects.all()
    for language in languages:
        print(language)
    # Since foreign keys are being used, need to use a contains command to trace back the string.
    #JS_function_types = FunctionType.objects.filter(language__unique_language__contains="javascript")
    language_function_types = {}
    for language in languages:
        language_functions = FunctionType.objects.filter(language__unique_language__contains=language.unique_language)
        function_types = []
        for function in language_functions:
            print(function)
            # Without str() the funtion gets added as a Queryset
            function_types.append(str(function))
            print(function_types)
        language_function_types[language.unique_language] = function_types
 
    print(language_function_types)


    # Two foreign keys so two contains
    #JS_numbers_functions = FunctionInfo.objects.filter(language__unique_language__contains="javascript", function_type__unique_function_type__contains="numbers")
    #JS_strings_functions = FunctionInfo.objects.filter(language__unique_language__contains="javascript", function_type__unique_function_type__contains="strings")
    return render(request, "funkdata/index.html", {
        "language_database": languages,
        "language_function_types": language_function_types,
        #"javascript_numbers": JS_numbers_functions,
        #"javascript_strings": JS_strings_functions,
    })