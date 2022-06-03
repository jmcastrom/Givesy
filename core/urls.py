from django.urls import path
from .views import (
    ItemDetailView,
    VistaFundacion,
    CheckoutView,
    CheckoutView2,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    VistaFundacionesLista,
    VistaServiciosLista,
    VistaComunicadosLista,
    VistaServicio,
    VistaComunicado,
    VistaRegistrarFundacion,
    VistaHacerComunicado
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('servicios/', VistaServiciosLista.as_view(), name='servicios'),
    path('fundaciones/', VistaFundacionesLista.as_view(), name='fundaciones'),
    path('comunicados/', VistaComunicadosLista.as_view(), name='comunicados'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout2/', CheckoutView2.as_view(), name='checkout2'),
    path('registrarFundacion/', VistaRegistrarFundacion.as_view(),
         name='registrar-fundacion'),
    path('hacerComunicado/', VistaHacerComunicado.as_view(),
         name='hacer-comunicado'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('servicio/<slug>/', VistaServicio.as_view(), name='servicio'),
    path('comunicado/<slug>/', VistaComunicado.as_view(), name='comunicado'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('fundacion/<slug>/', VistaFundacion.as_view(), name='fundacion'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
