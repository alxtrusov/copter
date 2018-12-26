async function getImage(){
    const data = await $.get('http://172.16.2.155:8080/api/stream');
    if (data && data.result);
    document.getElementById("image").src = "data:image/png;base64," + data.result;
    getImage();
}

$(document).ready(() => {
    getImage();
});