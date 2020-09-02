let details = document.getElementsByClassName('details');
let buttons = document.getElementsByTagName('button');


function showDetails(detail) {
    let container = detail.closest('li');
    let info = container.querySelector('.info-under');
    let arrow = detail.querySelector('.arrow');



    if (info.style.height === "200px") {
        info.style.height = "0px";
        detail.innerHTML = 'See Details';

    } else {

        info.style.height = "200px";
        detail.innerHTML = 'Hide Details';
    }
}

function clicked(button) {

    if (button.name === 'delete_button') {

        if (confirm('Are you sure you want to delete this ride?')) {
            button.parentElement.submit();
        } else {
            return false;
        }

    } else {
        button.parentElement.submit();
    }

}

let flexBox = document.querySelectorAll(' .flex-box > div');

function underline() {

    for (var i = 0; i < flexBox.length; i++) {
        flexBox[i].addEventListener('mouseover', function () {
            this.querySelector('.bottom-border').classList.add('extend');
        })

        flexBox[i].addEventListener('mouseout', function () {
            this.querySelector('.bottom-border').classList.remove('extend');
        })
    }

};

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

underline();
