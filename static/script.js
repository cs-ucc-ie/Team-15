<<<<<<< HEAD
//script for age verification pop up 
document.addEventListener("DOMContentLoaded", function () {
    let overlay = document.getElementById("age-overlay");
    let mainContent = document.getElementById("main-content");

    // Checks if age is already verified
    if (sessionStorage.getItem("ageVerified")) {
        overlay.style.display = "none";
        mainContent.style.display = "block";
    } else {
        overlay.style.display = "flex"; 
        mainContent.style.display = "none"; // Hides the homepage until age is verified
    }
});

function checkAge() {
    let dobInput = document.getElementById("dobInput").value;
    
    if (!dobInput) {
        alert("Please enter your date of birth.");
        return;
    }

    let birthDate = new Date(dobInput);
    let today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    let monthDiff = today.getMonth() - birthDate.getMonth();
    let dayDiff = today.getDate() - birthDate.getDate();

    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--; 
    }

    //If the user is over 18, load the homepage, otherwise redirect them to Google by default
    if (age >= 18) {
        sessionStorage.setItem("ageVerified", "true");
        document.getElementById("age-overlay").style.display = "none";
        document.getElementById("main-content").style.display = "block";
    } else {
        alert("You must be 18 or older to access this site.");
        window.location.href = "https://www.google.com"; // Redirect underage users
    }
}
//for carousel
=======
//function scrollLeft() {
//    document.getElementById('scrollContainer').scrollBy({ left: -220, behavior: 'smooth' });
//}

//function scrollRight() {
//    document.getElementById('scrollContainer').scrollBy({ left: 220, behavior: 'smooth' });
//}
>>>>>>> master
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
<<<<<<< HEAD
=======

>>>>>>> master
