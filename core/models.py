from re import A
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.forms import BooleanField
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

import random


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('D', 'Donación'),
    ('I', 'Intercambio')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    contact_link = models.CharField(max_length=200, blank=True, null=True)
    productos_ofertados = ArrayField(models.IntegerField(
        blank=True, null=True), blank=True, null=True, default=list)


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class Item2(models.Model):
    idProducto = models.AutoField(primary_key=True, editable=True)
    es_servicio = models.BooleanField(blank=True, default=False)
    ofertante = models.ForeignKey(
        CustomUser, related_name='Ofertante', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    departamento = models.CharField(max_length=15, blank=True)
    ciudad = models.CharField(max_length=20, blank=True)
    categoria = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=15, blank=True)
    intercambio = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if(self.es_servicio):
            return reverse("core:servicio", kwargs={
                'slug': self.slug})
        return reverse("core:product", kwargs={
            'slug': self.slug})

    def generate_slug(name):
        a = random.randint(1, 429496729)
        a = str(a)
        slug = name+a
        return slug

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_delete_product(self):
        self.delete()
        # CUANDO SE ELIMINE UN PRODUCTO TAMBNN SE DEBE BORRAR EL ID DEL OFERTANTE.PRODUCTOS_OFERTADOS

        # messages.success(
        #   self.request, "Producto eliminado correctamente")
        return redirect("/")


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class OrderItem2(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item2, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Order2(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem2)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username


class Fundacion(models.Model):
    idFundacion = models.AutoField(primary_key=True, editable=True)
    administrador = models.ForeignKey(
        CustomUser, related_name='Administrador', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True)
    telefono = models.IntegerField(blank=True)
    estrato = models.IntegerField(blank=True)
    cc_admid = models.CharField(max_length=25, blank=True)
    departamento = models.TextField()
    ciudad = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=20, blank=True)
    codigo_nit = models.CharField(max_length=20, blank=True)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("core:fundacion", kwargs={
            'slug': self.slug
        })

    def generate_slug(name):
        a = random.randint(1, 429496729)
        a = str(a)
        slug = name+a
        return slug

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_delete_foundation(self):
        self.delete()
        # messages.success(
        #  self.request, "Producto eliminado correctamente")
        return redirect("/")


class Comunicado(models.Model):
    idComunicado = models.AutoField(primary_key=True, editable=True)
    es_urgente = models.BooleanField(blank=True, default=False)
    autor = models.ForeignKey(
        CustomUser, related_name='Autor', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True)
    departamento = models.TextField()
    ciudad = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    cuenta_ahorros = models.CharField(max_length=20, blank=True)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("core:comunicado", kwargs={
            'slug': self.slug
        })

    def generate_slug(name):
        a = random.randint(1, 429496729)
        a = str(a)
        slug = name+a
        return slug

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_delete_comunicado(self):
        self.delete()
        # messages.success(
        #  self.request, "Producto eliminado correctamente")
        return redirect("/")


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=CustomUser)
