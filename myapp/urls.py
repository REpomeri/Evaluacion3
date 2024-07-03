from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('update/<int:id>/', views.update_document, name='update_document'),
    path('delete/<int:id>/', views.delete_document, name='delete_document'),
    path('compra/', views.compra_view, name='compra_view'),
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('guest-login/', views.guest_login, name='guest_login'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('confirmar_compra/', views.confirmar_compra, name='confirmar_compra'),
    path('historial_compras/', views.historial_compras, name='historial_compras'),
]