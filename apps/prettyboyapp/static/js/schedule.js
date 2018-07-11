let pay = document.querySelector('#private-pay');
let payText = document.querySelector('#private-pay-text');
let showDays = document.getElementById('repeat');
let days = document.getElementById('days');
let boxes = document.querySelector('.checkboxes').getElementsByTagName('input');

function checkBoxes(current){
    let parent = current.closest('span.together');
    let children = parent.getElementsByTagName('input');
    
    for(let each of children){
        each.checked = false;
    }
    
    current.checked = true;
}

function privatePay() {

    if (pay.checked === true) {
        payText.style.display = 'block';
    } else {
        payText.style.display = 'none';
    }
};

function dayDisplay(){
    if(showDays.checked ===true){
        days.style.display = 'block';
    }else{
        days.style.display = 'none';
    }
};

pay.onclick = function(){
    privatePay();
};

showDays.onclick = function(){
    dayDisplay();
}

for(i = 0; i < boxes.length; i++){
    boxes[i].onclick = function(){
        checkBoxes(this);
    }
    console.log(boxes[i]);
}
