from django.contrib import admin
from .models import (
    Pokemon, PokemonType, TrainerProfile, PokemonCollection,
    MarketplaceListing, Badge, Achievement, Transaction
)

@admin.register(PokemonType)
class PokemonTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('name', 'pokedex_number', 'rarity', 'total_stats')
    list_filter = ('rarity', 'types')
    search_fields = ('name', 'pokedex_number')
    filter_horizontal = ('types',)

@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'coins', 'created_at')
    search_fields = ('user__username', 'display_name')

@admin.register(PokemonCollection)
class PokemonCollectionAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'pokemon', 'nickname', 'date_acquired')
    list_filter = ('trainer', 'date_acquired')
    search_fields = ('trainer__user__username', 'pokemon__name', 'nickname')

@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'seller', 'price', 'status', 'listed_at')
    list_filter = ('status', 'listed_at')
    search_fields = ('pokemon__pokemon__name', 'seller__user__username')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'badge', 'earned_at')
    list_filter = ('badge', 'earned_at')
    search_fields = ('trainer__user__username', 'badge__name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'amount', 'transaction_type', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('trainer__user__username', 'description')