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
const selected_item_hidden = document.getElementById("id_item");
const item_field_hidden = document.getElementById("id_item_field_hidden");
const full_item_hidden = document.getElementById("id_full_item_hidden");
const orders_hidden = document.getElementById("id_orders_hidden");

//Paginator Area
const table_paginator = document.getElementById("table-paginator");
let itemsPage = 1;
let maxPages = 1;

//Submit Button
const submitButton = document.getElementById("submitButton");
const testSubmitButton  = document.getElementById("formSubmitButton");
submitButton.style.display = "none";

available_items_div.style.display = "none";
selected_item_hidden.style.display = "none";
item_field_hidden.style.display = "none";
full_item_hidden.style.display = "none";
orders_hidden.style.display = "none";

let end_date;
let start_date

let defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.text = "---------";
    defaultOption.selected = true;

//Applies onchange function to the start_date_field
start_date_field.onchange = function() {
    clearAvailableItems();
    let tempDate = new Date(start_date_field.value);
    start_date = new Date(tempDate.getFullYear(), tempDate.getMonth(), tempDate.getDate());
    validateDates();
};
//Applies onchange function to the end_date_field
end_date_field.onchange = function() {
    let tempDate = new Date(end_date_field.value);
    end_date = new Date(tempDate.getFullYear(), tempDate.getMonth(), tempDate.getDate());
    clearAvailableItems();
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
    available_items_div.style.display = "none";
    selected_item_hidden.value = "";

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

            if (id_item_type_field.value != "" && item_field.value != "")
            {
                //if only the dates have been changed, and not the item. Then jump
                //to running this function and populating the orderable items.
                chosenItem();
            }
        }
    }
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
    let itemTypeObjects = item_field_hidden;
    
    clearAvailableItems();
    removeOptions(item_field);
    item_field.appendChild(defaultOption);
    clearAvailableAndPriceDiv();
    
    for (let i = 1; i < itemTypeObjects.length; i++) {
        //BUGFIX - Turns out single quoutes (') causes an error.
        //so the above process replaces them with double quotes (")
        //Then removes the Decimal text and brackets ( and ).
        //This allows it to be used with JSON.parse
        //https://stackoverflow.com/questions/15585569/simple-regex-replace-brackets
        //https://stackoverflow.com/questions/36038454/parsing-string-as-json-with-single-quotes
        let jsonItem = itemTypeObjects.options[i].value;
        jsonItem = removeBadJson(jsonItem);
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
        item_field.value = "";
    } else {
        item_field.disabled = false;
        item_field.addEventListener("change", chosenItem);
    }
}

/**
 * Function to set the initial pricing and display the pricing div when
 * an item has been chosen. It will then show the available items that can be chosen.
 * - item_field(element id/id_item_field") holds the ItemType id. 
 * - This is used to search the Item database for all instances of this ItemType
 * - Using these Item(s), each Item is searched for any Order(s) where the date clashes
 * - item_field.value is json string of {id,name,cost_initial,cost_week}
 * - list of Item(s) stored in full_item_hidden(element id/id_full_item_hidden)
 * - Item(s) stored with json string {id,item_type,item_serial,status}
 * - full list of Order(s)) stored in orders_hidden(element id/id_orders_hidden)
 * - Order(s) stored with json string {item_id,start_date_str,end_date_str}
 * 
 * Due to the nature of the search/filter. Pages need to be implemented in JS
 * in the validItems/validOrderableItems section. 
 */
