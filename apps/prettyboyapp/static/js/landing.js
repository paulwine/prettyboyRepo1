function goToBottom(){
    let bottom = document.querySelector('.view-three').getBoundingClientRect().top;
    window.scrollBy({
        top: bottom,
        left: 0,
        behavior: 'auto',
    });
    
};

function goToAbout(){
    let about = document.querySelector('.view-two').getBoundingClientRect().top;
    window.scrollBy({
        top: about + 70,
        left: 0,
        behavior: 'smooth',
    });
};