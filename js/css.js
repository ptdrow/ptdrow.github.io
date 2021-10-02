// JavaScript source code
function toLight(elements) {
    var n = elements.length;
    for (let i = 0; i < n; i++) {
        toggleClass(elements[0], 'dark', 'light');
    }
}

function toDark(elements) {
    var n = elements.length;
    for (let i = 0; i < n; i++) {
        toggleClass(elements[0], 'light', 'dark');
    }
}

function toggleDarkLight() {
    var elements = document.getElementsByClassName('dark');
    if (elements.length > 0) {
        toLight(elements);
    } else {
        toDark(document.getElementsByClassName('light'));
        
    }
}

function toggleClass(element, fromClass, toClass) {
    element.classList.add(toClass);
    element.classList.remove(fromClass);
}