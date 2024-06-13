
//https://docs.djangoproject.com/en/5.0/howto/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const invoiceModal = new bootstrap.Modal(document.getElementById("invoiceModal"));

//const modalContent = document.getElementById("modalBody");
const modalId = document.getElementById("invoiceModal");
const modalInvoiceTitle = document.getElementById("modalLabel");
const modalInvoiceContent = document.getElementById("modal-content");
const modalInvoiceId = document.getElementById("modal-id");
const modalInvoiceDate = document.getElementById("modal-date");
const modalInvoiceNote = document.getElementById("modal-note");
const modalInvoiceAmount = document.getElementById("modal-amount");
const modalInvoiceText = document.getElementById("modal-text");

const modalInvoiceIdRow = document.getElementById("modal-id-row");
const modalInvoiceDateRow = document.getElementById("modal-date-row");
const modalInvoiceNoteRow = document.getElementById("modal-note-row");
const modalInvoiceAmountRow = document.getElementById("modal-amount-row");
const modalInvoiceTextRow = document.getElementById("modal-text-row");

const invoiceTableCreateButton = document.getElementById("create-invoice-load-modal");
invoiceTableCreateButton.addEventListener("click", populateInvoiceCreateModal);

const invoiceTableButtons = document.getElementsByClassName("button-table view invoice");
const invoiceConfirm = document.getElementById("invoiceConfirm");
const invoiceCancel = document.getElementById("invoiceCancel");

const orderId = modalId.getAttribute("data-order-id");

//const csrftoken = Cookies.get('csrftoken');

for (let button of invoiceTableButtons) {
    button.addEventListener("click", populateInvoiceDetailsModal);
}

function populateInvoiceCreateModal() {

    modalInvoiceContent.innerHTML=
    `<div id="modal-content" class="modal-content">
        <div class="modal-header">
            <h3 class="modal-title invoice" id="modalLabel">Create Invoice</h3>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div id="modalBody" class="modal-body">
            <form id="invoiceForm" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                <div id="div_id_amount_paid" class="mb-3">
                    <label for="id_amount_paid" class="form-label requiredField">
                        Amount <span class="asteriskField">*</span>
                    </label>
                    <input type="number" name="amount_paid" step="1.00" class="numberinput form-control" required="" id="id_amount_paid">   
                </div>
                <div id="div_id_note" class="mb-3">
                    <label for="id_note" class="form-label requiredField">
                        Note <span class="asteriskField">*</span>
                    </label>
                    <input type="text" name="note" class="textinput form-control" required="" id="id_note">
                </div>
                <div class="modal-footer">
                    <div class="row">
                        <button id="submitButton" type="submit" href="${orderId}/invoice_create/" class="button centre-align">Submit</button>
                        <a class="button centre-align" href="" data-bs-dismiss="modal">Cancel</a>
                    </div>
                    <a id="invoiceCancel" href="" class="btn btn-danger"
                        data-bs-dismiss="modal"><i class="fa-regular fa-circle-xmark"></i> Cancel </a>
                    <a id="invoiceConfirm" href="${orderId}/invoice_create/" class="btn
                        btn-success"><i class="fa-solid fa-sterling-sign"></i> Change </a>
                </div>
            </form>
        </div>
    </div>`;
    invoiceModal.show();
}

function populateInvoiceDetailsModal() {

    let thisButton = this;
    let invoiceStatus = thisButton.getAttribute("invoice-status");
    let invoiceId = thisButton.getAttribute("invoice-id");
    let invoiceDate = thisButton.getAttribute("invoice-date");
    let invoiceNote = thisButton.getAttribute("invoice-note");
    let invoiceAmount = thisButton.getAttribute("invoice-amount");

    let textString;
    let amountString;
    let hrefString;

    if (invoiceStatus == "False" || invoiceStatus == "false") { //if marked as unpaid 
        amountString = "<b>Amount to pay</b>: £"+invoiceAmount;
        textString = "Do you wish to pay this invoice?"
        hrefString = `${orderId}/invoice_status/${invoiceId}/true`;
    } else {
        amountString = "<b>Amount paid</b>: £"+invoiceAmount;
        textString = "Do you wish to mark this as unpaid?";
        hrefString = `${orderId}/invoice_status/${invoiceId}/false`;
    }

    modalInvoiceContent.innerHTML=
    `<div id="modal-content" class="modal-content">
        <div class="modal-header">
            <h3 class="modal-title invoice" id="modalLabel">Invoice Details</h3>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div id="modalBody" class="modal-body">
            <div id="modal-id-row" class="row">
                <h4 id="modal-id">Invoice No. : ${invoiceId}</h4>
            </div>
            <hr>
            <div id="modal-date-row" class="row">
                <p id="modal-date"><b>Date</b>: ${invoiceDate}</p>
            </div>
            <hr>
            <div id="modal-notes-row" class="row">
                <p id="modal-notes-title">Notes :</p>
                <p id="modal-note">${invoiceNote}</p>
            </div>
            <hr>
            <div id="modal-amount-row" class="row">
                <p id="modal-amount">${amountString}</p>
            </div>
            <div id="modal-text-row" class="row">
                <p id="modal-text">${textString}</p>
            </div>
            <div class="modal-footer" style="justify-content:space-between;">
                <a id="invoiceCancel" href="" class="btn btn-danger"
                    data-bs-dismiss="modal"><i class="fa-regular fa-circle-xmark"></i> Cancel </a>
                <a id="invoiceConfirm" href="${hrefString}" class="btn
                    btn-success"><i class="fa-solid fa-sterling-sign"></i> Change </a>
            </div>
        </div>
    </div>`;
    invoiceModal.show();
}


