
from django.contrib import admin
from django.urls import path

from Lollipop_CRM import views

urlpatterns = [
    path('accounts/login/', views.auth_login, name="Login"),
    path('logout', views.auth_logout, name="Logout"),

    path('dashboard/', views.dashboard, name="Dashboard"),

    path('add/customer/', views.add_customer, name="Add Customer"),
    path('view/customer/', views.view_customer, name="View Customer"),
    path('create/package/', views.create_package, name="Create Package"),
    path('package/label/<str:package_number>/', views.package_label, name="Package Label"),
    path('view/packages/', views.view_package, name="View Package"),


    path('generate/return/label/', views.generate_return_label, name="Generate Return Label"),
    path('view/return/label/', views.view_return_labels, name="View Return Label"),
    path('print/return/<int:barcode>/label/', views.print_return_label, name="Print Return Label"),


    # """Registration""",
    path('accounts/signup/', views.auth_signup, name="Sign Up"),
    path('view/requests/', views.view_registration_requests, name="Registration Requests"),
    path('requests/<str:email>/approve/', views.approve_registration_request,
         name="Approve Registration Requests"),

    path('update/label/status/', views.update_label_status, name="Update Label Status"),

    path('view/arrived/labels/', views.view_arrived_labels, name="View Arrived Labels"),
    path('view/created/labels/', views.view_intransit_lables, name="View In Transit Labels"),


]
