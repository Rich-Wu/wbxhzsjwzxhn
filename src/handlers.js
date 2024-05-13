const isMobile = 'ontouchstart' in window || navigator.maxTouchPoints;

function toggleDetails(event) {
    const word = event.currentTarget;
    const py = word.querySelector(".py");
    const def = word.querySelector(".def");
    py.classList.toggle("hidden");
    def.classList.toggle("hidden");
}

document.querySelectorAll(".word").forEach(word => {
    if (!isMobile) {
        word.addEventListener("mouseenter", toggleDetails);
        word.addEventListener("mouseleave", toggleDetails);
    } else {
        word.addEventListener("touchstart", toggleDetails);
        word.addEventListener("touchend", toggleDetails);
    }
})