document.addEventListener("DOMContentLoaded", function () {
    const editIncome = document.getElementById("edit-income");
    const incomeInput = document.getElementById("income-input");
    const totalIncomeDisplay = document.getElementById("total-income");

    
    if (editIncome && incomeInput) {
        editIncome.addEventListener("click", function () {
            incomeInput.style.display = "block";
            incomeInput.focus();
        });

        incomeInput.addEventListener("blur", function () {
            const newIncome = incomeInput.value;

            if (newIncome.trim() !== "") {
                fetch("/update_income", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: `income=${newIncome}`
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === "success") {
                            totalIncomeDisplay.textContent = `Rs.${data.total_income}`;
                        }
                        incomeInput.style.display = "none";
                    })
                    .catch(error => {
                        console.error("Error updating income:", error);
                        incomeInput.style.display = "none";
                    });
            } else {
                incomeInput.style.display = "none";
            }
        });
    }

    // Manual Entry
    const manualEntryButton = document.querySelector(".blue-btn");
    if (manualEntryButton) {
        manualEntryButton.addEventListener("click", () => openModal("manual-entry-form"));
    } else {
        console.error("Manual Entry button not found!");
    }

    // Pictorial Entry
    const pictorialEntryButton = document.querySelector(".orange-btn");
    if (pictorialEntryButton) {
        pictorialEntryButton.addEventListener("click", () => openModal("pictorial-entry-form"));
    } else {
        console.error("Pictorial Entry button not found!");
    }

    // Confirm photo
    // const confirmPhotoButton = document.getElementById("confirm-photo");
    // if (confirmPhotoButton) {
    //     confirmPhotoButton.addEventListener("click", function () {
    //         const fileInput = document.getElementById("upload-photo");
    //         const imagePreview = document.getElementById("uploaded-image");

    //         if (fileInput && fileInput.files.length > 0) {
    //             const file = fileInput.files[0];
    //             const reader = new FileReader();
    //             reader.onload = function (e) {
    //                 if (imagePreview) {
    //                     imagePreview.src = e.target.result;
    //                     openModal("image-preview-section");
    //                 }
    //             };
    //             reader.readAsDataURL(file);
    //         } else {
    //             alert("Please select an image to upload.");
    //         }
    //     });
    // }
    

document.getElementById("ocr-form").addEventListener("submit", function (e) {
    const input = document.getElementById("upload-photo");
    if (!input.files[0]) {
        e.preventDefault(); // prevent form submission
        alert("Please select an image before submitting.");
    }
});

window.addEventListener("DOMContentLoaded", function () {
    const textForm = document.getElementById("text-form-section");
    if (textForm) {
        textForm.style.display = "block";
    }
});



    // document.getElementById("extract-text").addEventListener("click", function () {
    //     // Example: Populate the fields with dynamic values
    //       // This will pass the 'result' dictionary as a JSON object to JavaScript
    //     // Populate the input fields with the extracted data
    //     document.getElementById("field1").value = result.Name || "Default Name";  // Fallback if result.Name is undefined
    //     document.getElementById("field2").value = result.Amount || "Default Amount";
    //     document.getElementById("field3").value = result.Date || "Default Date";
    //     document.getElementById("field4").value = result.Category || "Default Category";
    
    //     // Hide the image preview and show the form
    //     document.getElementById("image-preview-section").style.display = "none";
    //     document.getElementById("text-form-section").style.display = "block";
    // });
    
    
    function closeModal(id) {
        document.getElementById(id).style.display = "none";
        document.getElementById("image-preview-section").style.display = "block"; // return to image preview
    }
    

    // Add Expense
    const addExpenseButton = document.getElementById("add-expense");
    const transactionList = document.getElementById("transaction-list");
    const amountInput = document.getElementById("amount");
    const dateInput = document.getElementById("date");
    const categoryInput = document.getElementById("category");

    let transactionCount = 5;

    // if (addExpenseButton) {
    //     addExpenseButton.addEventListener("click", function (e) {
    //         e.preventDefault();
    //         const amount = amountInput?.value.trim();
    //         const date = dateInput?.value.trim();
    //         const category = categoryInput?.value;

    //         if (!amount || !date || !category) {
    //             alert("Please fill all fields!");
    //             return;
    //         }

    //         // Display as list (optional if you have a separate list)
    //         const expenseList = document.getElementById("transaction-list-items");
    //         if (expenseList) {
    //             const listItem = document.createElement("li");
    //             listItem.innerHTML = `<strong>${category}</strong>: Rs.${amount} - ${date}`;
    //             expenseList.appendChild(listItem);
    //         }

    //         // Display in table
    //         if (transactionList) {
    //             const newRow = document.createElement("tr");
    //             newRow.innerHTML = `
    //                 <td>${transactionCount + 1}</td>
    //                 <td>${date}</td>
    //                 <td>${category}</td>
    //                 <td>Manual</td>
    //                 <td>Rs.${amount}</td>
    //             `;
    //             transactionList.insertBefore(newRow, transactionList.firstChild);

    //             while (transactionList.rows.length > 5) {
    //                 transactionList.removeChild(transactionList.lastChild);
    //             }

    //             [...transactionList.rows].forEach((row, index) => {
    //                 row.cells[0].textContent = index + 1;
    //             });
    //         }

    //         amountInput.value = "";
    //         dateInput.value = "";

    //         closeModal("manual-entry-form");
    //     });
    // } else {
    //     console.error("Add Expense button not found!");
    // }

    // Spending Data Visualization
    fetch('/spending_data')
        .then(response => response.json())
        .then(data => {
            let categories = {};
            let dates = {};
            const today = new Date();
            const currentMonth = today.toISOString().substring(0, 7);

            const currentMonthEntries = data.filter(entry => entry.date.startsWith(currentMonth));

            currentMonthEntries.forEach(entry => {
                categories[entry.category] = (categories[entry.category] || 0) + entry.amount;
                dates[entry.date] = (dates[entry.date] || 0) + entry.amount;
            });

            new Chart(document.getElementById("pieChart"), {
                type: 'pie',
                data: {
                    labels: Object.keys(categories),
                    datasets: [{
                        data: Object.values(categories),
                        backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff']
                    }]
                }
            });

            new Chart(document.getElementById("lineChart"), {
                type: 'line',
                data: {
                    labels: Object.keys(dates),
                    datasets: [{
                        label: "Daily Spending",
                        data: Object.values(dates),
                        borderColor: '#36a2eb',
                        fill: false
                    }]
                }
            });

            new Chart(document.getElementById("polarChart"), {
                type: 'polarArea',
                data: {
                    labels: Object.keys(categories),
                    datasets: [{
                        data: Object.values(categories),
                        backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Spending Distribution (Polar Area)'
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Error fetching spending data:", error));
});

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "block";
    else console.error("Modal not found:", modalId);
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "none";
    else console.error("Modal not found:", modalId);
}
