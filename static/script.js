//function scrollLeft() {
//    document.getElementById('scrollContainer').scrollBy({ left: -220, behavior: 'smooth' });
//}

//function scrollRight() {
//    document.getElementById('scrollContainer').scrollBy({ left: 220, behavior: 'smooth' });
//}
document.addEventListener("DOMContentLoaded", function () {
    const grid = document.getElementById("cocktail-grid");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let scrollAmount = 300;

    nextBtn.addEventListener("click", function () {
        grid.scrollBy({ left: scrollAmount, behavior: "smooth" });
    });

    prevBtn.addEventListener("click", function () {
        grid.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    });
});

