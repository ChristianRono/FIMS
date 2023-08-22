"""FIMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from Main.views import homepage,customer,tax,items,delete_invoice,delete_item,pdfprint,edit,edit_item,edit_customer,edit_tax,add_item,send_mail,profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',view=auth_views.LoginView.as_view(template_name="login.html"),name='homepage'),
    path('customer/',view=customer,name='homepage'),
    path('items/',view=items,name='homepage'),
    path('tax/',view=tax,name='homepage'),
    path('logout/',view=auth_views.logout_then_login,name='logout'),
    path('delete/invoice/<int:id>',view=delete_invoice,name="delete invoice"),
    path('delete/item/<int:id>',view=delete_item,name="delete item"),
    path('print/<int:id>/',view=pdfprint,name="print"),
    path('edit/invoice/<int:id>/',view=edit,name="edit invoice"),
    path('edit/customer/',view=edit_customer,name="edit customer"),
    path('edit/tax/',view=edit_tax,name="edit tax"),
    path('edit/item/<int:invoiceid>/<int:itemid>/',view=edit_item,name="edit item"),
    path('add/item/',view=add_item,name="add item"),
    path('send/<int:id>/',view=send_mail,name="send mail"),
    path('profile/', view=profile, name="profile"),
    path('',view=homepage,name='homepage'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)