
//Age Verification Popup

document.addEventListener("DOMContentLoaded", function () {
    let overlay = document.getElementById("age-overlay");
    let mainContent = document.getElementById("main-content");

    if (sessionStorage.getItem("ageVerified")) {
        overlay.style.display = "none";
        mainContent.style.display = "block";
    } else {
        overlay.style.display = "flex";
        mainContent.style.display = "none";
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
    if (age >= 18) {
        sessionStorage.setItem("ageVerified", "true");
        document.getElementById("age-overlay").style.display = "none";
        document.getElementById("main-content").style.display = "block";
    } else {
        alert("You must be 18 or older to access this site.");
        window.location.href = "https://www.google.com";
    }
}


//IDK

document.addEventListener("DOMContentLoaded", function () {
    const grid = document.getElementById("cocktail-grid");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    let scrollAmount = 300;

    nextBtn?.addEventListener("click", function () {
        grid.scrollBy({ left: scrollAmount, behavior: "smooth" });
    });

    prevBtn?.addEventListener("click", function () {
        grid.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    });
});


//Navigation Functions

function goToExplore(id) {
    window.location.href = "/explore.html?id=" + id;
}

function applyFilter() {
    let filter = document.getElementById("filter-select").value;
    window.location.href = "/explore.html?filter=" + filter;
}

function filterCocktails() {
    let input = document.getElementById("search-bar").value.toLowerCase();
    let cards = document.querySelectorAll(".cocktail-card");
    
    cards.forEach(card => {
        let name = card.querySelector("h3").innerText.toLowerCase();
        card.style.display = name.includes(input) ? "block" : "none";
    });
}

function openReviewModal() {
    document.getElementById("reviewModal").style.display = "block";
}

function closeReviewModal() {
    document.getElementById("reviewModal").style.display = "none";
}


//Ingredient Selection (Pantry & Creation Pages)


let selectedIngredients = [];

document.addEventListener("DOMContentLoaded", () => {
    const ingredientList = document.getElementById("ingredient-list");
    const availableIngredients = document.querySelectorAll(".ingredient-item");
    const selectedIngredientsList = document.getElementById("selected-ingredients-list") || document.getElementById("selectedIngredientsList");
    const selectedIngredientsInput = document.getElementById("selectedIngredientsInput");
    const cocktailList = document.getElementById("cocktail-list");

    function updateUI() {
        if (selectedIngredientsList) {
            selectedIngredientsList.innerHTML = selectedIngredients.map(ing => 
                `<li onclick="toggleIngredient(${ing.id}, '${ing.name}')">${ing.name}</li>`
            ).join("");
        }
        if (selectedIngredientsInput) {
            selectedIngredientsInput.value = selectedIngredients.map(ing => ing.id).join(",");
        }
        if (cocktailList) {
            fetch("/get_cocktails", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ingredients: selectedIngredients.map(ing => ing.id) })
            })
            .then(response => response.json())
            .then(cocktails => {
                cocktailList.innerHTML = cocktails.length ? cocktails.map(c => `<li>${c.name}</li>`).join("") : "<li>No matches found</li>";
            });
        }
    }

    window.toggleIngredient = function (id, name) {
        const index = selectedIngredients.findIndex(ing => ing.id === id);
        if (index > -1) {
            selectedIngredients.splice(index, 1);
        } else {
            selectedIngredients.push({ id, name });
        }
        updateUI();
    };

    availableIngredients.forEach(item => {
        item.addEventListener("click", () => {
            const id = parseInt(item.getAttribute("data-id"));
            const name = item.getAttribute("data-name");
            toggleIngredient(id, name);
        });
    });
});


//Flash Messages Auto-hide

setTimeout(() => {
    document.querySelectorAll("#flash-messages .alert").forEach(alert => {
        alert.style.display = "none";
    });
}, 3000);

