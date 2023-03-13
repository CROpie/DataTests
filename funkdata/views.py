from django.shortcuts import render
from .models import Language, FunctionType, FunctionName, FunctionAll
import json
from json import dumps
import csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Makes a dictionary consisting of {language: {function_type: {function_name: { function_data[] }}}}, which can be utilized in django loops
def database_to_dict():
    language_dict = {}
    languages = Language.objects.all()
    
    for language in languages:
        function_type_dict= {}

        # For a given language, retrieve all the FunctionType objects as a queryset
        # Since foreign keys are being used, need to use a contains command to trace back the string.
        function_types = FunctionType.objects.filter(language__unique_language__contains=language.unique_language)

        for function_type in function_types:
            function_names = FunctionName.objects.filter(language__unique_language__contains=language.unique_language, 
                                                         function_type__unique_function_type__contains=function_type.unique_function_type)
            function_name_dict = {}

            for function_name in function_names:
                function_data = FunctionAll.objects.filter(language__unique_language__contains=language.unique_language,
                                                           function_type__unique_function_type__contains=function_type.unique_function_type,
                                                           function_name__unique_function_name__contains=function_name.unique_function_name)
                function_data_list = []

                # Iterate over the queryset then add each into a list
                # Without str(), the data gets added as a Queryset, which causes issues down the line
                for function_datum in function_data:
                    function_data_list.append(str(function_datum))

                function_name_dict[function_name.unique_function_name] = function_data_list

            function_type_dict[function_type.unique_function_type] = function_name_dict

        language_dict[language.unique_language] = function_type_dict
    
    return language_dict

# Makes and sends the database dictionary, as well as a JSON dump of the same dictionary, to be used by javascript
def index(request):
    language_dict = database_to_dict()
    
    LFTJSON = dumps(language_dict)
    return render(request, "funkdata/index.html", {
        "LFTJson": LFTJSON,
        "LFTDjango": language_dict,
    })

@csrf_exempt
def deleteData(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)

    temp_language = Language.objects.get(unique_language = data["language"])

    if data["item_to_delete"] == "language":
        temp_language.delete()
        return JsonResponse({"Status": "Language deleted successfully"}, status=201)
    
    # .get(language__unique_language = data["language"] also works
    temp_function_type = FunctionType.objects.get(language = temp_language,
                                                  unique_function_type = data["function_type"])
    
    if data["item_to_delete"] == "function_type":
        temp_function_type.delete()
        return JsonResponse({"Status": "Function type deleted successfully"}, status=201)

    temp_function_name = FunctionName.objects.get(language = temp_language,
                                                  function_type = temp_function_type,
                                                  unique_function_name = data["function_name"])

    if data["item_to_delete"] == "function_name":
        temp_function_name.delete()
        return JsonResponse({"Status": "Function deleted successfully"}, status=201)

@csrf_exempt
def modifyData(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)

    temp_language = Language.objects.get(unique_language = data["language"])

    temp_function_type = FunctionType.objects.get(language = temp_language,
                                                  unique_function_type = data["function_type"])

    temp_function_name = FunctionName.objects.get(language = temp_language,
                                                  function_type = temp_function_type,
                                                  unique_function_name = data["function_name"])

    # Retrieve the current FunctionAll object in the database, and remove it
    old_function_all = FunctionAll.objects.get(language = temp_language,
                                               function_type = temp_function_type,
                                               function_name = temp_function_name)
    old_function_all.delete()

    # Put in the values for the 'modified' FunctionAll object, and store it
    temp_function_all = FunctionAll(language = temp_language,
                                    function_type = temp_function_type,
                                    function_name = temp_function_name,
                                    syntax = data["syntax"],
                                    parameters = data["parameters"],
                                    return_value = data["return_value"],
                                    example = data["example"],
                                    misc = data["misc"],)
    temp_function_all.save()

    return JsonResponse({"Status": "Data modified successfully"}, status=201)

# created is the second return value from .get_or_create, will be an (irrelevant?) bool
@csrf_exempt
def submitNew(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    print(data)

    temp_language, created = Language.objects.get_or_create(unique_language = data["language"])

    temp_function_type, created = FunctionType.objects.get_or_create(language = temp_language, 
                                                                     unique_function_type = data["function_type"])

    temp_function_name, created = FunctionName.objects.get_or_create(language = temp_language, 
                                                                     function_type = temp_function_type, 
                                                                     unique_function_name = data["function_name"])

    temp_function_all, created = FunctionAll.objects.get_or_create(language = temp_language,
                                                                   function_type = temp_function_type,
                                                                   function_name = temp_function_name,
                                                                   syntax = data["syntax"],
                                                                   parameters = data["parameters"],
                                                                   return_value = data["return_value"],
                                                                   example = data["example"],
                                                                   misc = data["misc"],)

    return JsonResponse({"Status": "Data sent successfully"}, status=201)

def import_csv(request):
    file = open("funkdata/NewData.csv")
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    
    rows = []
    for row in csvreader:
        rows.append(row)

    # Just like the submitNew function, but using a list instead
    for row in rows:

        temp_language, created = Language.objects.get_or_create(unique_language = row[0])

        temp_function_type, created = FunctionType.objects.get_or_create(language = temp_language, 
                                                                        unique_function_type = row[1])

        temp_function_name, created = FunctionName.objects.get_or_create(language = temp_language, 
                                                                        function_type = temp_function_type, 
                                                                        unique_function_name = row[2])

        temp_function_all, created = FunctionAll.objects.get_or_create(language = temp_language,
                                                                    function_type = temp_function_type,
                                                                    function_name = temp_function_name,
                                                                    syntax = row[3],
                                                                    parameters = row[4],
                                                                    return_value = row[5],
                                                                    example = row[6],
                                                                    misc = row[7],)
        
    file.close()
    return render(request, "funkdata/import.html")