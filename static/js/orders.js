//Dates
const start_date_field = document.getElementById("id_start_date");
const end_date_field = document.getElementById("id_end_date");
//Item/ItemDiv
const item_div = document.getElementById("order-form-item");
const item_type_field = document.getElementById("id_item_type_field");
const item_field = document.getElementById("id_item_field");
const item_field_hidden = document.getElementById("id_item_field_hidden");
const full_item_hidden = document.getElementById("id_full_item_hidden");
item_field.disabled = true;
item_field_hidden.style.display = "none";
full_item_hidden.style.display = "none";
//Prices/PriceDiv
const prices_div = document.getElementById("order-form-prices");
const initial_cost_field = document.getElementById("id_cost_initial");
const week_cost_field = document.getElementById("id_cost_week");

let end_date;
let start_date

//Applies onchange function to the start_date_field
start_date_field.onchange = function() {
    let tempDate = new Date(start_date_field.value);
    start_date = new Date(tempDate.getFullYear(), tempDate.getMonth(), tempDate.getDate());
    validateDates();
};
//Applies onchange function to the end_date_field
end_date_field.onchange = function() {
    let tempDate = new Date(end_date_field.value);
    end_date = new Date(tempDate.getFullYear(), tempDate.getMonth(), tempDate.getDate());
    validateDates();
};

/**
 * Firstly determines if both values exist.
 * Then compares the dates :
 * If the delivery is after the collection - invalid
 * If the delivery and collection are the same day - invalid
 * If these are not applicable, the dates are valid and the next step is available.
 */
function validateDates() {
    if (start_date && end_date) {
        if (start_date > end_date) {

            //needs to be able to set to none, if dates are changed afterwards
            item_div.style.display = "none";

        //Needs to be this specific, otherwise the time is included, which can allow same day
        //deliveries
        } else if (start_date.getDate() == end_date.getDate() &&
            start_date.getMonth() == end_date.getMonth() &&
            start_date.getFullYear() == end_date.getFullYear()) {

            //needs to be able to set to none, if dates are changed afterwards
            item_div.style.display = "none";

        } else {
            //valid dates - show the item select
            item_div.style.display = "block";
        }
    }
}