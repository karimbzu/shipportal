from django.db import models


class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    customer_zip = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50)

    invoicing_email = models.CharField(max_length=100)
    invoicing_schedule = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    rate_card = models.CharField(max_length=50)

    logo = models.ImageField(upload_to="images/logo", blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name


class Sender(models.Model):
    sender_name = models.CharField(max_length=50)
    sender_phone_number = models.CharField(max_length=50)
    sender_company = models.CharField(max_length=50)
    sender_address = models.CharField(max_length=200)
    sender_zip = models.CharField(max_length=50)
    sender_city = models.CharField(max_length=50)
    sender_email_address = models.CharField(max_length=50)

    def __str__(self):
        return self.sender_name


class Package(models.Model):
    package_number = models.CharField(max_length=50)
    package_weight = models.CharField(max_length=50)
    package_length = models.CharField(max_length=50)
    package_width = models.CharField(max_length=50)
    package_height = models.CharField(max_length=50)
    package_content = models.CharField(max_length=100)
    package_value = models.CharField(max_length=50)
    package_packaging = models.CharField(max_length=50)
    package_ref = models.CharField(max_length=50)
    package_note = models.CharField(max_length=100)
    package_remarks = models.CharField(max_length=100)
    package_billing = models.CharField(max_length=100)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE)
    package_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.package_number


class Profile(models.Model):
    phone_number = models.CharField(max_length=25)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),

)


class UserPermission(models.Model):
    role = models.CharField(choices=ROLE_CHOICES, max_length=150)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class ReturnLabel(models.Model):
    merchant_name = models.CharField(max_length=50)
    shipper = models.CharField(max_length=400, null=True, blank=True)
    logo = models.ImageField(upload_to="images/return_labels/logos/")
    barcode = models.ImageField(upload_to="images/return_labels/barcodes/")
    barcode_number = models.CharField(max_length=400)
    status = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    label_date = models.DateField(auto_now_add=True)
