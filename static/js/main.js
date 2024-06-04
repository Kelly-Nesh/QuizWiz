const timer = document.getElementById("displaytimer");
const inputtag = document.getElementById("timer");
const form = document.querySelector("form.d-none");
const start_button = document.querySelector("button.btn-success");

let t = 0;
const test = (n) => {
    alert(n);
};
const start = () => {
    form.classList.remove("d-none");
    start_button.classList.add("d-none");
    setInterval(() => {
        t += 1;
        timer.innerHTML = "<b>Timer: " + t + " seconds</b>";
        inputtag.value = t;
    }, 1000);
};