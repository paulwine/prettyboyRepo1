let pay = document.querySelector('#private-pay');
let payText = document.querySelector('#private-pay-text');
let showDests = document.getElementById('additional_checkbox');
let dests = document.getElementById('additional_destinations');
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

function destDisplay(){
    if(showDests.checked ===true){
        dests.style.display = 'block';
    }else{
        dests.style.display = 'none';
    }
};


showDests.onclick = function(){
    destDisplay();
}



for(i = 0; i < boxes.length; i++){
    boxes[i].onclick = function(){
        checkBoxes(this);
    }
}
