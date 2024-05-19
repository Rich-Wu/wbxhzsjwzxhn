const isMobile = 'ontouchstart' in window || navigator.maxTouchPoints;
function toggleDetails(event) {
    const word = event.currentTarget;
    const text = word.querySelector(".text");
    text.style.backgroundColor = "yellow" == text.style.backgroundColor ? "" : "yellow";
    const details = word.querySelector(".details");
    details.classList.toggle("hidden");
}
function handleMove(event) {
    const word = event.currentTarget;
    const details = word.querySelector(".details");
    const computedStyles = window.getComputedStyle(details);
    const width = computedStyles.getPropertyValue('width');
    const height = computedStyles.getPropertyValue('height');
    details.style.left = event.pageX - parseFloat(width) * .2 + "px";
    details.style.top = event.pageY + 20 + "px";
}
document.querySelectorAll(".word").forEach(word => {
    if (!isMobile) {
        word.addEventListener("mouseenter", toggleDetails);
        word.addEventListener("mousemove", handleMove);
        word.addEventListener("mouseleave", toggleDetails);
    } else {
        word.addEventListener("touchstart", toggleDetails);
    }
})