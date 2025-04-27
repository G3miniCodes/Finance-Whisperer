document.addEventListener("DOMContentLoaded", () => {
    const billForm = document.getElementById("bill-form");
    const billList = document.getElementById("bill-list");
    const floatingForm = document.getElementById("floating-form");
    const openFormBtn = document.getElementById("open-form-btn");
    const closeFormBtn = document.getElementById("close-form-btn");

    // Load stored bills on page load
    loadBills();

    // Open floating form
    openFormBtn.addEventListener("click", () => {
        floatingForm.style.display = "block";
    });

    // Close floating form
    closeFormBtn.addEventListener("click", () => {
        floatingForm.style.display = "none";
    });

    // Handle form submission
    billForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // Get input values
        const billName = document.getElementById("bill-name").value;
        const dueDate = document.getElementById("due-date").value;
        const amount = document.getElementById("amount").value;

        // Create bill object
        const bill = { name: billName, date: dueDate, amount: amount };

        // Store in local storage
        let bills = JSON.parse(localStorage.getItem("bills")) || [];
        bills.push(bill);
        localStorage.setItem("bills", JSON.stringify(bills));

        // Update the list
        addBillToList(bill);

        // Clear the form
        billForm.reset();
    });

    // Function to add a bill to the UI
    function addBillToList(bill) {
        const listItem = document.createElement("li");
        listItem.classList.add("bill-item");
        listItem.innerHTML = `
            ${bill.name} - ₹${bill.amount} (Due: ${bill.date})
            <button class="delete-btn">X</button>
        `;

        // Add delete event
        listItem.querySelector(".delete-btn").addEventListener("click", () => {
            removeBill(bill);
            listItem.remove();
        });

        billList.appendChild(listItem);
    }

    // Load bills from local storage
    function loadBills() {
        let bills = JSON.parse(localStorage.getItem("bills")) || [];
        bills.forEach(addBillToList);
    }

    // Remove bill from storage
    function removeBill(billToRemove) {
        let bills = JSON.parse(localStorage.getItem("bills")) || [];
        bills = bills.filter(bill => bill.name !== billToRemove.name || bill.date !== billToRemove.date);
        localStorage.setItem("bills", JSON.stringify(bills));
    }
});
