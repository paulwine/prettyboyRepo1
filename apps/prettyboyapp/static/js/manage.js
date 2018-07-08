let details = document.getElementsByClassName('details');
let buttons = document.getElementsByTagName('button');


function showDetails(detail) {
    let container = detail.closest('li');
    console.log(container);
    let info = container.querySelector('.info-under');
}


function clicked(button) {
    console.log(button);
    if (confirm('Do you want to cancel this ride?')) {
        button.submit();
    } else {
        return false;
    }

}

for (i = 0; i < details.length; i++) {
    let current = details[i];

    current.onclick = function () {
        showDetails(current);
    }
}

for (i = 0; i < buttons.length; i++) {
    let current = buttons[i];

    current.onclick = function () {
        clicked(current);
    }
}

