let btnSubmit = document.getElementById('submit');
let textForms = document.querySelectorAll("input[type=text]");
let submit2 = document.getElementById('submit2')

function checkForms(button){
    let passed = true;
    for(let each of textForms){
        if(each.value === ''){
            passed = false;
        }
    }
    
    let count = 0;
    for(let each of boxes){
        if(each.checked === true){
            count += 1;
        }
    }
    
    if(count < boxes.length / 2){
        passed = false;
    }    
    
    
    if(passed === true){
        submit2.click()
        
    }else{
        alert('One or more of the required (*) fields have been left unanswered. Please fill in each section to request a ride!')
    }
}

btnSubmit.onclick = function(){
        checkForms();
}