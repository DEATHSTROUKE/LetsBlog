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
var cat_btn = document.querySelectorAll('.users__btn');
console.log(cat_btn);
for (let i = 0; i < cat_btn.length; i++) {
    console.log(cat_btn[i].value);
    cat_btn[i].addEventListener('click', () => {
        ajax('post', '/add_sub_person', JSON.stringify('value=' + cat_btn[i].value), handler);
        cat_btn[i].classList.toggle('subs');
        change_text(cat_btn[i]);
    });
}

function ch1(btn1) {
    btn1.innerHTML = 'Отписаться';
}

function ch2(btn1) {
    btn1.innerHTML = 'Подписан';
}

function change_text(btn1) {
    if (btn1.innerHTML === 'Подписаться') {
        btn1.addEventListener('mouseover', ch1);
        btn1.addEventListener('mouseout', ch2);
        btn1.innerHTML = 'Подписан';
    } else {
        btn1.removeEventListener('mouseover', ch1);
        btn1.removeEventListener('mouseout', ch2);
        btn1.innerHTML = 'Подписаться';
    }
}

function ajax(method, url, data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.addEventListener('readystatechange', () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            callback(xhr.responseText)
        }
    });
    if (method == 'post') {
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-url');
    }
    xhr.send(data);

}

function handler(text) {
    console.log(text);
}
