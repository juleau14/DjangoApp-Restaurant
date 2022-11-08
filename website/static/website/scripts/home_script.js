function start() {
    window.addEventListener("scroll", progressBar);
}


function progressBar() {
    const bar = document.querySelector(".scroll_progress_bar");
    const body = document.querySelector("body");

    let totalScrollable = body.offsetHeight - window.innerHeight;
    let alreadyScrolled = window.scrollY;
    let ratioAlreadyScrolled = alreadyScrolled / totalScrollable;

    let totalWidth = body.offsetWidth;

    let barWidth = ratioAlreadyScrolled * totalWidth;

    bar.style.width = String(barWidth) + "px";
}


start();