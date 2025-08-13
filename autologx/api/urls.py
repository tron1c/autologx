# C:\Users\MY-PC\Desktop\unit 4\Autologx\autologx\api\urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Optional: Define an app_name for namespacing (good practice if you have multiple apps)
# app_name = 'api'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # User Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Vehicle Management
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),

    # Service Record Management (nested under vehicles)
    path('vehicles/<int:vehicle_pk>/service-records/create/', views.service_record_create, name='service_record_create'),

    # API Endpoints (AJAX)
    path('api/vin-lookup/', views.vin_lookup, name='vin_lookup'),
]
