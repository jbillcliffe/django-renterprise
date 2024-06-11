const currentCustomerStatus = document.getElementById("customer-status-id")
const statusModal = new bootstrap.Modal(document.getElementById("statusModal"));
const modalContent = document.getElementById("modalBody");
const statusButtons = document.getElementsByClassName("status_button");
const statusConfirm = document.getElementById("statusConfirm");

for (let button of statusButtons) {
    button.addEventListener("click", (e) => {
        let modalInnerText = e.target.getAttribute("modal_inner_text");
        let statusValue = e.target.getAttribute("status_value");
        /*
        start by setting the css on modal-body to default, to prevent issues when reloading a window
        without refreshing the page
        */
        modalContent.className = "modal-body";
        console.log(document.getElementById("customer-status-id").textContent);
        console.log(document.getElementById("customer-status-id").innerHTML);
        if (currentCustomerStatus.textContent == "Deceased") {
            statusConfirm.style.display = "none";
            modalContent.innerHTML = "The customer is deceased, this cannot be changed without the assistance of an administrator.";
        } else {
            if (modalInnerText == "Archived" || modalInnerText == "archived" || modalInnerText == "ARCHIVED") {
                modalContent.classList.add("bold-warning-text");
                
                modalContent.innerHTML = 
                "If you mark the customer as 'Archived' it will "+
                "no longer be visible to regular users. Are you sure you wish to do this?";
                
            } else {
                modalContent.innerHTML = "Are you sure that you wish to change the status to "+modalInnerText+"?";
            }
            statusConfirm.style.display = "inline-block";
            statusConfirm.href = `status_change/${statusValue}`;
        }
        statusModal.show();
    });
}