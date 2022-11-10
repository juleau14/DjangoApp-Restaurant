function start() {
    window.addEventListener("scroll", progressBar);
    window.addEventListener("scroll", contactApparition);
    window.addEventListener("scroll", mapApparition);
    window.addEventListener("scroll", pricesApparition);
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


function contactApparition() {
    const contacts = document.querySelector(".contacts_content");

    if (window.scrollY >= contacts.getBoundingClientRect().top) {
        contacts.style.marginLeft = "0";
    }

    else {
        contacts.style.marginLeft = "100vw";
    }
}


function mapApparition() {
    const map = document.querySelector(".map");

    if (window.scrollY >= map.getBoundingClientRect().top) {
        map.style.marginLeft = "0";
    }

    else {
        map.style.marginLeft = "-100vw";
    }
}


function pricesApparition() {
    const prices = document.querySelector(".prices_content");

    if (window.scrollY >= prices.getBoundingClientRect().top) {
        prices.style.marginLeft = "0";
    }

    else {
        prices.style.marginLeft = "100vw";
    }
}


start();