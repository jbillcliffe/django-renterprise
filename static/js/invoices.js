
const invoiceModal = new bootstrap.Modal(document.getElementById("invoiceModal"));

//const modalContent = document.getElementById("modalBody");
const modalId = document.getElementById("invoiceModal")
const modalInvoiceId = document.getElementById("modal-id");
const modalInvoiceDate = document.getElementById("modal-date");
const modalInvoiceNote = document.getElementById("modal-note");
const modalInvoiceAmount = document.getElementById("modal-amount");
const modalInvoiceText = document.getElementById("modal-text");

const invoiceTableButtons = document.getElementsByClassName("button-table");
const invoiceConfirm = document.getElementById("invoiceConfirm");
const invoiceCancel = document.getElementById("invoiceCancel");

for (let button of invoiceTableButtons) {

    button.addEventListener("click", populateInvoiceModal);
}

function populateInvoiceModal() {

    let thisButton = this;
    let orderId = modalId.getAttribute("data-order-id");
    let invoiceStatus = thisButton.getAttribute("invoice-status");
    let invoiceId = thisButton.getAttribute("invoice-id");
    let invoiceDate = thisButton.getAttribute("invoice-date");
    let invoiceNote = thisButton.getAttribute("invoice-note");
    let invoiceAmount = thisButton.getAttribute("invoice-amount");

    modalInvoiceId.innerHTML = "Invoice No. :"+invoiceId;
    modalInvoiceDate.innerHTML = "<b>Date</b>: "+invoiceDate;
    modalInvoiceNote.innerHTML = invoiceNote;

    if (invoiceStatus == "False" || invoiceStatus == "false") { //if marked as unpaid 
        modalInvoiceAmount.innerHTML = "<b>Amount to pay</b>: £"+invoiceAmount;
        modalInvoiceText.innerHTML = "Do you wish to pay this invoice?"
        invoiceConfirm.href = `${orderId}/invoice_status/${invoiceId}/true`;
    } else {
        modalInvoiceAmount.innerHTML = "<b>Amount paid</b>: £"+invoiceAmount;
        modalInvoiceText.innerHTML = "Do you wish to mark this as unpaid?";
        invoiceConfirm.href = `${orderId}/invoice_status/${invoiceId}/false`;
    }

    invoiceModal.show();
}


