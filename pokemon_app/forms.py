from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TrainerProfile, MarketplaceListing, PokemonCollection, Pokemon

class TrainerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=50, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create the trainer profile
            profile = TrainerProfile.objects.create(
                user=user,
                display_name=self.cleaned_data.get('display_name', ''),
                bio=self.cleaned_data.get('bio', '')
            )

            # Assign random starter Pokemon
            from .models import Pokemon
            starter_pokemon = Pokemon.get_random_starter_pokemon()
            for pokemon in starter_pokemon:
                PokemonCollection.objects.create(
                    trainer=profile,
                    pokemon=pokemon
                )

        return user

class PokemonSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search by name')
    pokemon_type = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Filter by type',
        empty_label='All Types'
    )
    rarity = forms.ChoiceField(
        choices=[('', 'All Rarities')] + list(Pokemon.RARITY_CHOICES),
        required=False,
        label='Filter by rarity'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import PokemonType
        self.fields['pokemon_type'].queryset = PokemonType.objects.all()

class ListPokemonForm(forms.ModelForm):
    pokemon = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = MarketplaceListing
        fields = ['pokemon', 'price', 'description']

    def __init__(self, trainer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trainer = trainer
        self.fields['pokemon'].queryset = PokemonCollection.objects.filter(
            trainer=self.trainer
        )

    def save(self, commit=True):
        listing = super().save(commit=False)
        listing.seller = self.trainer

        if commit:
            listing.save()

        return listing

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['display_name', 'bio']