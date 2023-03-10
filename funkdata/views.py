from django.shortcuts import render
from .models import Language, FunctionType, FunctionName, FunctionAll
import json
from json import dumps
import csv
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

def check_in_database(class_name):
    try:
        class_name.save()
    except IntegrityError:
        print (f"{class_name} duplicate ignored")
    else:
        print(f"added {class_name}")

def import_csv(request):
    file = open("funkdata/NewData.csv")
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    #print(header)
    rows = []
    for row in csvreader:
        rows.append(row)
    #print(rows)

    for row in rows:
        temp_language = Language(unique_language = row[0])
        check_in_database(temp_language)

        # After saving a new language, need to retrieve the newly created database entry
        temp_language = Language.objects.get(unique_language = row[0])

        temp_function_type = FunctionType(
                                           language = temp_language,
                                           unique_function_type = row[1],
                                          )
        check_in_database(temp_function_type)
        
        # After saving a new function_type, need to retrieve the newly created database entry
        # Without specifying the language, there can be >1 FunctionType objects with the same function_type, leading to an error
        # The syntax language__unique_language= traces back the language foreign key to the Language model.
        temp_function_type = FunctionType.objects.get(language__unique_language=row[0], unique_function_type = row[1])
        
        temp_function_name = FunctionName(language = temp_language,
                                          function_type = temp_function_type,
                                          unique_function_name = row[2])
        check_in_database(temp_function_name)

        # After saving a new function_name, need to retrieve the newly created database entry
        temp_function_name = FunctionName.objects.get(unique_function_name = row[2])

        temp_function_all = FunctionAll(language = temp_language,
                                        function_type = temp_function_type,
                                        function_name = temp_function_name,
                                        syntax = row[3],
                                        parameters = row[4],
                                        return_value = row[5],
        )
        check_in_database(temp_function_all)
        
    file.close()
    return render(request, "funkdata/import.html")

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
            #print(function_type_names)

        language_dict[language.unique_language] = function_type_dict
        #print(language_function_types)
    
    return language_dict

# Makes and sends the database dictionary, as well as a JSON dump of the same dictionary, to be used by javascript
def index(request):
    language_dict = database_to_dict()
    
    LFTJSON = dumps(language_dict)
    return render(request, "funkdata/index.html", {
        "LFTJson": LFTJSON,
        "LFTDjango": language_dict,
    })

# As in index
def new_function(request):
    language_dict = database_to_dict()

    return render(request, "funkdata/addnew.html", {
        "LFTDjango": language_dict,
    })

@csrf_exempt
def submit_new(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)

    print(data)
    

    temp_language = Language(unique_language = data["language"])
    check_in_database(temp_language)

    # After saving a new language, need to retrieve the newly created database entry
    temp_language = Language.objects.get(unique_language = data["language"])

    temp_function_type = FunctionType(
                                        language = temp_language,
                                        unique_function_type = data["function_type"],
                                        )
    check_in_database(temp_function_type)
    
    # After saving a new function_type, need to retrieve the newly created database entry
    # Without specifying the language, there can be >1 FunctionType objects with the same function_type, leading to an error
    # The syntax language__unique_language= traces back the language foreign key to the Language model.
    temp_function_type = FunctionType.objects.get(language__unique_language=data["language"], unique_function_type = data["function_type"])
    
    temp_function_name = FunctionName(language = temp_language,
                                        function_type = temp_function_type,
                                        unique_function_name = data["function_name"])
    check_in_database(temp_function_name)

    # After saving a new function_name, need to retrieve the newly created database entry
    temp_function_name = FunctionName.objects.get(unique_function_name = data["function_name"])

    temp_function_all = FunctionAll(language = temp_language,
                                    function_type = temp_function_type,
                                    function_name = temp_function_name,
                                    syntax = data["syntax"],
                                    parameters = data["parameters"],
                                    return_value = data["return_value"],
    )
    check_in_database(temp_function_all)

    return JsonResponse({"Status": "Data sent successfully"}, status=201)

@csrf_exempt
def delete_language(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)

    temp_language = Language(unique_language = data["language"])
    temp_language = Language.objects.get(unique_language = data["language"])

    temp_language.delete()

    return JsonResponse({"Status": "Data sent successfully"}, status=201)

@csrf_exempt
def delete_function_type(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)

    temp_language = Language(unique_language = data["language"])
    temp_language = Language.objects.get(unique_language = data["language"])

    temp_function_type = FunctionType(
                                    language = temp_language,
                                    unique_function_type = data["function_type"],
                                    )
    
    temp_function_type = FunctionType.objects.get(language__unique_language=data["language"], unique_function_type = data["function_type"])

    temp_function_type.delete()

    return JsonResponse({"Status": "Data sent successfully"}, status=201)

@csrf_exempt
def delete_function_name(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)

    temp_language = Language(unique_language = data["language"])
    temp_language = Language.objects.get(unique_language = data["language"])

    temp_function_type = FunctionType(
                                    language = temp_language,
                                    unique_function_type = data["function_type"],
                                    )
    
    temp_function_type = FunctionType.objects.get(language__unique_language=data["language"], unique_function_type = data["function_type"])

    temp_function_name = FunctionName(language = temp_language,
                                        function_type = temp_function_type,
                                        unique_function_name = data["function_name"])
    
    temp_function_name = FunctionName.objects.get(unique_function_name = data["function_name"])

    temp_function_name.delete()

    return JsonResponse({"Status": "Data sent successfully"}, status=201)