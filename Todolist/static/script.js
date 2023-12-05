let main =document.getElementById('main');

window.addEventListener('scroll',() =>{
    let value = window.scrollY;

    main.style.marginTop = value * 1 + 'px';
    main.style.Top = value * 2.5 + 'px';
});
