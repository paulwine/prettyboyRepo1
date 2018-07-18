let boxes = document.querySelector('.checkboxes').getElementsByTagName('input');
let submit = document.querySelector('#submit')

function checkBoxes(current){
    let parent = current.closest('span.together');
    let children = parent.getElementsByTagName('input');
    
    for(let each of children){
        each.checked = false;
    }
    
    current.checked = true;
}

for(let each of boxes){
	each.onclick = function(){
		checkBoxes(each);
	}
}

submit.onclick = function(){
	alert('Your Information has been saved and can be reused!');
}