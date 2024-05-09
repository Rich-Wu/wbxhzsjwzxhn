function togglePinyin(event) {
    const py = event.currentTarget.querySelector(".pinyin");
    py.style.visibility = py.style.visibility == "hidden" ? "visible" : "hidden";
}