
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


// Navigation Functions

// Directs user to explore page with the selected id of the drink 
function goToExplore(id) {
    window.location.href = "/explore.html?id=" + id;
}
// Gets the value of the filter from the list and directs to the explore page 
function applyFilter() {
    let filter = document.getElementById("filter-select").value;
    window.location.href = "/explore.html?filter=" + filter;
}

// Takes input form explore page searchbar. With considering only lowercase goes through all the cards to find if one includes input 
function filterCocktails() {
    let input = document.getElementById("search-bar").value.toLowerCase();
    let cards = document.querySelectorAll(".cocktail-card");
    
    cards.forEach(card => {
        let name = card.querySelector("h3").innerText.toLowerCase();
        card.style.display = name.includes(input) ? "block" : "none";
    });
}

// Opens review pop-up section in explore page (inspection mode)
function openReviewModal() {
    document.getElementById("reviewModal").style.display = "block";
}

// Closes review pop-up section in explore page (inspection mode) (x button)
function closeReviewModal() {
    document.getElementById("reviewModal").style.display = "none";
}

// Open the cocktail edit pop-up section in userpage
// takes all the current data from the cocktail (except image)
// Populates the edit sections with this data
function openEditModal(cocktailId) {
    document.getElementById("editModal").style.display = "block";
    
    fetch(`/get_cocktail/${cocktailId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("editCocktailId").value = data.id;
            document.getElementById("editName").value = data.name;
            document.getElementById("editAlcohol").value = data.alcohol_content;
            document.getElementById("editMethod").value = data.method;
        });
}

// Closes the cocktail edit pop-up section in userpage (x button)
function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}


//Ingredient Selection (Pantry & Creation Pages)

// Ingredients list
let selectedIngredients = [];

// While page loaded
// taking the necessary data form pantry/create page
// to handle the lists
document.addEventListener("DOMContentLoaded", () => {
    const availableIngredients = document.querySelectorAll(".ingredient-item");
    const selectedIngredientsList = document.getElementById("selectedIngredientsList");
    const selectedIngredientsInput = document.getElementById("selectedIngredientsInput");
    const cocktailList = document.getElementById("cocktail-list");


    
    function updateUI() {
        // replaces the current list with list on selected ingredients (with onclick function)
        if (selectedIngredientsList) {
            selectedIngredientsList.innerHTML = selectedIngredients.map(ing => 
                `<li onclick="toggleIngredient(${ing.id}, '${ing.name}')">${ing.name}</li>`
            ).join("");
        }
        //converts input into a string for hidden submission
        if (selectedIngredientsInput) {
            selectedIngredientsInput.value = selectedIngredients.map(ing => ing.id).join(",");
        }

        // 
        if (cocktailList) { 
            fetch("/get_cocktails", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ingredients: selectedIngredients.map(ing => ing.id) })
            })
            .then(response => response.json())
            .then(cocktails => {cocktailList.innerHTML = cocktails.length 
                ? cocktails.map(c => `<li><a href="/explore.html?id=${c.id}">${c.name}</a></li>`).join("")
                : "<li>No matches found</li>";
            });
        }
    }
    //Removal and addition of a ingredient to the list
    window.toggleIngredient = function (id, name) {
        const index = selectedIngredients.findIndex(ing => ing.id === id);
        if (index > -1) {
            selectedIngredients.splice(index, 1);
        } else {
            selectedIngredients.push({ id, name });
        }
        updateUI();
    };

    // Ingredient click checker. If so the data is sent to the functions above 
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

/*Homepage Slideshow */
let slideIndex = 0; 
let autoSlideInterval; 

document.addEventListener("DOMContentLoaded", () => {
    showSlides(); 
    startAutoSlides(); 
});

// Function to show slides
function showSlides() {
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");

    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slideIndex++;

    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    slides[slideIndex - 1].style.display = "block";

    for (let i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    if (dots.length > 0) {
        dots[slideIndex - 1].className += " active";
    }
}

// Function to start automatic slideshow
function startAutoSlides() {
    autoSlideInterval = setInterval(() => {
        showSlides();
    }, 5000); 
}

// Function for manual controls
function plusSlides(n) {
    clearInterval(autoSlideInterval); 
    slideIndex += n - 1; 
    showSlides();
    startAutoSlides(); 
}

// Function for direct dot selection
function currentSlide(n) {
    clearInterval(autoSlideInterval); 
    slideIndex = n - 1;
    showSlides();
    startAutoSlides(); 
}
//Chatbot Prefrences
const savePreferences = async () => {
    const preferences = {
        user_id: 1, // Get this dynamically if user login is implemented
        favorite_ingredients: ["rum", "lime", "mint"],
        disliked_ingredients: ["whiskey", "egg whites"],
        preferred_cocktail_types: ["refreshing", "sweet"]
    };

    const response = await fetch('/save_preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preferences)
    });

    const data = await response.json();
    alert(data.message);
};
