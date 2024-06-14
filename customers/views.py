
from datetime import datetime

from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from orders.models import Order, OrderNote, Invoice
from orders.forms import OrderNoteForm, InvoiceForm
from .models import Customer, CustomerNote
from .forms import CustomerForm, CustomerNoteForm


# Create your views here.
class CustomerList(ListView):
    """
    Class ListView to display the customers into a table.
    - queries the database and excludes all archived customers
    """
    paginate_by = 9
    model = Customer
    # Exclude archived customers
    queryset = Customer.objects.exclude(status=2)

    # Override original get_context_data to
    # allow sending of the application area.
    # This will allow DRY manipulation of the side-bar.html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def customer_view(request, customer_token):
    """
    Function to view a singular customer after being selected.
    -finds customer based on customer_token sent in URL
    -renders the template view and adds token, customer object and
     customer full name to context to be used in the template.
    """
    obj = get_object_or_404(Customer, customer_token=customer_token)

    # Render the template customer_view and send the found "Customer" to it.
    return render(
        request,
        "customers/customer_view.html",
        {
            # Add in custom context data to allow it's use in the template
            "customer": obj,
            "customer_token_value": customer_token,
            "full_name": obj.full_name,
        },
    )


def customer_status_change(request, customer_token, status):
    """
    Function to change the status on a customer based on a
    customer choice (status sent as an arguement).
    First gets the customer database entry by customer_token, then
    changes the status and updates the object.
    Finally sends a message back to prompt the user of the change.
    """
    customer = get_object_or_404(Customer, customer_token=customer_token)
    customer.status = status
    customer.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        'Customer status has been updated'
    )
    # Redirect after successful save
    return redirect('customers:customer_view', customer_token=customer_token)


def customer_create(request):
    """
    Function to display the customer_create.html template
    which will allow new customers to be added.
    - Also creates the form to be displayed in the "render".
    - Checks that the form "is_valid()" before creating the entry
    """
    customer_form = CustomerForm(request.POST)

    if request.method == "POST":
        # Check for form validity
        if customer_form.is_valid():
            # Save the form
            customer = customer_form.save(commit=False)
            customer.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer has been saved'
            )
            # Redirect after successful save
            return redirect('customers:customer_view',
                            customer_token=customer.customer_token)

    customer_form = CustomerForm()
    return render(
        request,
        "customers/customer_create.html",
        {
            "customer_form": customer_form,
        },
    )


class CustomerNotesList(ListView):
    """
    Function to display the notes of a customer in a ListView
    - Includes a paginator to only allow 7 results per page
    """
    paginate_by = 7
    model = CustomerNote
    # This pagination method will automatically send
    # list data as "customernote_list"
    template_name = "customers/customer_notes_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(
            Customer,
            customer_token=self.kwargs["customer_token"])

        return CustomerNote.objects.filter(
            customer=self.customer).order_by("created_on")

    def get_context_data(self, **kwargs):
        context = super(CustomerNotesList, self).get_context_data(**kwargs)
        # Add in custom context data to allow it's use in the template
        context['customer_token_value'] = self.customer.customer_token
        context['full_name'] = self.customer.full_name
        return context


def customer_add_notes(request, customer_token):
    """
    Function to display the customer_add_notes.html template
    which will allow new customer notes to be added.
    """
    # Get base customer
    customer = get_object_or_404(Customer, customer_token=customer_token)

    if request.method == "POST":
        customer_note_form = CustomerNoteForm(data=request.POST)
        # Check for form validity
        if customer_note_form.is_valid():
            # Add missing fields before database save
            customer_note = customer_note_form.save(commit=False)
            customer_note.customer = customer
            customer_note.created_by = request.user
            customer_note.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer note has been saved'
            )
            return redirect('customers:customer_notes_list',
                            customer_token=customer_token)
    # If not post, then create a blank form and render it to the
    # template and return additional context data"
    customer_note_form = CustomerNoteForm()
    return render(
        request,
        "customers/customer_add_notes.html",
        {
            "customer_note_form": customer_note_form,
            # Add in custom context data to allow it's use in the template
            "customer_token_value": customer_token,
            "full_name": customer.full_name,
        },
    )


