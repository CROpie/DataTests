from django.shortcuts import render
from .models import Language, FunctionType, FunctionName, FunctionAll
from json import dumps
import csv
from django.db import IntegrityError

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


# Makes a dictionary consisting of {language: [function_type-0, ... function_type-n], }, which can be utilized in django loops
# Also sends a JSON dump of the same dictionary, which is used by javascript

def index(request):
    language_function_types = {}
    languages = Language.objects.all()
    
    for language in languages:
        print(language)
        print("------------------")
        function_type_names = {}

        # For a given language, retrieve all the FunctionType objects as a queryset
        # Since foreign keys are being used, need to use a contains command to trace back the string.
        function_types = FunctionType.objects.filter(language__unique_language__contains=language.unique_language)
        print(function_types)
        # Iterate over the queryset then add each into a list called function_types
        # Without str(), the function gets added as a Queryset, which causes issues down the line
        #for function_type in language_functions:
        #    function_types.append(str(function_type))
        
        for function_type in function_types:
            print("------------------")
            function_names = FunctionName.objects.filter(language__unique_language__contains=language.unique_language, function_type__unique_function_type__contains=function_type.unique_function_type)
            print(function_names)
            function_name_list = []

            for function_name in function_names:
                print("------------------")
                function_name_list.append(str(function_name))
        
            function_type_names[function_type.unique_function_type] = function_name_list
            #print(function_type_names)

        language_function_types[language.unique_language] = function_type_names
        #print(language_function_types)
            
    print(language_function_types)
    
    LFTJSON = dumps(language_function_types)
    return render(request, "funkdata/index.html", {
        "LFTJson": LFTJSON,
        "LFTDjango": language_function_types,

    })

def test(request):
    return render(request, "funkdata/testing.html")

