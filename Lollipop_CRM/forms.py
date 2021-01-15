from django.forms import ModelForm

from Lollipop_CRM.models import Customer, Sender, Package, ReturnLabel


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class SenderForm(ModelForm):
    class Meta:
        model = Sender
        fields = '__all__'


class PackageForm(ModelForm):
    class Meta:
        model = Package
        fields = '__all__'


class ReturnLabelForm(ModelForm):
    class Meta:
        model = ReturnLabel
        fields = '__all__'
