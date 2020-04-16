from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='Index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign-up/', views.RegisterFormView.as_view(), name='sign_up'),
    path('my-basket/', views.UserBasket.as_view(), name='user_basket'),
    path('order-success/', TemplateView.as_view(template_name="Lab1/order_success.html"), name='order-success' ),
    path('delete-order/',views.DeleteOrder.as_view(),name='delete-order'),
    path('admin-orders/',views.AdminOrders.as_view(),name='admin-orders'),
    path('ajax/basket-control/', views.BasketControl.as_view(), name='basket_control'),
    path('ajax/get-new-common-price', views.GetNewCommonPrice.as_view(), name='get_new_common_price')
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