def customer_view_notes(request, customer_token, id):
    """
    Function to display the customer_view_notes.html template
    which will allow new authorised users (pre-authorised) to update notes.
    Will also log date and user who did an update.
    https://docs.djangoproject.com/en/5.0/ref/request-response/
    """
    # getting initial note value to send to the form
    customer_note_get = get_object_or_404(CustomerNote, pk=id)
    customer_note_text = customer_note_get.note

    if request.method == "POST":
        customer_note_form = CustomerNoteForm(data=request.POST)
        if customer_note_form.is_valid():
            # build note/editname/editdate for records
            newnote = request.POST.get('note', '')
            editname = " By : "+request.user.username+")"
            editdate = " (Edited : "+datetime.utcnow().strftime('%d-%m-%Y')
            fullnote = ''.join([newnote, editdate, editname])
            customer_note_get.pk = id
            customer_note_get.note = fullnote
            customer_note_get.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Customer note has been updated'
            )
            return redirect('customers:customer_notes_list',
                            customer_token=customer_token)

    # set initial note in form to be what was previously saved
    customer_note_form = CustomerNoteForm(initial={"note": customer_note_text})
    return render(
        request,
        "customers/customer_view_notes.html",
        {
            "customer_note_form": customer_note_form,
            # Add in custom context data to allow it's use in the template
            "customer_token_value": customer_token,
            "full_name": customer_note_get.customer.full_name,
        },
    )


class CustomerOrderList(ListView):
    """
    A class list view for all the orders belonging to a customer
    - sets a paginator of 3 database entries per page.
    """
    paginate_by = 3
    model = Order
    template_name = "customers/customer_order_list.html"

    def get_queryset(self):
        self.customer = get_object_or_404(
            Customer,
            customer_token=self.kwargs["customer_token"])
        return Order.objects.filter(
            customer=self.customer).order_by("start_date")

    def get_context_data(self, **kwargs):
        context = super(CustomerOrderList, self).get_context_data(**kwargs)
        # Add in custom context data to allow it's use in the template
        context['customer_token_value'] = self.customer.customer_token
        context['full_name'] = self.customer.full_name
        context['customer_status'] = self.customer.status
        return context


def customer_order_view(request, customer_token, order_id):
    """
    Function to view a singular order after being selected.
    When creating the order view, loads in a "table" which
    includes pagination features.
    """

    # Find a singular Item object.
    obj = get_object_or_404(Order, pk=order_id)

    invoice_list = Invoice.objects.filter(
        order=obj.id).order_by("created_on").values()

    paginate_invoice_list = Paginator(invoice_list, 3)
    page_number = request.GET.get('page')

    try:
        # returns the desired page object
        page_obj = paginate_invoice_list.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginate_invoice_list.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginate_invoice_list.page(paginate_invoice_list.num_pages)

    invoice_form = InvoiceForm()

    return render(
        request,
        "customers/customer_order_view.html",
        {
            # Add in custom context data to allow it's use in the template
            "order": obj,
            "customer_order_id": obj.id,
            "invoice_list": invoice_list,
            "invoice_form": invoice_form,
            "page_obj": page_obj,
            "customer_token_value": customer_token,
            "full_name": obj.customer.full_name,
        },
    )


class OrderNotesList(ListView):
    """
    A class list view for all the notes belonging to an order
    - sets a paginator of 7 database entries per page.
    """
    paginate_by = 7
    model = OrderNote
    template_name = "customers/customer_order_notes_list.html"

    def get_queryset(self):
        self.order = get_object_or_404(
            Order, id=self.kwargs["order_id"])
        return OrderNote.objects.filter(
            order=self.order).order_by("created_on")

    def get_context_data(self, **kwargs):
        get_customer = get_object_or_404(
            Customer,
            customer_token=self.kwargs["customer_token"])
        # Add in custom context data to allow it's use in the template
        context = super(OrderNotesList, self).get_context_data(**kwargs)
        context['customer_token_value'] = self.kwargs["customer_token"]
        context['customer_order_id'] = self.order.id
        context['full_name'] = get_customer.full_name
        context['customer_status'] = get_customer.status
        return context


