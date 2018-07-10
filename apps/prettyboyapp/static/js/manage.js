let details = document.getElementsByClassName('details');
let buttons = document.getElementsByTagName('button');


function showDetails(detail) {
    let container = detail.closest('li');
    let info = container.querySelector('.info-under');
    let arrow = detail.querySelector('.arrow');
    
    if (info.style.height === "200px") {
        info.style.height = "0px";
        
    } else {

        info.style.height = "200px"; 
    }
}


function clicked(button) {
    console.log(button);
    if (confirm('Do you want to cancel this ride?')) {
        button.submit();
    } else {
        return false;
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
