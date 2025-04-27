// Login Form Validation
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email");
    const password = document.getElementById("password");

    if (!email.value.includes("@") || password.value.length < 6) {
        alert("Invalid email or password too short.");
        return;
    }

    alert("Login successful!");
});


// Dropdown Toggle
document.querySelector(".dropdown-btn").addEventListener("click", function(event) {
    event.preventDefault();
    document.querySelector(".dropdown-menu").classList.toggle("show");
});

// Close Dropdown on Outside Click
document.addEventListener("click", function(event) {
    if (!event.target.closest(".dropdown")) {
        document.querySelector(".dropdown-menu").classList.remove("show");
    }
});
