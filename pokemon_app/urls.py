from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='pokemon_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Profile and Pokemon management
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-pokemon/', views.my_pokemon, name='my_pokemon'),

    # Pokemon information
    path('pokemon/', views.pokemon_list, name='pokemon_list'),
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),

    # Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/create/', views.create_listing, name='create_listing'),
    path('marketplace/buy/<int:listing_id>/', views.buy_pokemon, name='buy_pokemon'),

    # Achievements
    path('achievements/', views.achievements, name='achievements'),
]