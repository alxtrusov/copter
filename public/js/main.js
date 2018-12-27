async function getImage(cb) {
    const data = await $.get('http://172.16.2.155:8080/api/stream');
    cb((data && data.result) ? "data:image/png;base64," + data.result : null);

    /*if (data && data.codes) {
        console.log(data.codes);
    }*/

    getImage(cb);
}

$(document).ready(() => {
    const canvas = document.getElementById('canvas');
        canvas.width = 400;
        canvas.height = 300;
    const context = canvas.getContext('2d');
    const image = new Image();
    image.onload = () => context.drawImage(image, 0, 0);
    getImage(data => image.src = data);
});