let cvs = document.getElementById("gauge");
let ctx = cvs.getContext("2d");
const maxFrames = 100;

let lastVal = 0;

const img = new Image;
img.src = "http://localhost:8000/arrow.svg";

function get(url, callback) {
    let xml = new XMLHttpRequest();
    xml.open(`GET`, url, true);
    xml.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xml.onload = () => callback(xml.status, xml.responseText);
    xml.send(null);
}

function drawCirlce(x, y, r, colour) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI, false);
    ctx.fillStyle = colour;
    ctx.fill();
}

function drawArc(x, y, r, sA, eA, colour) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.arc(x, y, r, sA, eA, false);
    ctx.fillStyle = colour;
    ctx.lineTo(x, y);
    ctx.fill();
}

function drawArrow(x, y, a) {
    ctx.save();
    ctx.translate(250, 250);
    ctx.rotate(a);
    ctx.translate(-250, -250);
    ctx.drawImage(img, 0, 0);
    ctx.restore();
}

function drawScale(value, rgb) {
    const startAngle = -0.708 * Math.PI;
    const fullScale = 1.398 * Math.PI;
    const endAngle = startAngle + value * fullScale;
    var centerX = cvs.width / 2;
    var centerY = cvs.height / 2;
    var radius = 200;
    const offset = 0;

    ctx.clearRect(0, 0, cvs.width, cvs.height);
    
    drawArc(centerX, centerY + offset, radius, 0.8 * Math.PI, 0.2 * Math.PI, rgb);

    drawCirlce(centerX, centerY + offset, radius / 2.5, `white`);
    drawArrow(centerX, centerY, endAngle);
}

function drawNumber(number) {
    ctx.font = "30px Helvetica";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText(`${number}`, 250, 400); 
}

function animateScale(scale, frame) {
    if (frame === 0) {
        lastVal = scale;
        return;
    }
    const delta = scale - lastVal;
    const angle = delta * Math.sin (((maxFrames - frame) / maxFrames) / 2 * Math.PI) + lastVal;
    const red = (1 - angle) * 255;
    const green = angle * 255;
    requestAnimationFrame(() => {
        drawScale(angle, `rgb(${red}, ${green}, 0)`);
        drawNumber(parseInt(scale * 100));
        animateScale(scale, --frame);
    });
}

function drawGauge() {
    get(`http://localhost:80/api/testSite?site=${$("#input").val()}`, (status, text) => {
        if (status !== 200) {
            console.log(`API error`);
            return
        }
        let json = JSON.parse(text);
        animateScale(json.trust, 100);
        let ul = $("#reasons");
        ul.html("");
        for (const item of json.reasons) {
            ul.append(`<li>${item}</li>`);
        }
    });
}

img.onload = () => {
    animateScale(0, 1);
}
