const statusModal = new bootstrap.Modal(document.getElementById("statusModal"));
const modalContent = document.getElementById("modalBody");
const statusButtons = document.getElementsByClassName("status_button");
const statusConfirm = document.getElementById("statusConfirm");

for (let button of statusButtons) {
    button.addEventListener("click", (e) => {
        let modalInnerText = e.target.getAttribute("modal_inner_text");
        let statusValue = e.target.getAttribute("status_value");
        modalContent.innerHTML = "Are you sure that you wish to change the status to "+modalInnerText+"?";
        statusConfirm.href = `status_change/${statusValue}`;
        statusModal.show();
    });
}


