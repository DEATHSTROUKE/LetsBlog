window.onload = function () {
    ajax('post', '/add_watch', JSON.stringify('value=' + cat_btn[i].value), handler);
};

var thumb_up = document.querySelector('.thumb_up');
var thumb_down = document.querySelector('.thumb_down');


function ajax(method, url, data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.addEventListener('readystatechange', () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(xhr.responseText)
        }
    });
    if (method === 'post') {
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-url');
    }
    xhr.send(data);

}

