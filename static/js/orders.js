//Dates
const start_date_field = document.getElementById("id_start_date");
const end_date_field = document.getElementById("id_end_date");
//Item/ItemDiv
const item_div = document.getElementById("order-form-item");
const item_type_field = document.getElementById("id_item_type_field");
const item_field = document.getElementById("id_item_field");
item_field.disabled = true;
//Prices/PriceDiv
const prices_div = document.getElementById("order-form-prices");
const initial_cost_field = document.getElementById("id_cost_initial");
const week_cost_field = document.getElementById("id_cost_week");
//Available Items Area
const available_items_div = document.getElementById("available-items");
//Hidden Fields
const item_field_hidden = document.getElementById("id_item_field_hidden");
const full_item_hidden = document.getElementById("id_full_item_hidden");
const orders_hidden = document.getElementById("id_orders_hidden");

item_field_hidden.style.display = "none";
full_item_hidden.style.display = "none";
orders_hidden.style.display = "none";

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

/**
 * 
 * @param {*} selectElement - <select> sent for options removal
 * Function designed to clear a drop down menu before being
 * repopulated with values that are relvant to what has been picked
 * https://stackoverflow.com/questions/3364493/how-do-i-clear-all-options-in-a-dropdown-box
 */
function removeOptions(selectElement) {
    let i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
       selectElement.remove(i);
    }
}

/**
 * 
 * @param {string} stringToJson 
 * @returns JSON.parse ready string
 * 
 * A function to run through several RegEx replace patterns. Removing and replacing bad JSON
 * parse data. Requires a string that resembles a JSON object eg. { 'key1':'value1' }
 */
function removeBadJson(stringToJson) {
    stringToJson = stringToJson.replace(/'/g, "\"");
    stringToJson = stringToJson.replace(/None/g,"\"None\"");
    stringToJson = stringToJson.replace(/[()]/g, "");
    return stringToJson;
}
/**
  * Function to determine the actions of the drop down menu where an item is chosen
  * after a change is detected in the item category drop down.
  * The item <select> will display only items in the database which relate to the
  * category.
  * - 1. It clears the item <select>
  * - 2. It re-adds the default -------- option.
  * - 3. It iterates through the itemTypes in a hidden field 
  * which is content from the database.
  * - 4. If the category matches it will add it back into the item <select>
  */

id_item_type_field.onchange = function() {
    
    let selectedCategory = id_item_type_field.value;
    let itemTypeObject = item_field_hidden;
    removeOptions(item_field)

    let defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "---------";
        defaultOption.selected = true;
        item_field.appendChild(defaultOption);

    for (let i = 1; i < itemTypeObject.length; i++) {
        //BUGFIX - Turns out single quoutes (') causes an error.
        //so the above process replaces them with double quotes (")
        //Then removes the Decimal text and brackets ( and ).
        //This allows it to be used with JSON.parse
        //https://stackoverflow.com/questions/15585569/simple-regex-replace-brackets
        //https://stackoverflow.com/questions/36038454/parsing-string-as-json-with-single-quotes
        let jsonItem = itemTypeObject.options[i].value;
        jsonItem = removeBadJson(jsonItem)
        jsonItem = JSON.parse(jsonItem);

        if (jsonItem.category == selectedCategory)
        {
            let option = document.createElement("option");
            option.value = `{ "id": "${jsonItem.id}",
                              "name": "${jsonItem.name}",
                              "cost_initial": "${jsonItem.cost_initial_str}",
                              "cost_week": "${jsonItem.cost_week_str}"
                            }`;
            option.text = jsonItem.name;
            item_field.appendChild(option);
        }
    }
    
    // Event listener for the item chosing field added in this way. 
    //Because do not want the population of the <select> to fire a change event
    if (id_item_type_field.value == "") {
        item_field.disabled = true;
        item_field.removeEventListenerEventListener("change", chosenItem);
    } else {
        item_field.disabled = false;
        item_field.addEventListener("change", chosenItem);
    }
}

/**
 * Function to set the initial pricing and display the pricing div when
 * an item has been chosen. It will then show the available items that can be chosen.
 */
function chosenItem() {
    if (item_field.value == "")
    {
        prices_div.style.display = "none";
        initial_cost_field.value = "";
        week_cost_field.value = "";
    } else {
        prices_div.style.display = "block";
        let itemJson = JSON.parse(item_field.value);
        initial_cost_field.value = itemJson.cost_initial;
        week_cost_field.value = itemJson.cost_week;
    }
    
    let getSelectedItemTypeData = JSON.parse(item_field.value);
    let getSelectedItemId = getSelectedItemTypeData.id;
    let itemListObject = full_item_hidden;
    let validItems = [];
    //go through each option in the hidden items. Turn it to JSON. Check for a value.
    //starts at 1 as the first (0) is a blank value. It will then return these values to
    //a new JSON Object Array.
    for (let i = 1; i < itemListObject.length; i++) {
        let jsonItem = itemListObject.options[i].value;
        jsonItem = removeBadJson(jsonItem);
        jsonItem = JSON.parse(jsonItem);

        if(jsonItem.item_type == parseInt(getSelectedItemId)) {
            validItems.push(jsonItem);
        }  
    }
    console.log(validItems);
    for (let i = 0; i < validItems.length; i++) {
        /*
        id:57,
        item_serial:"CHEESE-SERIAL",
        item_type:25,
        status:0*/
        const tableRow = document.createElement("div");
        tableRow.classList.add("table-row");
        const serialDiv = document.createElement("div");
        serialDiv.classList.add("col-8");
        const serialP = document.createElement("p");
        serialP.innerHTML = validItems[i].item_serial;
        const radioDiv = document.createElement("div");
        radioDiv.classList.add("col-4");
        const radioElement = document.createElement("input");
        radioElement.setAttribute("type", "radio");
        radioElement.setAttribute("id", validItems[i].id);
        radioElement.setAttribute("name", "order_item_radio");

        serialDiv.appendChild(serialP);
        radioDiv.appendChild(radioElement);
        tableRow.appendChild(serialDiv);
        tableRow.appendChild(radioDiv);

        available_items_div.appendChild(tableRow);

    }
    //available_items_div.appendChild("{% include 'paginate.html' %}");
}