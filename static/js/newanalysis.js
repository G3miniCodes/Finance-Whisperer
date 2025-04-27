document.addEventListener("DOMContentLoaded", function () {
    // Buttons
    let manualEntryBtn = document.getElementById("manualEntryBtn");
    let pictorialEntryBtn = document.getElementById("pictorialEntryBtn");

    // Forms
    let manualEntryForm = document.getElementById("manualEntryForm");
    let pictorialEntryForm = document.getElementById("pictorialEntryForm");
    let ocrForm = document.getElementById("ocrForm");

    // Open Manual Entry Form
    manualEntryBtn.addEventListener("click", function () {
        manualEntryForm.style.display = "block";
    });

    // Open Pictorial Entry Form
    pictorialEntryBtn.addEventListener("click", function () {
        pictorialEntryForm.style.display = "block";
    });

    // Close Forms on Back
    document.querySelectorAll(".popup button").forEach(button => {
        if (button.textContent === "Back") {
            button.addEventListener("click", function () {
                this.parentElement.style.display = "none";
            });
        }
    });

    // Dummy OCR Processing → show ocrForm
    document.getElementById("uploadImage").addEventListener("change", function () {
        if (this.files.length > 0) {
            alert("Image Uploaded!");
        }
    });

    document.querySelector("#pictorialEntryForm button:nth-child(2)").addEventListener("click", function () {
        alert("Image Processed, OCR Data Extracted!");
        pictorialEntryForm.style.display = "none";
        ocrForm.style.display = "block";

        // Dummy extracted data
        document.getElementById("ocrAmount").value = "1000";
        document.getElementById("ocrCategory").value = "Food";
        document.getElementById("ocrDate").value = "2025-03-25";
    });

    // Assign submitForm function to all Submit buttons
    document.querySelectorAll("button").forEach(button => {
        if (button.textContent === "Submit") {
            button.addEventListener("click", function () {
                submitForm();
            });
        }
    });
});

// ✅ Global submit function (handles manual & OCR form submission)
function submitForm() {
    const ocrAmount = document.getElementById("ocrAmount");
    const ocrCategory = document.getElementById("ocrCategory");
    const ocrDate = document.getElementById("ocrDate");

    if (ocrAmount && ocrAmount.value) {
        console.log("OCR Submitted:", {
            amount: ocrAmount.value,
            category: ocrCategory.value,
            date: ocrDate.value
        });
    } else {
        const amount = document.getElementById("amount").value;
        const category = document.getElementById("category").value;
        const date = document.getElementById("date").value;

        console.log("Manual Submitted:", { amount, category, date });
    }

    alert("Form Submitted!");
    document.getElementById("manualEntryForm").style.display = "none";
    document.getElementById("ocrForm").style.display = "none";
}