function chosenItem() {

    clearAvailableItems();
    let selectedItemTypeId;

    if (item_field.value == "")
    {
        clearAvailableAndPriceDiv();
    } else {
        prices_div.style.display = "block";
        let itemJson = JSON.parse(item_field.value);
        selectedItemTypeId = itemJson.id;
        initial_cost_field.value = itemJson.cost_initial;
        week_cost_field.value = itemJson.cost_week;
    }

    let itemListObjects = full_item_hidden; //{id,item_type,item_serial,status}
    let orderHistoryObjects = orders_hidden; //{item_id,start_date_str,end_date_str}
    let validItems = [];
    let validOrderableItems = [];


    //go through each option in the hidden items. Turn it to JSON. Check for a value.
    //starts at 1 as the first (0) is a blank value. It will then return these values to
    //a new JSON Object Array.
    //{id,item_type,item_serial,status}
    for (let i = 1; i < itemListObjects.length; i++) {
        let jsonItem = itemListObjects.options[i].value;
        jsonItem = removeBadJson(jsonItem);
        jsonItem = JSON.parse(jsonItem);
        
        if(jsonItem.item_type == parseInt(selectedItemTypeId)) {
            validItems.push(jsonItem);
        } else {
            //do nothing
        }
    }

    //go through the items and check for date clashes from a previous order where item_id matches
    for (let x = 0; x < validItems.length; x++) {
        //check its available first
        if (validItems[x].status == 0) {
            //then compare against orders
            for (let i = 1; i < orderHistoryObjects.length; i++) {
                //{item_id,start_date_str,end_date_str}
                let jsonItem = orderHistoryObjects.options[i].value;
                jsonItem = removeBadJson(jsonItem);
                jsonItem = JSON.parse(jsonItem);

                history_start = new Date(jsonItem.start_date_str+" UTC");
                history_end = new Date(jsonItem.end_date_str+" UTC");

                if (validItems[x].id == jsonItem.item_id) {
                    //then check for date clashes from other orders
                    if (dateRangeInterceptionCalculator(start_date, end_date, history_start, history_end) == true) {
                        //passed all requirements, make this item orderable
                        validOrderableItems.push(validItems[x]);
                        break;
                    } else {
                        //Fails at date check, so this item will not be orderable for the new order date range.
                        break;
                    }
                } else {
                    //Item does not appear in this order
                    if (i == orderHistoryObjects.length - 1) {
                        //item has not appeared in any orders, this is the last one,
                        //so make it available for ordering.
                        validOrderableItems.push(validItems[x]);
                        break;
                    } else {
                        //not last order, so check the next one.
                        continue;
                    }
                }
            }
        } else {
            //Do not add as status check fails
            continue;
        }
    }

    //eg. 12 results would send a remainder of 2
    let pageRemainder = validOrderableItems.length % 5;
    // wholepages = 12 - 2 = 10, then divide by 5 = 2.
    //There will always be this number of pages + 1.
    let wholeDivisor = (validOrderableItems.length - pageRemainder)/5;
    console.log("R:"+pageRemainder);
    console.log("W:"+wholeDivisor);
    maxPages = wholeDivisor + 1;

    createOrderableItemsTable(validOrderableItems);
    available_items_div.style.display = "block";
    
}

function createOrderableItemsTable(validItemsArray) {
    console.log(validItemsArray);
    clearAvailableItems();

    // 0*5 = 0, 1*5 = 5, 2*5 = 10, 15 .....
    let thisStart = (itemsPage-1) * 5;
    let thisEnd;
    
    
    if ( thisStart+5 > validItemsArray.length) {
        //eg. 5 + 5 > 7
        thisEnd = validItemsArray.length;
    } else {
        //eg. 5 + 5 > 15
        thisEnd = thisStart + 5;
    }

    //let thisEnd = thisStart + 5;
    console.log(itemsPage);
    console.log(thisStart);
    console.log(thisEnd);
    //0-4, 5-9, 10-14, 15-19 ......
    for (let i = thisStart; i < thisEnd; i++) {
        /*  
            id:int,
            item_serial:string,
            item_type:int,
            status:int
        */
        if (validItemsArray[i].status == 0) {
            const tableRow = document.createElement("div");
            tableRow.classList.add("table-row", "order-table-row");
            tableRow.id = "order-row-number-"+i;
            const serialDiv = document.createElement("div");
            serialDiv.classList.add("col-8", "note-row");
            const serialP = document.createElement("p");
            serialP.innerHTML = validItemsArray[i].item_serial;
            const radioDiv = document.createElement("div");
            radioDiv.classList.add("col-4");
            const radioElement = document.createElement("input");

            radioElement.setAttribute("type", "radio");
            radioElement.setAttribute("id", validItemsArray[i].id);
            radioElement.setAttribute("name", "order_item_radio");

            //create a function to change the hidden item <select> this will
            //make is straight forward for form submission.
            radioElement.onclick = function() {
                selected_item_hidden.value = validItemsArray[i].id;
                submitButton.style.display = 'block';
                testSubmitButton.style.display = 'block';
            }
            //add elements to divs
            serialDiv.appendChild(serialP);
            radioDiv.appendChild(radioElement);
            //add divs to row
            tableRow.appendChild(serialDiv);
            tableRow.appendChild(radioDiv);
            //add row to available-items "table" before the paginator footer
            available_items_div.insertBefore(tableRow, table_paginator);
        }
    }

    updatePaginator(validItemsArray);
}