def add_order_notes(request, customer_token, order_id):
    """
    Function to add a new note to an order
    - Gets the order referenced to (by id) with get_object_or_404
    - This Order is then used as a reference as it is a required
    foreign key for the OrderNote model
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order_note_form = OrderNoteForm(request.POST)
        if order_note_form.is_valid():
            order_note = order_note_form.save(commit=False)
            order_note.order = order
            order_note.created_by = request.user
            order_note.save()

            messages.add_message(
                request, messages.SUCCESS,
                'Order note has been saved'
            )
            return redirect('customers:order_notes_list',
                            customer_token=customer_token,
                            order_id=order.id)

    order_note_form = OrderNoteForm()

    return render(
        request,
        "customers/customer_add_order_notes.html",
        {
            "order_note_form": order_note_form,
            "customer_token_value": customer_token,
            "customer_order_id": order_id,
            "full_name": order.customer.full_name,
        },
    )


def order_view_notes(request, customer_token, order_id, id):
    """
    Function to display the customer_view_notes.html template
    which will allow authorised users (pre-authorised in template)
    to update notes.
    Will also log date and user who did an update.
    """
    # getting initial note object
    order_note_get = get_object_or_404(OrderNote, pk=id)
    # getting note text from the note object
    order_note_text = order_note_get.note

    if request.method == "POST":
        order_note_form = OrderNoteForm(data=request.POST)
        if order_note_form.is_valid():
            # build note/editname/editdate for records
            newnote = request.POST.get('note', '')
            editname = " By : "+request.user.username+")"
            editdate = " (Edited : "+datetime.utcnow().strftime('%d-%m-%Y')
            fullnote = ''.join([newnote, editdate, editname])
            # change the note text value to the new built string
            order_note_get.note = fullnote
            order_note_get.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Order note has been updated'
            )
            return redirect('customers:order_notes_list',
                            customer_token=customer_token,
                            order_id=order_id)
    # set initial note in form to be what was previously saved
    order_note_form = OrderNoteForm(initial={"note": order_note_text})
    return render(
        request,
        "customers/customer_view_order_notes.html",
        {
            "order_note_form": order_note_form,
            "customer_token_value": customer_token,
            "customer_order_id": order_id,
            "full_name": order_note_get.order.customer.full_name,
        },
    )


def invoice_status_change(request, customer_token, order_id,
                          invoice_id, set_invoice):
    """
    Function to change the status on the invoice.
    True to false.
    """
    # get the original invoice
    invoice = get_object_or_404(Invoice, pk=invoice_id)

    # get the set_invoice value from request sent by the template
    # then interpret the string to boolean value to save
    if (set_invoice == "false" or set_invoice == "False"):
        invoice.status = False
    else:
        invoice.status = True

    invoice.save()
    messages.add_message(
        request, messages.SUCCESS,
        'Invoice status has been updated'
    )

    return redirect('customers:customer_order_view',
                    customer_token=customer_token,
                    order_id=order_id)


def invoice_create(request, customer_token, order_id,
                   amount_paid, note):
    """
    Function to build a new invoice based on data sent
    in the request. Form is built by Javascript in a modal
    window, because the modal can also display invoices.
    Data sent, is inserted into a new empty Invoice object
    in this function and then saved.
    """
    # Get Order object based on order id sent in request
    order = get_object_or_404(Order, pk=order_id)
    # Build the new Invoice object
    invoice = Invoice(
        created_on=datetime.utcnow(),
        order=order,
        note=note,
        amount_paid=Decimal(amount_paid),
        status=False)
    invoice.save()
    messages.add_message(
        request, messages.SUCCESS,
        'Invoice has been created'
    )
    # Return to the customer order view (reload the page)
    return redirect('customers:customer_order_view',
                    customer_token=customer_token,
                    order_id=order_id)
