from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from Lollipop_Customers import views
from Project_Lollipop import settings

urlpatterns = [

    path('settings/profile/', views.profile_view, name="Customer Profile"),

    path('payment/', views.PackagesPageView.as_view(), name='home'),
    path('config/', views.stripe_config_view),  # new
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()),  # new
    path('cancelled/', views.CancelledView.as_view()),  # new
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
