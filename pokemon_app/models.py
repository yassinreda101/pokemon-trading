from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

class PokemonType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Pokemon(models.Model):
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('legendary', 'Legendary'),
        ('mythical', 'Mythical'),
    ]

    name = models.CharField(max_length=100)
    pokedex_number = models.IntegerField(unique=True)
    types = models.ManyToManyField(PokemonType, related_name='pokemon')
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True)
    description = models.TextField(blank=True)

    # Stats
    hp = models.IntegerField(default=50)
    attack = models.IntegerField(default=50)
    defense = models.IntegerField(default=50)
    sp_attack = models.IntegerField(default=50)
    sp_defense = models.IntegerField(default=50)
    speed = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.name} (#{self.pokedex_number})"

    @property
    def total_stats(self):
        return self.hp + self.attack + self.defense + self.sp_attack + self.sp_defense + self.speed

    @classmethod
    def get_random_starter_pokemon(cls, count=5):
        """Return a set of random Pokemon for new users"""
        # Exclude legendary and mythical for starters
        common_pokemon = list(cls.objects.exclude(rarity__in=['legendary', 'mythical']))
        count = min(count, len(common_pokemon))  # Ensure we don't try to get more than what exists

        if common_pokemon:
            return random.sample(common_pokemon, count)
        return []

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    pokemon = models.ManyToManyField(Pokemon, through='PokemonCollection')
    coins = models.IntegerField(default=1000)  # Starting currency
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class PokemonCollection(models.Model):
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    date_acquired = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['trainer', 'pokemon', 'date_acquired']

    def __str__(self):
        if self.nickname:
            return f"{self.trainer.user.username}'s {self.nickname} ({self.pokemon.name})"
        return f"{self.trainer.user.username}'s {self.pokemon.name}"

class MarketplaceListing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ]

    seller = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='listings')
    pokemon = models.ForeignKey(PokemonCollection, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pokemon.pokemon.name} - {self.price} coins"

    def sell_to(self, buyer):
        """Process the sale of this Pokemon to a buyer"""
        if self.status != 'active':
            return False, "This listing is no longer active"

        if buyer.coins < self.price:
            return False, "Not enough coins to purchase"

        # Process the transaction
        buyer.coins -= self.price
        self.seller.coins += self.price

        # Transfer ownership
        new_collection = PokemonCollection.objects.create(
            trainer=buyer,
            pokemon=self.pokemon.pokemon,
            nickname=self.pokemon.nickname
        )

        # Update status and save changes
        self.status = 'sold'
        self.save()
        buyer.save()
        self.seller.save()

        # Remove from original trainer's collection
        self.pokemon.delete()

        return True, new_collection

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badge_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='achievements')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'badge')

    def __str__(self):
        return f"{self.trainer.user.username} earned {self.badge.name}"

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('system', 'System'),
    ]

    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField()  # Positive for gains, negative for expenses
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.amount} coins - {self.description[:30]}"