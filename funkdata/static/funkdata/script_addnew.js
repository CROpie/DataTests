function createNewLanguageField() {
    new_language_field = document.createElement("input");
    new_language_field.setAttribute('id', "new-function-type-field");
    new_language_field.setAttribute('type', "text");
    return new_language_field;
}

function showFunctionTypes(functionlanguage) {

    // If the input box next to function type is present, remove it.
    // Only is relevant when changing the langage after the function type has been chosen,
    
    if (document.querySelector("#new-function-type-field")) {
        remove_me = (document.querySelector("#new-function-type-field"));
        remove_me.remove();
    }

    document.querySelectorAll('.language-type-container').forEach(container => {
        container.style.display = 'none';
            
    })

    if (functionlanguage === "lang-default") {
        return;
    
    } else if (functionlanguage === "new-language") {
        document.querySelector("#new-language-field").setAttribute('type', "text");

        showdropdowns = document.getElementById("frozen-type-container");
        showdropdowns.style.display = "flex";
        new_language_field = createNewLanguageField()
        showdropdowns.append(new_language_field);

    } else {

        showdropdowns = document.getElementById(`${functionlanguage}-type-container`);
        showdropdowns.style.display = "flex";
    }
}

// need to create the new-function-type-field using jscript so it occurs after django has done its thing
// otherwise, >1 field will be created

function showNewFunctionTypeField(function_type) {
    if (!document.querySelector("#new-function-type-field") && (function_type === "new-function-type")) {

        selected_language = document.querySelector("#lang-menu").value;
        new_language_field = createNewLanguageField()

        // Since a unique dropdown is added for every language choice, need to select the specific one
        function_type_dropdown = document.querySelector(`#${selected_language}-type-container`);
        function_type_dropdown.append(new_language_field);
    }
}

// Checks that none of the data fields are empty when trying to submit
function check_not_null() {
    if ((!document.querySelector("#syntax-data").value) || 
        (!document.querySelector("#parameters-data").value) || 
        (!document.querySelector("#return_value-data").value)) {
        alert("blank data field error")
        return "error";
    }
}

function whitespace_check(value_submit) {
    for (i = 0; i < value_submit.length; i++) {
        if (value_submit.charAt(i) === ' ') {
            alert("whitespace error");
            return "error";
        }
    }
}

// ensure that the language is not default nor a blank new language field when trying to submit
function get_language_submit(selected_language) {

    if (selected_language === "new-language") {
        if (!document.querySelector("#new-language-field").value) {
            alert("blank_language_field_error");
            return "error";
        } else {
            language_submit = document.querySelector("#new-language-field").value;

            space_check = whitespace_check(language_submit);
            if (space_check === "error") {
                return "error";
            } else {
                return language_submit;
            }
        }
    }

    if (selected_language === "lang-default") {
        alert ("language-default-error")
        return "error";
    }

    // neither new, nor default, so return the selected language as the one to submit
    return selected_language;
}

// ensure that the function type is not default nor a blank new function type field when trying to submit
function get_function_type_submit(selected_language) {
    if (selected_language === "new-language") {
        if (!document.querySelector("#new-function-type-field").value) {
            alert("blank_function_type_error");
            return "error";
        } else {
            new_function_type = document.querySelector("#new-function-type-field").value;

            space_check = whitespace_check(new_function_type);
            if (space_check === "error") {
                return "error";
            } else {
                return new_function_type;
            }
        }
    } else {
        // not a new language, so the function type dropdown box will be specific to the language chosen
        selected_function_type = document.querySelector(`#${selected_language}-function-type-menu`).value
    }

    if(selected_function_type === "new-function-type") {
        if (!document.querySelector("#new-function-type-field").value) {
            alert("blank_function_type_error");
            return "error";
        } else {
            new_function_type = document.querySelector("#new-function-type-field").value;

            space_check = whitespace_check(new_function_type);
            if (space_check === "error") {
                return "error";
            } else {
                return new_function_type;
            }
        }
    }

    if (selected_function_type === "func-default") {
        alert("function_type_default_error")
        return "error";
    
    }

    return selected_function_type;
}

// collect the information from the various fields while checking for errors 
function submitData() {
    
    selected_language = document.querySelector("#lang-menu").value;

    language_submit = get_language_submit(selected_language);
    if (language_submit === "error") {
        return;
    }

    function_type_submit = get_function_type_submit(selected_language)
    if (function_type_submit === "error") {
        return;
    }

    data_submit_check = check_not_null()
    if (data_submit_check === "error") {
        return;
    }

    function_name_submit = document.querySelector("#function-name-data").value;
    syntax_submit = document.querySelector("#syntax-data").value;
    parameters_submit = document.querySelector("#parameters-data").value;
    return_value_submit = document.querySelector("#return_value-data").value;

    console.log(language_submit, function_type_submit, function_name_submit, syntax_submit, parameters_submit, return_value_submit);

    // note: fetch has to use 'body', not some random variable name
    // note: saving the return of stringify as a variable and sending to a different function resulted in errors
    fetch('/funkdata/submitnew', {
        method: "POST",
        body: JSON.stringify({
            language: language_submit,
            function_type: function_type_submit,
            function_name: function_name_submit,
            syntax: syntax_submit, 
            parameters: parameters_submit, 
            return_value: return_value_submit,
        })
    })
        .then(response => response.json())
        .then(result => {
            alert(result);
        })
}