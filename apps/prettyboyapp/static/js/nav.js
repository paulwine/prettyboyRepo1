"use strict"; 

let sideNav = document.getElementById('side-nav');
let gradient = document.querySelector('.gradient')

function navOut() {
    "use strict"; 

    sideNav.classList.toggle('hidden');    
    gradient.classList.toggle('applied-gradient');

}
