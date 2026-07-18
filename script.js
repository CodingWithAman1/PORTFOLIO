/* ==========================================================

   PORTFOLIO SCRIPT

========================================================== */



/* ==========================================================

   LIVE CLOCK (IST)

========================================================== */



function updateClock() {



    const clock = document.getElementById("clock");



    if (!clock) return;



    const now = new Date();



    clock.textContent = now.toLocaleTimeString("en-IN", {

        timeZone: "Asia/Kolkata",

        hour: "2-digit",

        minute: "2-digit",

        second: "2-digit",

        hour12: true

    }) + " IST";



}



updateClock();

setInterval(updateClock, 1000);



/* ==========================================================

   CUSTOM CURSOR

========================================================== */



const dot = document.querySelector(".cursor-dot");

const outline = document.querySelector(".cursor-outline");



let mouseX = 0;

let mouseY = 0;



let outlineX = 0;

let outlineY = 0;



document.addEventListener("mousemove", (e) => {



    mouseX = e.clientX;

    mouseY = e.clientY;



    if (dot) {

        dot.style.left = mouseX + "px";

        dot.style.top = mouseY + "px";

    }



});



function animateCursor() {



    outlineX += (mouseX - outlineX) * 0.18;

    outlineY += (mouseY - outlineY) * 0.18;



    if (outline) {

        outline.style.left = outlineX + "px";

        outline.style.top = outlineY + "px";

    }



    requestAnimationFrame(animateCursor);



}



animateCursor();



/* ==========================================================

   CURSOR HOVER

========================================================== */



document.querySelectorAll("a,button,.nav-link,.item").forEach((el) => {



    el.addEventListener("mouseenter", () => {



        if (outline) outline.classList.add("cursor-hover");



    });



    el.addEventListener("mouseleave", () => {



        if (outline) outline.classList.remove("cursor-hover");



    });



});


const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-link");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 120;

        if (window.scrollY >= sectionTop) {

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach(link => {

        link.classList.remove("active");

        if(link.getAttribute("href")==="#" + current){

            link.classList.add("active");

        }

    });

});
 
