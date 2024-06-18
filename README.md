# Renterprise - The Program
<div style="width:100%; height:100px; background-color:#1D5D40; margin-left:auto;margin-right:auto;">
<a href="https://portfolio4-django-renterprise-00869e0146b8.herokuapp.com//" target="_self">
            <img class="header-logo" src="readme/logo-readme-banner.png" alt="Renterprise"
                aria-label="Renterprise CRM software home page">
        </a>
</div>

***Click this banner to load the website.***

A secondary prototype for a rental booking system. To create orders for customers and provide them with hired equipment. This example is based on a company hiring mobility equipment. However, the stock is based on what your provide to it. Flexibility is key to this software.

More people are turning to rentals as the world finances are in disarray and they can have your product at a much more manageable  cost. 

This interface is developed using designs and features from [Portfolio 1](https://github.com/jbillcliffe/portfolio1-renterprise/ "Go to Portfolio 1 - Renterprise Website")[^4] and [Portfolio 3](https://github.com/jbillcliffe/portfolio3-booking-system/ "Go to Portfolio 3 - Renterprise Python Console Booking System")[^5].

**This software will improve your hire bookings right from the start!**

# User Experience Design

## Target Audience
- Current business owners ready to make a change to their software.
- A consumer who is ready to take on a new challenge.

## User Stories
- User stories and model structures created in GitHub Projects[^6]
![Image of GitHub projects user stories](readme/user-stories/user-stories.png)


## Wireframe Program Flow
Program flow wireframe was created using Figma[^1]. The image shows the processes through the stages of the software.
Some parts are still in development. New data structure implemented compared to Portfolio 3[^5].
![Image of wireframe created for Renterprise software](readme/design/django-renterprise-flow.png)

## Logo - Redocumented from Portfolio 1.
The logo was created using the website LOGO.com[^2]. It has been pulled from my previous Renterprise project for Portfolio 1[^4].

### Logo Process - Redocumented from Portfolio 1[^4].
Using their step by step builder a full brand could be created from scratch, firstly the selection of software industry was chosen as it was accurate and appropriate.

![Logo and brand creation for Renterprise, first step](readme/design/logo-step-1.png)

Next, it gave an overall palette choice, blues, greens etc. Given the fact that a product is trying to be sold, and green symbolises wealth it seemed like a logical decision.

![Logo and brand creation for Renterprise, second step](readme/design/logo-step-2.png)

The creator then asked for a styling of the font to be used, a modern font was the best choice as it is for a modern product.

![Logo and brand creation for Renterprise, third step](readme/design/logo-step-3.png)

The final font choice for the logo was then made and it displayed the generated logo with it.

![Logo and brand creation for Renterprise, fourth step](readme/design/logo-step-4.png)

This was then the branding provided.

![Full branding theme for Renterprise](readme/design/initial-brand-board.png)

## Responsive

Attempts were made to use a responsive tester from previous projects. However, due to every page requiring security clearance the page would not load.

![External access failure](readme/design/responsive-security-failure.png)

## Breakdown of Design - Redocumented from Portfolio 1[^4].

### Colour Theme
Colour theme was initially chosen and subsequently revised with Coolors.[^3] 
The overall palette was picked with the website tools which enabled complementary and contrasting colour choices based upon the initial colour from the logo.

![Initial colour palette for Renterprise](readme/design/initial-colour-palette.png)

# Features

## Existing Features

**Create Item**

Creating an item can be divided into two categories. The Item Type (stock option) and an Item (the owned stock option with a serial number)


***Add New Item Type***

A [form](readme/features/create-item/item-type/item-type-form.png "The Item Type form") that asks for little data, this is useful to allow quick adding of item types and with as few margins for error as possible. This security is further enhanced by form validation. A category to assign it to (categories used previously will mean that it can be joined together later on). [Validation](readme/features/create-item/item-type/validation-example.png "Form validation on item type creation") occurs on all the visible fields. It also uses Cloudinary[^7] to allow images to be stored externally and accessed remotely. These images are useful to provide continuity across items. Also featuring in this is django-crispy-forms[^102]. When complete a [success message](readme/features/create-item/item-type/success-prompt.png "Success prompt sent to user") is sent to the user.


***Add New Item***

A [form](readme/features/create-item/item/item-form.png "The Item form") that asks for very little data, this is useful to allow quick adding of it ems to stock and with as few margins for error as possible. This security is further enhanced by form validation. A category to assign it to (categories used previously will mean that it can be joined together later on). [Validation](readme/features/create-item/item/validation-example.png "Form validation on item creation") occurs on all the visible fields. When complete a [success message](readme/features/create-item/item/success-prompt.png "Success prompt sent to user") is sent to the user.

---

**Create Customer**

An easy to understand [form](readme/features/create-customer/customer-form.png "Overall view of the customer create form") which contains [floating labels](readme/features/create-customer/floating-labels.png "Showing floating labels inside textfields") to increase space available. It also features multiple points of [validation](readme/features/create-customer/validation-example.png "Form validation on customer creation") to ensure that there is a minimum amount of data required to create a customer.
Also features a drop down menu of [counties across the UK](readme/features/create-customer/localflavor.png "A sample of django-localflavor data in the dropdown"). Provided by django-localflavor[^101] python/django library. When complete a success message is sent to the user.

---

**Create Order**

More data is required for this [form](readme/features/create-order/order-form.png "Initial view of the order create form")/[complete form](readme/features/create-order/order-form-complete.png "Overall view of the order create form"). Requires a user to enter a delivery and collection [dates](readme/features/create-order/date-picker.png "View of the datepicker in use") will only validate if collection is after delivery, historical orders (dates before today) can be entered with no consequences.<br><br>
Orders are created in steps. First it asks for dates, secondly an item category then [item type](readme/features/create-order/item-to-order.png "View of the item selection in use")
The program searches the database for orders already on the system that match the item chosen, it will then filter any items out that are already booked in this date range. After filtering it will [display the items](readme/features/create-order/order-form-item-selection.png "Selecting the item to order") that can be chosen from the list of stock available. Once the item has been chosen, the submit button appears and it gets booked for those days and it will be unavailable to others in this date range. It does this and creates an initial invoice record (unpaid) into the system, once saved the user is [moved to another view](readme/features/create-order/order-view-page.png "Displaying the created order to the user."), which displays the order just created and gives a prompt to show it has been created. Finally, when the order is created it adds the amount paid onto the tally for the item. So it can be determined how much money an item has earned in rental payments.

---


**Creating Customer/Order Notes**

These two entries are discussed together as they perform the same function. But save into different places. Customer notes are designed to log communications with the customer across all of their orders. Order notes are entered within an order itself and are relevant only to the order.<br><br>
If no notes are available, a prompt is shown to the user : ([ Empty customer notes ](readme/features/create-notes/empty-customer-notes.png "Displaying empty customer notes prompt")/[ Empty order notes ](readme/features/create-notes/empty-order-notes.png "Displaying empty order notes prompt"))<br><br>
Entering a note uses django-summernote[^103], to allow for rich text editing : [ Summernote ](readme/features/create-notes/adding-notes.png "Adding notes to order/customer")<br><br>
When the note is created a [ success prompt ](readme/features/create-notes/success-prompt.png "Success for adding a note to an order/customer") is displayed and the user is sent back to the [customer notes list](readme/features/create-notes/customer-notes-list.png "Displaying all notes for the customer") / [order notes list](readme/features/create-notes/order-notes-list.png "Displaying all notes for an order").

---

**Creating Invoice, Paying Invoices, Marking Invoices Unpaid**

Invoices are key to the customer/order experience as this relates to the company being able to reliably get an income from the software.

***Updating Invoices***

---

[Select an invoice](readme/features/invoices/change/select-unpaid.png "Select invoice from a list")


*Mark Unpaid*

[Confirm the process](readme/features/invoices/change/mark-as-unpaid.png "Displaying modal with unpaid data to be paid")
->
[Success prompt displayed](readme/features/invoices/change/update-success-unpaid.png "Display success prompt and reload the order view to update the invoice table")

*Paying An Invoice*

[Confirm the process](readme/features/invoices/changes/mark-as-paid.png "Displaying modal with paid data to be unpaid")
->
[Success prompt displayed](readme/features/invoices/change/update-success-paid.png "Display success prompt and reload the order view to update the invoice table")

***Creating Invoices***

Displays a modal which has two fields of entry. One for the amount of the invoice and another for the text description for the invoice.

[Load the create invoice modal](readme/features/invoices/create/create-invoice.png "Displaying modal with paid data to be unpaid")
->
[Validate the fields to ensure clean data](readme/features/invoices/create/validation-example.png "Displaying modal with paid data to be unpaid").<br><br>
[When all data is in that is required](readme/features/invoices/create/create-invoice-data.png "Modal with all the required data inputted"). Clicking submit will take the user to the order view with an [updated table of invoices](readme/features/invoices/create/create-invoice-data-table.png "Table of invoices after window reload"). Along with this a [success prompt](readme/features/invoices/create/success-prompt.png "User prompt to show the created invoice") is generated for the user.

---

**List Displays**

---

***Customer***

[Shows all the customers](readme/features/lists/customers/customer-list.png "The list of customers available to the user") in the system. The only other status that is visible is deceased. If someone is marked as archived they become [restricted](readme/features/lists/customers/archived-customer-warning.png "User prompt to warn that the customer is archived") to all and can only be recovered by the user being re-opened in the django-admin back end.<br><br>
Once a customer has been clicked on, their [status](readme/features/lists/customers/customer-status.png "Part of the sidebar within a customer view") can be edited. <br>
A customer can be marked available, [deceased](readme/features/lists/customers/mark-as-deceased.png "User prompt to warn that the customer cannot be recovered at the front end") or [archived](readme/features/lists/customers/mark-as-archived.png "User prompt to warn that the customer cannot be recovered at the front end")<br><br>If they are deceased/archived only an administrator can [recover](readme/features/lists/customers/deceased-status-recovery-fail.png "User prompt to warn that the customer cannot be recovered at the front end") them to "Available", if they are deceased regular users can see them, but only administrators can unlock them back to "Available" in the back end.

---

***Items***
[Shows all the items](readme/features/lists/items/items-list.png "The list of items in the database") and their status is visible in the list view by the colour of the row. Their [status](readme/features/lists/items/item-status.png "Status options available to be selected by the user") can be changed within the [item view](readme/features/lists/items/item-view.png "Details that are on the item")

---

**Sidebar Navigation**
A key feature in the program. (Almost) all through the web application it provides options for the user and the list changes depending upon the users location in the site. Where applicable, one of the options will be highlighted to show where the user is currently active. It can also hold options such as "Add an Invoice" which brings up the modal window to create an invoice for an order. Examples of its use are below: <br><br>

![Example of sidebar use (1)](readme/features/sidebar/sidebar-1.png)<br>
![Example of sidebar use (2)](readme/features/sidebar/sidebar-2.png)<br>
![Example of sidebar use (3)](readme/features/sidebar/sidebar-3.png)

Although not principally designed for smaller devices such as mobile phones (it's designed to be a comprehensive CRM system) there is responsiveness which will, when the screen resolution is small enough, relocated the sidebar and collapse it at the top of the main container. The two below images show the sidebar at the top of this first image, oepned, after that showing them sidebar collapsed.

![Top location sidebar](readme/features/sidebar/sidebar-scaledown.png)<br>
![Top location sidebar collapsed](readme/features/sidebar/sidebar-scaledown-collapse.png)<br>

# Testing
---

## Linting
---

Given the framework involved. Using a standard linter was not strictly the best option. I did manage to install a a django specific linter called djLint which worked within the IDE, this was also combined with Flake8 and it also worked with the html templates too. No python files have any poorly formated areas of code. 
Except for in renterprise.settings where :
- Some setting strings are too long, but cannot be broken up and this would render them unusable.
- In the templates. Intially, I had some inline styles, now wherever possile they are part of the css style sheet.
- No errors arrive through the linter/template analysis.


## Manual Testing
---

This section is broken down into the different areas of the program and to how it is expected to function.

### Main Menu
---

- [x] Log out?     
- [x] Force log in?  
- [x] Register?            
- [x] Functioning nav buttons?            
- [x] Header logo back to home?
- [x] Social Media links?            

### Admin
---

- [x]  Able to edit existing entries?         
- [x]  Can only access as a user?              
- [x]  Force login if trying to access via url?   

### Create Customer
---

- [x]  Create customer fields valid where needs to be?           
- [x]  Validate clearly states where to edit?             
- [x]  Feedback on submission?                   
- [x]  Navigate to created customer on submission?        
- [x]  Drop down for counties for future filtering?                          
- [x]  Return to customer list button?  

### View Customer
---

- [x]  All fields clearly visible?
- [x]  Seperation of data to maximise use of space
- [x]  Side bar shows correct options?<br>
        1. [x] Back to customer list<br>
        2. [x] Display Name<br>
        3. [x] Customer Notes<br>
        4. [x] Customer Orders<br>
        5. [x] New Order<br>
        6. [x] Current status<br>
        7. [x] Change status buttons<br>
- [x]  Status buttons restrictons if archived/deceased?
- [x]  Status button updates customer?

### Customer List
---

- [x]  Pagination?
- [x]  List has clickable element to go to customer?
- [x]  Hide archived customers?
- [x]  Show customers who are deceased clearly?

### Customer Notes
---

- [x]  Show notes in a list format?
- [x]  View individual notes by permission (to then edit)?
- [x]  Add note button to go to create note screen?
- [x]  Pagination?
- [x]  Return To Customer button?
- [x]  Sidebar?<br>
        1. [x] Home<br>
        2. [x] Customer List (back to)<br>
        3. [x] Display name<br>
        4. [x] Customer Notes (active when on list screen)<br>
        5. [x] Add Customer Note (active when on note screen)<br>
- [x]  Return to notes list when note created

### Create Order
---

- [x]  Form presented in stages?
- [x]  Collection after delivery?
- [x]  Item has to be selected before moving forward to price?
- [x]  Default pricing inserted when item selected (can be changed)?
- [x]  Reset item if dates changed to something invalid?
- [x]  Hide create order button until all is valid?
- [x]  Only show valid orderable items for time period?
- [x]  Paginate items if necessary?
- [x]  Create first invoice on submission?
- [x]  Navigate to order view when submitted successfully.

### View Order
---

- [x]  Display all data clearly?
- [x]  Display item image?
- [x]  Sidebar correct?<br>
        1. [x] Home<br>
        2. [x] Customer List (back to)<br>
        3. [x] Display name<br>
        4. [x] Display order number<br>
        5. [x] Order Notes (active when on list screen)<br>
        6. [x] Add Invoice successfully loads modal?<br>
        7. [x] Customer orders (to order list)<br>
- [x]  Invoice window shows all invoices?
- [x]  Paginate invoices?
- [x]  View/Edit invoices?
- [x]  Create invoices?

### Order Notes
---

- [x]  Show notes in a list format?
- [x]  View individual notes by permission (to then edit)?
- [x]  Add note button to go to create note screen?
- [x]  Pagination?
- [x]  Return To Order button?
- [x]  Sidebar?<br>
        1. [x] Home<br>
        2. [x] Customer List (back to)<br>
        3. [x] Display name<br>
        4. [x] Display order number<br>
        4. [x] Order Notes (active when on list screen)<br>
        5. [x] Add Order Note (active when on note screen)<br>
- [x]  Return to order notes list when note created?

### Items List 
---

- [x] Show list of items?
- [x] Paginate list of items?
- [x] Clearly show status of items?
- [x] Sidebar correct?<br>
        1. [x] Home<br>
        2. [x] Item List (active when on list)<br>
        3. [x] New Item (active when creating item)<br>
        4. [x] New Item Type (active when creating item type)<br>
- [x] Can click an item to view it?

### Item View
---

- [x] Show data clearly?
- [x] Show item image?
- [x] Return to item list button?
- [x] Sidebar correct?<br>
        1. [x] Home<br>
        2. [x] Item List (active when on list)<br>
        3. [x] Current status display<br>
        4. [x] Edit status buttons, do not show button for current status<br>
- [x] Status buttons pop up modal to confirm.
- [x] Status change reloads window, showing new status

### New Item
---

- [x] Validate form fields?
- [x] Clearly display where data is required?
- [x] On save go to item view of the item made?

### New Item Type
---

- [x]  Validate fields?
- [x]  Allow empty image (will save as placeholder)?
- [x]  Clearly show where data required
- [x]  Return to items list on save
- []  Show previous categories 
This would be in a future release


# Deployment

To deploy this project:

- Fork and clone this repository to your local machine.
- Create a new Heroku app.
- In the Heroku dashboard, navigate to the app's settings and set the buildpacks to Python and NodeJS in that order.
- Connect your Heroku app to the repository by linking it to your forked copy of the repository.
- Click on the "Deploy" button in the Heroku dashboard.
- After following these steps, the app is successfully deployed to Heroku.

- NB. You would need your own Credentials from Google to operate your own google spreadsheets. Also a creds.json file would need to be implemented into your own code and added to the .gitignore.
- This creds file would then be copied and pasted into a VALUE in the Heroku App Settings.

[LIVE RENTERPRISE SOFTWARE](https://portfolio4-django-renterprise-00869e0146b8.herokuapp.com/ "Go to Renterprise")

# Technologies Used

## Languages

- HTML5
- CSS3
- Python 3
- Django Templates
- Javascript/jQuery

## Relevant Help Links
1. Back to customers etc.
https://stackoverflow.com/questions/524992/how-to-implement-a-back-link-on-django-templates

2. How to toggle class
//https://www.w3schools.com/howto/howto_js_toggle_class.asp

3. get_context help :
https://stackoverflow.com/questions/37370534/django-listview-where-can-i-declare-variables-that-i-want-to-have-on-template

4. A useful testing tool for debugging/testing<br><br>
import logging<br>
logger = logging.getLogger(__name__)<br>
logger.warning(trace) -> general.log<br>

5. Bootstrap kept overriding button style when it is unwanted.
Have to use javascript to submit the form and keep FloatingField styles
- A request to crispy forms to remove default bootstrap styling on form buttons.
- It was not ideal to work around. However, it was by creating the button in raw HTML
(customers/forms.py) lines 50/51
https://github.com/django-crispy-forms/django-crispy-forms/issues/158

6. Adding pagination to a non-class ListView
https://www.geeksforgeeks.org/how-to-add-pagination-in-django-project/

7. def invoice_create<br>
**Bug zone**<br>wsgirequest' object has no attribute 'amount_paid'<br>
Change to same type as status change, to implement as posting form
is causing problems. So values will be sent by URL.
the form created by JS. JS dynamically validates the fields
prior to submission.<br>
<b>Main fix was in the end dynamically and manipulating javascript to create the form for the modal window and functions associated with it.</b>

8. Best practice for django constants :
https://stackoverflow.com/questions/12822847/best-practice-for-python-django-constants


## Frameworks, Libraries & Programs Used

- Font Awesome[^5]
- Gitpod[^14]
- Figma[^1]
- Heroku[^7]
- Django Frameworks[^13]

# Technologies Used

## Python Libraries :
**Sourced from PyPI**[^8]
[^101]: django-localflavor is a package that offers additional functionality for particular countries or cultures : https://pypi.org/project/django-localflavor/
[^102]: django-crispy-forms is a package that allows greater form manipulation and quick template tag insertion :
https://django-crispy-forms.readthedocs.io/en/latest/
[^103]: django-summernote is a "WYSIWYG" text editor. Allows for rich text field entries.:
https://pypi.org/project/django-summernote/
[^104]: djlint a django template formatting analyser: https://open-vsx.org/extension/monosans/djlint
[^105]: Flake8 : https://marketplace.visualstudio.com/items?itemName=ms-python.flake8
bleach - an HTML sanitising library
cloudinary - an image hosting service to allow uploads and downloads
dj3-cloudinary-storage - part of the above package for hosting images
crispy-bootstrap5 - a bootstrap 5 styling for django-crispy-forms
gunicorn- Gunicorn is a Python WSGI HTTP Server for UNIX
psycopg2 - Implementation of a PostgreSQL adapter for Python
pylint-django - a python linter that incorporates django frameworks structure.
whitenoise - implified static file serving for Python web apps

*NB. There are other libraries but they were installed as part of others.

## Website Tutorials/References
- W3Schools[^10]
- Stack Overflow[^11]
- Pycode[^12]

# References 
[^1]: Figma is a free website for designing storyboards and wireframes : https://www.figma.com/
[^2]: LOGO website used for creating a logo and branding from scratch for free : https://app.logo.com/
[^3]: Coolors website for creating free colour themes : https://www.coolors.com/
[^4]: Renterprise Portfolio 1 - My own web design I created as part of my first project for Code Institute. This software is an extension of the idea of Renterprise: https://github.com/jbillcliffe/portfolio1-renterprise/
[^5]: Renterprise Portfolio 3 - My own python console program created as part of my third project for Code Institute. This software is an extension of the idea of Renterprise: https://github.com/jbillcliffe/portfolio3-booking-system/
[^6]: GitHub projects - A way of creating workflows for a project and being able to manage across teams.: https://github.com/users/jbillcliffe/projects/4
[^7]: Heroku - A place to host projects. In this case to host the python terminal. : https://www.heroku.com
[^8]: PyPI - the package index. Containg a whole wealth of python libraries to plug in: https://pypi.org/
[^10]: W3Schools- Invaluable for providing details on elements and their attributes and so much HTML/CSS information : https://www.w3schools.com/
[^11]: Stack Overflow - One of the most important resources for developers : https://stackoverflow.com/
[^12]: How to do correct formatting for PEP8 : https://peps.python.org/pep-0008/
[^13]: Django Frameworks. The framework that allows the operation of this as an MVC model : https://www.djangoproject.com/
[^14]: Gitpod, a cloud based IDE for developing the web application : https://www.gitpod.io
[^15]: Font Awesome - A great source of free icons to use in many formats : https://www.fontawesome.com
