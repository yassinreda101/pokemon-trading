from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

from .models import (
    Pokemon, PokemonType, TrainerProfile, PokemonCollection,
    MarketplaceListing, Badge, Achievement, Transaction
)
from .forms import (
    TrainerSignUpForm, PokemonSearchForm, ListPokemonForm, ProfileUpdateForm
)

def home(request):
    # Count of available Pokemon in the database
    total_pokemon = Pokemon.objects.count()
    # Get a random sample of Pokemon to feature
    featured_pokemon = Pokemon.objects.order_by('?')[:6]

    # Get recently listed marketplace items
    recent_listings = MarketplaceListing.objects.filter(status='active').order_by('-listed_at')[:5]

    context = {
        'total_pokemon': total_pokemon,
        'featured_pokemon': featured_pokemon,
        'recent_listings': recent_listings,
    }

    return render(request, 'pokemon_app/home.html', context)

def signup(request):
    if request.method == 'POST':
        form = TrainerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome to your Pokémon journey!')
            return redirect('profile')
    else:
        form = TrainerSignUpForm()

    return render(request, 'pokemon_app/signup.html', {'form': form})

@login_required
def profile(request):
    trainer = get_object_or_404(TrainerProfile, user=request.user)
    pokemon_collection = PokemonCollection.objects.filter(trainer=trainer)
    achievements = Achievement.objects.filter(trainer=trainer)
    active_listings = MarketplaceListing.objects.filter(seller=trainer, status='active')

    # Calculate collection stats
    total_pokemon = pokemon_collection.count()
    pokemon_types = {}
    rarities = {}

    for item in pokemon_collection:
        for type_obj in item.pokemon.types.all():
            pokemon_types[type_obj.name] = pokemon_types.get(type_obj.name, 0) + 1

        rarities[item.pokemon.rarity] = rarities.get(item.pokemon.rarity, 0) + 1

    context = {
        'trainer': trainer,
        'pokemon_collection': pokemon_collection,
        'achievements': achievements,
        'active_listings': active_listings,
        'total_pokemon': total_pokemon,
        'pokemon_types': pokemon_types,
        'rarities': rarities,
    }

    return render(request, 'pokemon_app/profile.html', context)

@login_required
def edit_profile(request):
    trainer = get_object_or_404(TrainerProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=trainer)

    return render(request, 'pokemon_app/edit_profile.html', {'form': form})

def pokemon_list(request):
    # Get all Pokemon
    pokemon = Pokemon.objects.all()

    # Handle search and filtering
    form = PokemonSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        pokemon_type = form.cleaned_data.get('pokemon_type')
        rarity = form.cleaned_data.get('rarity')

        if query:
            pokemon = pokemon.filter(name__icontains=query)

        if pokemon_type:
            pokemon = pokemon.filter(types=pokemon_type)

        if rarity:
            pokemon = pokemon.filter(rarity=rarity)

    context = {
        'pokemon': pokemon,
        'form': form,
        'total_count': Pokemon.objects.count(),
        'filtered_count': pokemon.count(),
    }

    return render(request, 'pokemon_app/pokemon_list.html', context)

