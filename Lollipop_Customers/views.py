import stripe
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Lollipop_CRM.models import Customer
from Project_Lollipop import settings


def profile_view(request):
    if request.method == "POST":
        customer = Customer.objects.get(user=request.user)
        customer.customer_name = request.POST.get("customer_name")
        customer.phone_number = request.POST.get("phone_number")
        customer.address = request.POST.get("address")
        customer.city = request.POST.get("city")
        customer.customer_zip = request.POST.get("customer_zip")
        customer.logo = (request.FILES["logo"])

        customer.save()

    info = Customer.objects.get(user=request.user)

    context = {
        'info': info
    }
    return render(request, template_name="ESR_Customers/profile.html", context=context)


class PackagesPageView(TemplateView):
    template_name = 'purchase_test.html'


# new
@csrf_exempt
def stripe_config_view(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'user/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'user/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Packages',
                        'quantity': 10,
                        'currency': 'eur',
                        'amount': '100',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'redirects/success.html'


class CancelledView(TemplateView):
    template_name = 'redirects/cancelled.html'
