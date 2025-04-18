# Pokémon Trading Platform

**CS 2340: Objects and Design**  
**Georgia Tech - Spring 2025**

## Project Description

This Pokémon Trading Platform is a web application that allows trainers to collect, trade, and sell Pokémon. Built with Django, the platform features user authentication, a marketplace system, direct trading between users, and an achievements tracking system.

## Features

### Implemented Features

1. **User Authentication**
   - Sign up and login to manage Pokémon collections securely
   - User profiles with customizable display names and bios

2. **Pokémon Collection**
   - Receive random starter Pokémon upon registration
   - View detailed Pokémon stats and information
   - Search and filter Pokémon by name, type, and rarity

3. **Marketplace**
   - List Pokémon for sale with custom prices
   - Browse and purchase Pokémon from other trainers
   - Transaction history tracking

4. **Trading System**
   - Propose direct trades with other trainers
   - Review and accept/reject incoming trade offers
   - Trade multiple Pokémon in a single transaction

5. **Achievements**
   - Earn badges based on collection milestones
   - Track progress through the trainer profile
   - Special achievements for marketplace and trading activity

6. **Admin Dashboard**
   - Monitor trading activity
   - Manage user accounts
   - View marketplace and transaction data

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: Django Authentication System

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/pokemon-trading.git
   cd pokemon-trading

Install dependencies:
bashpip install django pillow django-crispy-forms django-allauth crispy-bootstrap4

Run migrations:
bashpython manage.py migrate

Load initial Pokémon data:
bashpython manage.py loaddata pokemon_app/fixtures/initial_data.json

Create a superuser (admin):
bashpython manage.py createsuperuser

Start the development server:
bashpython manage.py runserver

Visit the application at http://127.0.0.1:8000/

Team Members

Yassin Reda
Mehtab Nasir
Araav Yadav
Joshua Kim

pokemon_trading/
├── pokemon_trading/         # Project settings folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pokemon_app/             # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Forms for user input
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin site configuration
│   ├── templates/           # HTML templates
│   ├── static/              # Static assets (CSS, JS)
│   └── fixtures/            # Initial data
├── media/                   # User-uploaded media
└── manage.py                # Django management script

Course Context
This project was developed for CS 2340: Objects and Design at Georgia Tech. The focus was on applying object-oriented design principles, implementing user stories, and developing a web application with proper separation of concerns.
Future Enhancements

AI-based trade recommendations
Pokémon battle system
Custom Pokémon image generation
Real-time chat system for negotiating trades


© 2025 Georgia Tech CS 2340 Team
