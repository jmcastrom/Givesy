import random
import string

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, render

from .forms import CheckoutForm, CheckoutForm2, CouponForm, RefundForm, PaymentForm, FundacionForm,  ComunicadoForm
from .models import Item, Item2, OrderItem, OrderItem2, Order, Order2, Address, Payment, Coupon, Refund, UserProfile, CustomUser, Fundacion, Comunicado

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")

# Crear instancia de modelo producto (crear producto con los datos q de el ususario para que apqarezca)
# https://docs.djangoproject.com/en/4.0/ref/models/instances/#:~:text=To%20create%20a%20new%20instance,you%20need%20to%20save()%20.


class CheckoutView2(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm2()
        context = {
            'form': form,
        }
        return render(self.request, "checkout2.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm2(self.request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
        terminos = self.request.POST.get('terminos')
        if(terminos.__eq__('on')):
            messages.success(
                self.request, "Producto publicado correctamente")
            nombre = self.request.POST.get('nombre')
            descripcion = self.request.POST.get('descripcion')
            auto_slug = Item2.generate_slug(nombre.replace(" ", ""))
            servicio = self.request.POST.get('es_servicio')
            es_servicio = False
            if(servicio.__eq__('Servicio')):
                es_servicio = True
            ofertante_nombre = self.request.user
            ofertante = CustomUser.objects.get(
                username=ofertante_nombre)
            intercambio = self.request.POST.get('intercambio')
            print("intercambio:hhhhhh")
            print(intercambio)
            print("hhhhhhhh")
            busca_intercambio = False
            if(not(intercambio.__eq__(''))):
                busca_intercambio = True
            print("ofertanto")
            print(self.request)
            print(type(ofertante))
            print(ofertante)
            newProducto = Item2(es_servicio=es_servicio, busca_intercambio=busca_intercambio, title=nombre.lower().capitalize(), ofertante=ofertante, description=descripcion.lower().capitalize(), departamento=self.request.POST.get(
                'departamento'), ciudad=self.request.POST.get('ciudad').lower().capitalize(), intercambio=self.request.POST.get('intercambio'), categoria=self.request.POST.get('categoria'),
                tipo=self.request.POST.get('tipo'), slug=auto_slug, image=self.request.FILES['foto'], telefono=self.request.POST.get('telefono'), email=self.request.POST.get('email'))
            newProducto.save()
            id = newProducto.idProducto
            ofertante.productos_ofertados.append(id)
            ofertante.save()
            print(ofertante.productos_ofertados)
            newProducto.save()
            # CustomUser.objects.filter(username=ofertante_nombre).update(
            #   productos_ofertados.append(id))
            # self.update(productos_ofertados=Append(
            #   'productos_ofertados', id))
            # print(self.request.productos_ofertados)
            print("Producto creado correctamente")
            print(CustomUser.objects.filter(username=ofertante))
        return redirect("/")


class VistaRegistrarFundacion(View):
    def get(self, *args, **kwargs):
        form = FundacionForm()
        context = {
            'form': form,
        }
        return render(self.request, "crear_fundacion.html", context)

    def post(self, *args, **kwargs):
        form = FundacionForm(self.request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            nombre = self.request.POST.get('nombre')
            descripcion = self.request.POST.get('descripcion')
            auto_slug = Fundacion.generate_slug(nombre.replace(" ", ""))
            admin_nombre = self.request.user
            admin = CustomUser.objects.get(
                username=admin_nombre)
            newFundacion = Fundacion(administrador=admin, nombre=nombre.lower().capitalize(), descripcion=descripcion.lower().capitalize(), departamento=self.request.POST.get(
                'departamento'), ciudad=self.request.POST.get('ciudad').lower().capitalize(), direccion=self.request.POST.get('direccion'), telefono=self.request.POST.get('telefono'),
                estrato=self.request.POST.get('estrato'), slug=auto_slug, image=self.request.FILES['foto'], nombre_admin=self.request.POST.get('nombre_admin'), cc_admid=self.request.POST.get('cc_admin'),
                codigo_nit=self.request.POST.get('codigo_nit'),)
            newFundacion.save()
            id = newFundacion.idFundacion
            admin.fundaciones.append(id)
            admin.save()
            newFundacion.save()
            messages.success(
                self.request, "Fundaci??n registrada correctamente")
            print("Producto creado correctamente")
        return redirect("/fundaciones/")


class VistaHacerComunicado(View):
    def get(self, *args, **kwargs):
        form = ComunicadoForm()
        context = {
            'form': form,
        }
        return render(self.request, "hacer_comunicado.html", context)

    def post(self, *args, **kwargs):
        form = ComunicadoForm(self.request.POST or None)
        # if form.is_valid():
        #   print(form.cleaned_data)
        print(self.request.POST.get('es_urgente'))
        urgencia = self.request.POST.get('es_urgente')
        es_urgente = False
        if(urgencia.__eq__('on')):
            es_urgente = True
        if(urgencia.__eq__('None')):
            es_urgente = False
        cuenta_ahorros = self.request.POST.get('cuenta_ahorros')
        print(cuenta_ahorros)
        tiene_cuenta = False
        if(not(cuenta_ahorros.__eq__(''))):
            tiene_cuenta = True
        titulo = self.request.POST.get('titulo')
        descripcion = self.request.POST.get('descripcion')
        auto_slug = Fundacion.generate_slug(titulo.replace(" ", ""))
        autor_nombre = self.request.user
        autor = CustomUser.objects.get(
            username=autor_nombre)
        newComunicado = Comunicado(es_urgente=es_urgente, autor=autor, titulo=titulo.lower().capitalize(), descripcion=descripcion.lower().capitalize(), departamento=self.request.POST.get(
            'departamento'), ciudad=self.request.POST.get('ciudad').lower().capitalize(), direccion=self.request.POST.get('direccion'), telefono=self.request.POST.get('telefono'),
            email=self.request.POST.get('email'), slug=auto_slug, tiene_cuenta=tiene_cuenta, image=self.request.FILES['foto'], cuenta_ahorros=self.request.POST.get('cuenta_ahorros'), especificaciones_cuenta=self.request.POST.get('especificaciones_cuenta'))
        newComunicado.save()
        id = newComunicado.idComunicado
        autor.comunicados.append(id)
        autor.save()
        newComunicado.save()
        print("oe q paso")
        print(newComunicado.es_urgente)
        messages.success(
            self.request, "Comunicado realizado con ??xito")
        print("Producto creado correctamente")
        return redirect("/comunicados/")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


class HomeView(ListView):
    model = Item2
    paginate_by = 15
    template_name = "home.html"


class VistaServiciosLista(ListView):
    model = Item2
    paginate_by = 15
    template_name = "servicios_lista.html"


class VistaComunicadosLista(ListView):
    model = Comunicado
    paginate_by = 15
    template_name = "comunicados_lista.html"


class VistaFundacionesLista(ListView):
    model = Fundacion
    paginate_by = 15
    template_name = "fundaciones_lista.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order2.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item2
    template_name = "product.html"


class VistaServicio(DetailView):
    model = Item2
    template_name = "servicio.html"


class VistaFundacion(DetailView):
    model = Fundacion
    template_name = "fundacion.html"


class VistaComunicado(DetailView):
    model = Comunicado
    template_name = "comunicado.html"


@ login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item2, slug=slug)
    order_item, created = OrderItem2.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order2.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order2.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@ login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item2, slug=slug)
    order_qs = Order2.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem2.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@ login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item2, slug=slug)
    order_qs = Order2.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@ login_required
def delete_product(request):
    request.delete()
    messages.success(request, "Producto eliminado correctamente")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
