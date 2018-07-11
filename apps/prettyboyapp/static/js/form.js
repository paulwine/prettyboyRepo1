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


    if(validateDateTime() === false){
        passed = false;
    }
    
    if(passed === true){
        submit2.click()
        
    }else{
        alert('One or more of the required (*) fields have been left unanswered, or the ride is not scheduled at least 24 hours in advance. Please fill in each section to request a ride!')
    }
}

function validateDateTime(){
    let date = document.querySelector('input[type=date]');
    let time = document.querySelector('input[type=time]');
    let now = new Date();
    let yearMonthDay = date.value.split('-'); //returns array Year, Month, Day

    console.log(yearMonthDay);
    let hourSeconds = time.value.split(':'); //returns array Hour, seconds
    let rideTime = new Date(parseInt(yearMonthDay[0], 10), (parseInt(yearMonthDay[1], 10) - 1), parseInt(yearMonthDay[2], 10), parseInt(hourSeconds[0], 10), parseInt(hourSeconds[1], 10), 0, 0);


    if(date.value === '' || time.value === ''){
        return false;
    }

    if(now.getTime() > (rideTime.getTime() - 86400000)){
        return false
    }else{

    }

}

btnSubmit.onclick = function(){
        checkForms();
}