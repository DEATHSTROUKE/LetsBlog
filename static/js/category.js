var btn = document.querySelectorAll('.subs');
console.log(btn);
for (let i = 0; i < btn.length; i++) {
    btn[i].addEventListener('mouseover', () => {
        btn[i].innerHTML = 'Отписаться';
    });
    btn[i].addEventListener('mouseout', () => {
        btn[i].innerHTML = 'Подписан';
    });
}
