import uuid
from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from localflavor.gb.gb_regions import GB_REGION_CHOICES


# Create your models here.
class Customer(models.Model):
    """
    Fields for the customer model, mostly personal data
    Then string definition functions such as "full_name"
    To provide the first and surname together when the function
    is called
    """

    null_values = [None, 'None', 'none', 'null', 'Null']
    CURRENT = 0
    DECEASED = 1
    ARCHIVED = 2
    STATUS = (
        (CURRENT, 'Current'),
        (DECEASED, 'Deceased'),
        (ARCHIVED, 'Archived'),
    )

    customer_token = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    address_line_one = models.CharField(max_length=200)
    # sometimes people only have a first line before
    # town is the next entry
    address_line_two = models.CharField(max_length=200,
                                        blank=True,
                                        null=True)
    address_line_three = models.CharField(max_length=200,
                                          blank=True,
                                          null=True)
    address_line_town = models.CharField(max_length=200)
    address_line_county = models.CharField(choices=GB_REGION_CHOICES)
    # longest UK postcode would be 8 characters including a space
    postcode = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=CURRENT)

    # order by last_name then first_name
    # (last name more common for searches)
    class Meta:
        ordering = ["last_name", "first_name"]

    def full_name(self):
        """
        Self contained function to get first and last name by
        calling a function
        """
        if self.first_name in self.null_values:
            return f"{self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

    def status_str(self):
        """
        Returning the human readable version of status
        """
        return self.STATUS[self.status][1]

    def customer_css_status(self):
        """
        Returning the css ready version of status (noteably
        in lower case)
        """
        self = str(self.STATUS[self.status][1]).lower()
        return self

    def __str__(self):
        """
        String representation of the customer object.
        """
        if self.first_name in self.null_values:
            return f"{self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"


class CustomerNote(models.Model):
    """
    Fields for the customer note model, assigns it to a customer
    and states who created it and when they did.
    Then string definition functions such as "full_name"
    To provide the first and surname together when the function
    is called
    """
    null_values = [None, 'None', 'none', 'null', 'Null']

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer"
    )
    note = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_by"
    )

    def __str__(self):
        """
        String representation of the customer note object.
        """
        return f"Customer Note : {self.id}"

    def full_name(self):
        """
        Self contained function to get first and last name by
        calling a function
        """
        if self.customer.first_name in self.null_values:
            return f"{self.customer.last_name}"
        else:
            return f"{self.customer.first_name} {self.customer.last_name}"

    def created_on_by(self):
        """
        Self contained function to convert the saved datetime to a way
        that is preferred to display in the UK
        """
        date_to_string = self.created_on.strftime("%d-%m-%Y")

        return f"Created on : {date_to_string}, By : "
        f"{self.created_by.username}"

    class Meta:
        ordering = ["created_on", "id"]
