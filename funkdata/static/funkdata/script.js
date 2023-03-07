function clearFunctionInfo() {
    console.log('clear!')
}

function displayJSStringFunction() {
    functionChoice = document.querySelector('#JS-string-menu').value;

    clearFunctionInfo();

    if (functionChoice === "length") {
        document.querySelector('#method-content').textContent = ".length()";

    } else if (functionChoice === "slice") {
        console.log('Slice')
    }
}

function displayJSNumberFunction() {
    functionChoice = document.querySelector('#JS-number-menu').value;

    clearFunctionInfo();

    if (functionChoice === "numbersomething") {
        console.log('Numberchoice');
    }
}

// Get rid of any currently displayed function menus, to prevent stacking
function clearFunctionMenus() {
    document.querySelectorAll('.function-menu-container').forEach(container => {
        container.style.display = 'none';
    });
    document.querySelectorAll('.JSFM').forEach(menu => {
        menu.style.display = 'none';
    });

    document.querySelectorAll('.PyFM').forEach(menu => {
        menu.style.display = 'none';
    });
}

// Make different dropdown menus appear based on the language chosen
function displayTypes() {
    langMenu = document.querySelector('#lang-menu');

    clearFunctionMenus();

    if (langMenu.value === "javascript") {
        console.log("JS success!");
        document.querySelector('#JS-function-menu-container').style.display = 'flex';
        document.querySelectorAll('.JSFM').forEach(menu => {
            menu.style.display = 'block';
        });

    } else if (langMenu.value === "python") {
        console.log("python success!");
        document.querySelector('#Py-function-menu-container').style.display = 'flex';
        document.querySelectorAll('.PyFM').forEach(menu => {
            menu.style.display = 'block';
        });

    } else if (langMenu.value === "html") {
        alert("HTML not yet implemented");

    } else if (langMenu.value === "css") {
        alert("CSS not yet implemeneted");
        
    }
}

// Make the menus active via .onchange event
document.querySelector('#lang-menu').onchange = displayTypes;
document.querySelector('#JS-number-menu').onchange = displayJSNumberFunction;
document.querySelector('#JS-string-menu').onchange = displayJSStringFunction;