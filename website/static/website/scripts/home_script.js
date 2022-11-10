const body = document.querySelector("body");

const contactsScrollButton = document.querySelector(".nav.contacts");
const pricesScrollButton = document.querySelector(".nav.prices");
const topScrollButton = document.querySelector(".nav.top");


function start() {
    // Loader
    window.addEventListener("load", hideLoader);

    // Progress bar
    window.addEventListener("scroll", progressBar);     
    
    // Apparitions
    window.addEventListener("scroll", contactApparition);
    window.addEventListener("scroll", mapApparition);
    window.addEventListener("scroll", pricesApparition);
    window.addEventListener("scroll", logosApparitions);

    // Scroll Buttons
    contactsScrollButton.addEventListener("click", scrollToContacts);
    pricesScrollButton.addEventListener("click", scrollToPrices);
    topScrollButton.addEventListener("click", scrollToTop);
}


function hideLoader() {
    const loader = document.querySelector(".loader");
    const animation = document.querySelector(".loading_animation");
    setTimeout(function() {
        loader.style.height = "0";
        animation.style.height = "0";
        setTimeout(function() {loader.style.display = "none"}, 1000 );
    }, 2000);
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


function logosApparitions() {
    const logoInstagram = document.querySelector(".logo_link.instagram");
    const logoFacebook = document.querySelector(".logo_link.facebook");
    const logoMichelin = document.querySelector(".logo_link.michelin");
    const logoGaultmillau = document.querySelector(".logo_link.gaultmillau");

    if (window.scrollY >= (body.offsetHeight - window.innerHeight - 30)) {
        logoInstagram.style.marginLeft = "3vw";
        logoInstagram.style.transition = "1s";

        logoFacebook.style.marginLeft = "3vw";
        logoFacebook.style.transition = "1.2s";
        logoFacebook.style.display = "inherit";

        logoMichelin.style.marginLeft = "3vw";
        logoMichelin.style.transition = "1.4";

        logoGaultmillau.style.marginLeft = "3vw";
        logoGaultmillau.style.transition = "1.6s";
    }
}


function scrollToContacts() {
    const contactsDiv = document.querySelector(".contacts_div");
    window.scrollBy(0, contactsDiv.getBoundingClientRect().top);
    html.style.backgroundColor="red";
}


function scrollToPrices() {
    const pricesDiv = document.querySelector(".prices_div");
    window.scrollBy(0, pricesDiv.getBoundingClientRect().top);
}


function scrollToTop() {
    window.scrollTo(0, 0);
}


start();