def pokemon_detail(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

    # Get active marketplace listings for this Pokemon
    listings = MarketplaceListing.objects.filter(
        pokemon__pokemon=pokemon,
        status='active'
    ).order_by('price')

    context = {
        'pokemon': pokemon,
        'listings': listings,
    }

    return render(request, 'pokemon_app/pokemon_detail.html', context)

@login_required
def my_pokemon(request):
    trainer = get_object_or_404(TrainerProfile, user=request.user)
    collection = PokemonCollection.objects.filter(trainer=trainer)

    # Handle search and filtering
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    rarity_filter = request.GET.get('rarity', '')

    if search_query:
        collection = collection.filter(
            Q(pokemon__name__icontains=search_query) |
            Q(nickname__icontains=search_query)
        )

    if type_filter:
        collection = collection.filter(pokemon__types__name=type_filter)

    if rarity_filter:
        collection = collection.filter(pokemon__rarity=rarity_filter)

    # Get all types and rarities for filter options
    all_types = PokemonType.objects.all()
    all_rarities = [choice[0] for choice in Pokemon.RARITY_CHOICES]

    context = {
        'collection': collection,
        'search_query': search_query,
        'type_filter': type_filter,
        'rarity_filter': rarity_filter,
        'all_types': all_types,
        'all_rarities': all_rarities,
    }

    return render(request, 'pokemon_app/my_pokemon.html', context)

@login_required
def marketplace(request):
    # Get all active listings
    listings = MarketplaceListing.objects.filter(status='active').order_by('-listed_at')

    # Handle search and filtering
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    rarity_filter = request.GET.get('rarity', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search_query:
        listings = listings.filter(
            Q(pokemon__pokemon__name__icontains=search_query) |
            Q(pokemon__nickname__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if type_filter:
        listings = listings.filter(pokemon__pokemon__types__name=type_filter)

    if rarity_filter:
        listings = listings.filter(pokemon__pokemon__rarity=rarity_filter)

    if min_price:
        listings = listings.filter(price__gte=min_price)

    if max_price:
        listings = listings.filter(price__lte=max_price)

    # Get all types and rarities for filter options
    all_types = PokemonType.objects.all()
    all_rarities = [choice[0] for choice in Pokemon.RARITY_CHOICES]

    context = {
        'listings': listings,
        'search_query': search_query,
        'type_filter': type_filter,
        'rarity_filter': rarity_filter,
        'min_price': min_price,
        'max_price': max_price,
        'all_types': all_types,
        'all_rarities': all_rarities,
    }

    return render(request, 'pokemon_app/marketplace.html', context)

@login_required
def create_listing(request):
    trainer = get_object_or_404(TrainerProfile, user=request.user)

    if request.method == 'POST':
        form = ListPokemonForm(trainer, request.POST)
        if form.is_valid():
            listing = form.save()
            messages.success(request, f'Your {listing.pokemon.pokemon.name} has been listed!')
            return redirect('marketplace')
    else:
        form = ListPokemonForm(trainer)

    return render(request, 'pokemon_app/create_listing.html', {'form': form})

@login_required
def buy_pokemon(request, listing_id):
    listing = get_object_or_404(MarketplaceListing, pk=listing_id, status='active')
    buyer = get_object_or_404(TrainerProfile, user=request.user)

    # Prevent buying your own Pokemon
    if listing.seller == buyer:
        messages.error(request, "You cannot buy your own Pokemon!")
        return redirect('marketplace')

    # Process the transaction
    success, result = listing.sell_to(buyer)

    if success:
        # Record the transaction
        Transaction.objects.create(
            trainer=buyer,
            amount=-listing.price,
            transaction_type='purchase',
            description=f"Purchased {result.pokemon.name} from {listing.seller.user.username}"
        )

        Transaction.objects.create(
            trainer=listing.seller,
            amount=listing.price,
            transaction_type='sale',
            description=f"Sold {result.pokemon.name} to {buyer.user.username}"
        )

        messages.success(request, f"You've successfully purchased {result.pokemon.name}!")

        # Check for achievements
        check_for_achievements(buyer)

        return redirect('my_pokemon')
    else:
        messages.error(request, result)  # Show error message
        return redirect('marketplace')

@login_required
def achievements(request):
    trainer = get_object_or_404(TrainerProfile, user=request.user)
    earned_achievements = Achievement.objects.filter(trainer=trainer).order_by('-earned_at')
    all_badges = Badge.objects.all()

    # Calculate which badges haven't been earned yet
    earned_badge_ids = earned_achievements.values_list('badge_id', flat=True)
    unearned_badges = Badge.objects.exclude(id__in=earned_badge_ids)

    context = {
        'earned_achievements': earned_achievements,
        'unearned_badges': unearned_badges,
    }

    return render(request, 'pokemon_app/achievements.html', context)

# Helper function to check for achievements
def check_for_achievements(trainer):
    """Check if trainer has earned any new achievements"""
    # Get all collection data
    collection = PokemonCollection.objects.filter(trainer=trainer)
    collection_count = collection.count()

    # Get all existing achievements
    existing_achievements = Achievement.objects.filter(trainer=trainer).values_list('badge_id', flat=True)

    # Check for collection size achievements
    collection_badges = {
        5: Badge.objects.get_or_create(name="Novice Collector", description="Collect 5 Pokemon")[0],
        10: Badge.objects.get_or_create(name="Intermediate Collector", description="Collect 10 Pokemon")[0],
        25: Badge.objects.get_or_create(name="Advanced Collector", description="Collect 25 Pokemon")[0],
        50: Badge.objects.get_or_create(name="Expert Collector", description="Collect 50 Pokemon")[0],
        100: Badge.objects.get_or_create(name="Master Collector", description="Collect 100 Pokemon")[0],
    }

    for count, badge in collection_badges.items():
        if collection_count >= count and badge.id not in existing_achievements:
            Achievement.objects.create(trainer=trainer, badge=badge)

    # Check for type-based achievements
    type_counts = {}
    for item in collection:
        for type_obj in item.pokemon.types.all():
            type_counts[type_obj.name] = type_counts.get(type_obj.name, 0) + 1

    for type_name, count in type_counts.items():
        if count >= 5:
            badge_name = f"{type_name} Specialist"
            badge = Badge.objects.get_or_create(
                name=badge_name,
                description=f"Collect 5 {type_name}-type Pokemon"
            )[0]

            if badge.id not in existing_achievements:
                Achievement.objects.create(trainer=trainer, badge=badge)

    # Check for rarity-based achievements
    rarity_counts = {}
    for item in collection:
        rarity_counts[item.pokemon.rarity] = rarity_counts.get(item.pokemon.rarity, 0) + 1

    rarity_badges = {
        'rare': (3, "Rare Hunter", "Collect 3 rare Pokemon"),
        'legendary': (1, "Legend Catcher", "Collect a legendary Pokemon"),
        'mythical': (1, "Myth Seeker", "Collect a mythical Pokemon"),
    }

    for rarity, (min_count, badge_name, description) in rarity_badges.items():
        if rarity_counts.get(rarity, 0) >= min_count:
            badge = Badge.objects.get_or_create(name=badge_name, description=description)[0]

            if badge.id not in existing_achievements:
                Achievement.objects.create(trainer=trainer, badge=badge)

    # Trading achievements
    sales_count = Transaction.objects.filter(trainer=trainer, transaction_type='sale').count()
    purchase_count = Transaction.objects.filter(trainer=trainer, transaction_type='purchase').count()

    if sales_count >= 1:
        badge = Badge.objects.get_or_create(name="First Sale", description="Complete your first Pokemon sale")[0]
        if badge.id not in existing_achievements:
            Achievement.objects.create(trainer=trainer, badge=badge)

    if purchase_count >= 1:
        badge = Badge.objects.get_or_create(name="First Purchase", description="Buy your first Pokemon from marketplace")[0]
        if badge.id not in existing_achievements:
            Achievement.objects.create(trainer=trainer, badge=badge)