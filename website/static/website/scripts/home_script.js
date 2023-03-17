const body = document.querySelector("body");

// Phone nav
const openPhoneNavButton = document.querySelector(".open_phone_nav");
const closePhoneNavButton = document.querySelector(".close_phone_nav");
const contactsPhoneNavButton = document.querySelector(".phone_nav_button.contacts");
const pricesPhoneNavButton = document.querySelector(".phone_nav_button.prices");

// Scroll
const contactsScrollButton = document.querySelector(".nav.contacts");
const pricesScrollButton = document.querySelector(".nav.prices");
const topScrollButton = document.querySelector(".nav.top");
const reservationScrollButton = document.querySelector(".nav.reservation");


function start() {
    // Loader
    window.addEventListener("load", hideLoader);

    // PhoneNav
    window.addEventListener("scroll", phoneNavButtonToTop);
    openPhoneNavButton.addEventListener("click", displayPhoneNav);
    closePhoneNavButton.addEventListener("click", closePhoneNav);
    contactsPhoneNavButton.addEventListener("click", scrollToContactsPhoneNav);
    pricesPhoneNavButton.addEventListener("click", scrollToPricesPhoneNav);

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
    reservationScrollButton.addEventListener("click", scrollToReservation);
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


function phoneNavButtonToTop() {
    if (window.scrollY == 0) {
        openPhoneNavButton.style.marginTop = '0';
    }
    else {
        openPhoneNavButton.style.marginTop = '8px';
    }
}


function displayPhoneNav() {
    const phoneNav = document.querySelector(".phone_nav");

    phoneNav.style.visibility = 'inherit';
    phoneNav.style.transform = 'rotate(0)';
    phoneNav.style.height = '100vh';
    phoneNav.style.marginLeft = '0';

    openPhoneNavButton.style.marginLeft = '-70px';
}


function closePhoneNav() {
    const phoneNav = document.querySelector(".phone_nav");

    phoneNav.style.marginLeft = '-200vw';
    phoneNav.style.transform = 'rotate(-45deg)';
    phoneNav.style.height = '400vh';
    setTimeout(function() {phoneNav.style.visibility = 'hidden'}, 1000);

    openPhoneNavButton.style.marginLeft = '0';
}


function scrollToContactsPhoneNav() {
    closePhoneNav();
    scrollToContacts();
}


function scrollToPricesPhoneNav() {
    closePhoneNav();
    scrollToPrices();
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

function scrollToReservation() {
    const reservationDiv = document.querySelector(".reservation_title");
    window.scrollBy(0, reservationDiv.getBoundingClientRect().top);
}


start();