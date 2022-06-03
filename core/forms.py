from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db import models

TYPE_CHOICES = (
    ('Donación', 'Donación'),
    ('Intercambio', 'Intercambio'),
)
CATEGORY_CHOICES = (
    'Educación',
    'Ropa',
    'Tecnología',
    'Mascotas',
    'Cocina',
    'Uso Cotidiano'
)

ESTRATO_CHOICES = (
    1,
    2,
    3
)

B_O_S_CHOICES = (
    'Producto',
    'Servicio'
)

DEPARTAMENTO_CHOICES = (
    'Amazonas',
    'Antioquia',
    'Arauca',
    'Atlántico',
    'Bolívar',
    'Boyacá',
    'Caldas',
    'Caquetá',
    'Casanare',
    'Cauca',
    'Cesar',
    'Chocó',
    'Córdoba',
    'Cundinamarca',
    'Guainía',
    'Guaviare',
    'Huila',
    'La Guajira',
    'Magdalena',
    'Meta',
    'Nariño',
    'Norte de Santander',
    'Putumayo',
    'Quindío',
    'Risaralda',
    'San Andrés y Providencia',
    'Santander',
    'Sucre',
    'Tolima',
    'Valle del Cauca',
    'Vaupés',
    'Vichada'
)


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CheckoutForm2(forms.Form):
    es_servicio = forms.Select()
    b_o_s = forms.ChoiceField(
        choices=B_O_S_CHOICES, required=False)
    nombre = forms.CharField()
    descripcion = forms.CharField()
    departamento = forms.Select()
    departamentos_list = forms.ChoiceField(
        choices=DEPARTAMENTO_CHOICES, required=False)
    ciudad = forms.CharField()
    email = forms.CharField()
    telefono = forms.CharField()
    categoria = forms.Select()
    categoria_list = forms.ChoiceField(
        choices=CATEGORY_CHOICES, required=False)
    tipo = forms.ChoiceField(
        widget=forms.RadioSelect, choices=TYPE_CHOICES)
    foto = forms.ImageField(required=False)
    intercambio = forms.CharField()
    terminos = forms.BooleanField(required=False)


class FundacionForm(forms.Form):
    nombre = forms.CharField()
    descripcion = forms.CharField()
    codigo_nit = forms.IntegerField()
    telefono = forms.IntegerField()
    estrato = forms.Select()
    estratos_list = forms.ChoiceField(
        choices=ESTRATO_CHOICES, required=False)
    foto = forms.ImageField(required=False)
    nombre_admin = forms.CharField()
    cc_admin = forms.IntegerField()
    departamento = forms.Select()
    departamentos_list = forms.ChoiceField(
        choices=DEPARTAMENTO_CHOICES, required=False)
    ciudad = forms.CharField()
    direccion = forms.CharField()

    terminos = forms.BooleanField(required=False)


class ComunicadoForm(forms.Form):
    es_urgente = forms.BooleanField(required=False)
    titulo = forms.CharField()
    descripcion = forms.CharField()
    email = forms.CharField()
    telefono = forms.CharField()
    foto = forms.ImageField(required=False)
    departamento = forms.Select()
    departamentos_list = forms.ChoiceField(
        choices=DEPARTAMENTO_CHOICES, required=False)
    ciudad = forms.CharField()
    direccion = forms.CharField()
    cuenta_ahorros = forms.CharField()
    especificaciones_cuenta = forms.CharField()

    terminos = forms.BooleanField(required=False)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
