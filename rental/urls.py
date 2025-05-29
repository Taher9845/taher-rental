from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.property_list,name='property_list'),
    path('property/<int:pk>/',views.property_detail,name='property_detail'),
    path('property/add/', views.add_property, name='add_property'),
    path('property/<int:pk>/apply/', views.apply_for_property, name='apply_for_property'),
    path('applications/', views.application_status, name='application_status'),
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tenant/applications/', views.tenant_applications, name='tenant_applications'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
