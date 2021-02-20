from datetime import datetime

import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.db import IntegrityError
from django.db.models.functions import Log
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Lollipop_CRM.forms import CustomerForm, SenderForm, PackageForm, ReturnLabelForm
from Lollipop_CRM.models import Customer, Sender, Package, Profile, UserPermission, ReturnLabel


def dashboard(request):
    shipments = Package.objects.filter(package_date__month=datetime.now().month).count()
    labels = ReturnLabel.objects.filter(label_date__month=datetime.now().month).count()
    arrived = ReturnLabel.objects.filter(status="Arrived At Warehouse", label_date__month=datetime.now().month).count()
    transit = ReturnLabel.objects.filter(status="In Transit").count()
    customers = Customer.objects.count()
    recent_labels = ReturnLabel.objects.all().order_by('-id')[:10]
    context = {
        'shipments': shipments,
        'labels': labels,
        'arrived': arrived,
        'transit': transit,
        'customers': customers,
        'recent_labels': recent_labels
    }

    return render(request, template_name="CRM/dashboard.html", context=context)


def auth_login(request):
    role = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['userpassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            perm = UserPermission.objects.get(user=request.user)
            role = perm.role
            if perm.role == "Customer":
                return redirect('/crm/generate/return/label/')
            elif perm.role == "Admin":
                return redirect('/crm/dashboard')
        else:
            messages.error(request, 'Invalid username/password')

    form = AuthenticationForm()
    context = {
        'form': form,
        'role': role
    }

    return render(request, 'auth/auth-login.html', context=context)


def auth_signup(request):
    if request.method == "POST":
        email_address = request.POST.get("useremail")
        password = request.POST.get("userpassword")
        try:
            if validate_password(password, user=email_address) is None:
                user = User.objects.create(first_name=request.POST.get("first_name"),
                                           last_name=request.POST.get("last_name"),
                                           username=request.POST.get("useremail"),
                                           email=request.POST.get("useremail"),
                                           password=make_password(request.POST.get("userpassword")),
                                           is_active=False,
                                           is_staff=False,
                                           is_superuser=False,
                                           date_joined=datetime.now()
                                           )
                user.save()
                customer = Customer.objects.create(
                    customer_name=request.POST.get("first_name") + " " + request.POST.get("last_name"),
                    phone_number=request.POST.get("phone_number"),
                    email_address=request.POST.get("useremail"),
                    company=request.POST.get("company"),
                    address=request.POST.get("address"),
                    city=request.POST.get("city"),
                    customer_zip=request.POST.get("customer_zip"),
                    logo="customers/logo/alter-logo.png",
                    user=user)
                perms = UserPermission.objects.create(role="Customer", user=user)
                perms.save()
                customer.save()
                return redirect('/user/payment/')
        except TypeError:
            messages.error(request, "Please comply with the password requirements.")
        except ValidationError:
            messages.error(request, "Please comply with the password requirements.")
        except IntegrityError:
            messages.error(request, "User with this email address already exist.")

    help_text = password_validators_help_text_html()
    context = {
        'help_text': help_text
    }
    return render(request, 'auth/auth-register.html', context=context)


@login_required(login_url='/crm/accounts/login/')
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(data=request.POST, files=request.FILES)
        user = User.objects.create(username=request.POST.get("email_address"),
                                   first_name=request.POST.get("customer_name"),
                                   email=request.POST.get("email_address"), password=make_password("1234"))
        user.save()

        customer = Customer.objects.create(
            customer_name=request.POST.get("customer_name"),
            phone_number=request.POST.get("phone_number"),
            company=request.POST.get("company"),
            address=request.POST.get("address"),
            customer_zip=request.POST.get("customer_zip"),
            city=request.POST.get("city"),
            email_address=request.POST.get("email_address"),
            invoicing_email=request.POST.get("invoice_email"),
            invoicing_schedule=request.POST.get("invoicing_schedule"),
            payment_method=request.POST.get("payment_method"),
            rate_card=request.POST.get("rate_card"),
            user=user

        )
        customer.save()
        perms = UserPermission.objects.create(user=user, role="Customer")
        perms.save()
        messages.success(request, "Customer added successfully")

    return render(request, template_name='CRM/add-customers.html')


@login_required(login_url='/crm/accounts/login/')
def auth_logout(request):
    logout(request)
    return redirect('/crm/accounts/login/')


@login_required(login_url='/crm/accounts/login/')
def view_customer(request):
    customers = Customer.objects.all()

    context = {
        'customers': customers
    }

    return render(request, template_name='CRM/view-customers.html', context=context)


@login_required(login_url='/crm/accounts/login/')
def create_package(request):
    if request.method == "POST":
        sender = Sender.objects.create(
            sender_name=request.POST.get("sender_name"),
            sender_phone_number=request.POST.get("sender_phone_number"),
            sender_company=request.POST.get("sender_company"),
            sender_address=request.POST.get("sender_address"),
            sender_zip=request.POST.get("sender_zip"),
            sender_city=request.POST.get("sender_city"),
            sender_email_address=request.POST.get("sender_email_address"))

        receiver = Customer.objects.create(
            customer_name=request.POST.get("customer_name"),
            phone_number=request.POST.get("phone_number"),
            company=request.POST.get("company"),
            address=request.POST.get("address"),
            customer_zip=request.POST.get("customer_zip"),
            city=request.POST.get("city"),
            email_address=request.POST.get("email_address"))

        package = Package.objects.create(
            package_number=request.POST.get("package_number"),
            package_weight=request.POST.get("package_weight"),
            package_length=request.POST.get("package_length"),
            package_width=request.POST.get("package_width"),
            package_height=request.POST.get("package_height"),
            package_content=request.POST.get("package_content"),
            package_value=request.POST.get("package_value"),
            package_packaging=request.POST.get("package_packaging"),
            package_ref=request.POST.get("package_ref"),
            package_note=request.POST.get("package_note"),
            package_remarks=request.POST.get("package_remarks"),
            package_billing=request.POST.get("package_billing"),
            sender=sender,
            receiver=receiver
        )

        sender.save()
        receiver.save()
        package.save()

    return render(request, template_name='packages/create-package.html')


@login_required(login_url='/crm/accounts/login/')
def view_package(request):
    all_packages = Package.objects.all()
    context = {
        'all_packages': all_packages
    }

    return render(request, template_name='packages/view-packages.html', context=context)


@login_required(login_url='/crm/accounts/login/')
def package_label(request, package_number=None):
    package_details = Package.objects.filter(package_number=package_number)
    context = {
        'package_details': package_details
    }
    return render(request, template_name="CRM/label.html", context=context)


@login_required()
def view_registration_requests(request):
    requests = User.objects.filter(is_active=False)
    context = {
        'requests': requests
    }
    return render(request, 'auth/registration-requests.html', context=context)


@login_required()
def approve_registration_request(request, email):
    User.objects.filter(username=email).update(is_active=True)
    mail_subject = "Account Update"
    message = "Congratulations! Your account has been approved."
    # email = EmailMessage(
    #     mail_subject, message, from_email="noreply@simplereturn.io", to=[email]
    # )
    # email.send()
    send_mail(mail_subject, message, 'noreply@simplereturn.io', [email])
    return redirect('/crm/view/requests')


def generate_return_label(request):
    if request.method == "POST":
        total_label = ReturnLabel.objects.latest('id')

        internal_number = total_label.id + 1
        print("label", internal_number)
        now = datetime.now()
        internal_number = str(internal_number)

        current_year = now.year
        current_year = str(current_year)
        barcode_number = current_year + "000000" + str(internal_number)
        print("baaaar", barcode_number)
        # barcode = EAN13(barcode_number, writer=ImageWriter(), no_checksum=False)
        # barcode.save("media/images/return_labels/barcodes/"+barcode_number)
        ean = barcode.get('ean', barcode_number, writer=ImageWriter())
        print("cccccc", ean.get_fullcode())
        filename = ean.save("media/images/return_labels/barcodes/" + str(ean.get_fullcode()))
        customer = Customer.objects.get(user=request.user)
        label = ReturnLabel.objects.create(
            merchant_name=request.POST.get("merchant_name"),
            shipper=request.POST.get("shipper"),
            logo=request.POST.get("logo"),
            barcode="images/return_labels/barcodes/" + str(ean.get_fullcode()) + ".png",
            barcode_number=ean.get_fullcode(),
            status="In Transit",
            customer=customer
        )

        label.save()
        messages.success(request, "Label Generated. Go to > Labels > Return Labels, to view/print/copy the label.")
    customer_info = Customer.objects.get(user=request.user)

    context = {
        'customer_info': customer_info
    }
    return render(request, template_name="labels/generate-return-label.html", context=context)


def view_return_labels(request):
    customer = Customer.objects.get(user=request.user)
    labels = ReturnLabel.objects.filter(customer=customer)

    context = {
        'labels': labels
    }

    return render(request, template_name="labels/view-return-labels.html", context=context)


def print_return_label(request, barcode=None):
    label = ReturnLabel.objects.get(pk=barcode)
    context = {
        'label': label
    }
    return render(request, template_name="labels/print-return-label.html", context=context)


def info(request):
    return render(request, 'info.html')


def update_label_status(request):
    label = ""
    if request.method == "POST":
        label = ReturnLabel.objects.get(barcode_number=request.POST.get("barcode_number"))
        label.status = "Arrived At Warehouse"
        label.weight = request.POST.get("weight")
        label.save()

    context = {
        'label': label
    }
    return render(request, template_name="labels/update-label.html", context=context)


def view_arrived_labels(request):
    labels = ReturnLabel.objects.filter(status="Arrived At Warehouse")
    context = {
        'labels': labels
    }
    return render(request, template_name="reports/view-return-labels.html", context=context)


def view_intransit_lables(request):
    labels = ReturnLabel.objects.filter(status="In Transit")
    context = {
        'labels': labels
    }
    return render(request, template_name="reports/view-return-labels.html", context=context)
