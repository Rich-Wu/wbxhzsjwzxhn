function togglePinyin(event) {
    const py = event.currentTarget.querySelector(".pinyin");
    py.style.visibility = py.style.visibility == "hidden" ? "visible" : "hidden";
    const def = event.currentTarget.querySelector(".def");
    def.style.visibility = def.style.visibility == "hidden" ? "visible" : "hidden";
    event.stopPropagation()
}