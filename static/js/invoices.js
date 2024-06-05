const invoiceModal = new bootstrap.Modal(document.getElementById("invoiceModal"));
const modalContent = document.getElementById("modalBody");
const invoiceTableButtons = document.getElementsByClassName("invoice-button");
const invoicePaidConfirm = document.getElementById("invoicePaid");
const invoiceUnpaidConfirm = document.getElementById("invoiceUnpaid");

for (let button of invoiceTableButtons) {
    button.addEventListener("click", (e) => {
        let invoice_id = e.target.getAttribute("invoice_id");
        let modalInnerText = e.target.getAttribute("modal_inner_text");
        modalContent.innerHTML = "Are you sure that you wish to change the status to "+modalInnerText+"?";
        invoicePaidConfirm.href = `invoice_pay/${invoice_id}`;
        invoiceUnpaidConfirm.href = `invoice_unpaid/${invoice_id}`;
        invoiceModal.show();
    });
}