function updatePaginator(itemsArray) {
    //paginator-page-text = page X of X/Y
    //table-paginator = holder of << < > >>
    //paginate every 4 items.
    //itemsPage is a global var which determines current page selection, default page 1]
    //itemsPage = 1;

    let paginatorText = document.getElementById("paginator-page-text");
    let arrowList = table_paginator.getElementsByClassName("paginate-arrows");
    
    console.log(itemsPage);
    console.log(maxPages);

    while (arrowList.length > 0)
    {
        arrowList[0].remove();
    }

    if (itemsArray.length < 5) {
        // 1 page
        paginatorText.innerHTML = "Page 1 of 1";
    
    } else if (itemsArray.length <= 0) {
        // 0 items
        paginatorText.innerHTML = "No Items";

    } else {
        //Enough items for more than one page.

        // for javascript it will be simpler and more reliable to just use one step pages
        // also for the feature requirement only one step is necessary
        const aNearLeft = document.createElement("a");
        const aNearRight = document.createElement("a");

        aNearLeft.onclick = function() {
            console.log("B:"+itemsPage);
            itemsPage--;
            console.log("A:"+itemsPage);
            createOrderableItemsTable(itemsArray);
        };

        aNearRight.onclick = function() {
            console.log("B:"+itemsPage);
            itemsPage++;
            console.log("A:"+itemsPage);
            createOrderableItemsTable(itemsArray);
        };

        aNearLeft.classList.add("paginate-arrows");
        aNearRight.classList.add("paginate-arrows");

        aNearLeft.innerHTML = `<i class="fa-solid fa-angle-left"></i>`;
        aNearRight.innerHTML = `<i class="fa-solid fa-angle-right"></i>`;

        //<a href="?page=1" class="paginate-arrows" style="display:none;"><i class="fa-solid fa-angles-left"></i></a>
        //<a href="?page={{ page_obj.next_page_number }}" class="paginate-arrows"><i class="fa-solid fa-angle-right"></i></a>

        

        if (itemsPage == 1) {
            aNearLeft.style.display = "none";
            aNearRight.style.display = "block";

            //aNearLeft.href = "#";
            //aNearRight.href = "?page=2";

        } else if (itemsPage == maxPages) {
            aNearLeft.style.display = "block";
            aNearRight.style.display = "none";

            //aNearLeft.href = "?page="+(maxPages-1);
            //aNearRight.href = "#";
        } else {
            aNearLeft.style.display = "block";
            aNearRight.style.display = "block";

            //aNearLeft.href = "?page="+(itemsPage-1);
            //aNearRight.href = "?page="+(itemsPage+1);
        }

        paginatorText.innerHTML = `Page ${itemsPage} of ${maxPages}`;

        table_paginator.insertBefore(aNearLeft, paginatorText);
        table_paginator.appendChild(aNearRight);
        console.log(aNearLeft);
        console.log(aNearRight);
    }
}

/**
 * Function to empty the items available to order so the table doesnt fill up with duplicates
 * when fields are changed.
 * - gets all elements with class "order-table-row"
 * - uses a while loop to detect if there are any left in element array
 * - if there is, it will remove index 0 and keep doing this until length = 0
 */
function clearAvailableItems() {
    selected_item_hidden.value = "";
    submitButton.style.display = 'none';
    rowList = document.getElementsByClassName("order-table-row");
    while (rowList.length > 0)
    {
        rowList[0].remove();
    }
}



function clearAvailableAndPriceDiv() {
    prices_div.style.display = "none";
    initial_cost_field.value = "";
    week_cost_field.value = "";
    available_items_div.style.display = "none";
    selected_item_hidden.value = "";
    submitButton.style.display = 'none';
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
 * 
 * @param {Date} deliveryDate 
 * @param {Date} collectionDate 
 * @param {Date} orderDelivery 
 * @param {Date} orderCollection 
 * 
 * A function to calculate if the date range on a new order is going to intercept
 * an old order. If it does, the function returns false to imply it is invalid.
 */
function dateRangeInterceptionCalculator(deliveryDate, collectionDate,
                                         orderDelivery, orderCollection) {
    /*Situations -     
                      |---------OLDORDER---------|
    1.        |----NEWORDER----|                      
    2.                                |----NEWORDER----|
    3.                    |----NEWORDER----|
    4. |--NEWORDER--|             
    5.                                               |--NEWORDER--|
    6.   |--NEWORDER--|
    7.                |--NEWORDER--|
    8.                                           |--NEWORDER--|
    9.                              |--NEWORDER--|

    4 & 5 are the only "true" values as the new order dates do not intercept the old order dates.
    */

    //validate delivery and collection to check if before historical order delivery
    if (deliveryDate < orderDelivery && collectionDate < orderDelivery) {
        //both new dates before delivery (4)
        return true;
    } else if (deliveryDate > orderCollection) {
        //collectionDate is required to be after delivery, so this will be true as
        //both dates will be after historical order collection. (5)
        return true;
    } else {
        //anything else clashes with the historical order
        return false;
    }
}