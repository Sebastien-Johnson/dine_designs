# dine_designs
Recipe sharing web app that allows for CRUD operations, commenting and rating

## Motivation
- Having a large family of cooks with few handing down their secrets is a recipe for disaster
- Collecting the tastes of home they've been clutching for far too long
- Building an app that feels good to users across a broad age range

## Features
- User Authentication: Secure registration and login functionality
- Users: Create and edit profiles and accounts
- CRUD Operations: Create, read, update, and delete blog posts
- Admin Dashboard: Manage users and content with Django's admin interface
- Commenting System: Engage readers through comments on posts
- Rating system: Rate other's recipes


## Prerequisites
- [Python 3.14+](https://www.python.org/downloads/)
- [Pip package manager](https://pip.pypa.io/en/stable/installation/)

## Quick Start
- Clone the Repository
```
git clone https://github.com/Sebastien-Johnson/dine_designs
```
- Setup version control
```
python -m venv /path/to/new/virtual/environment
```
- Install dependencies
```
pip install -r /path/to/requirements.txt
```
- [Get api key](https://fdc.nal.usda.gov/api-key-signup#top) and add to 'config.yaml' file
```
usda_api_key: api_key
```
- Enter 'dj_blog' directory and run migrations
```
cd dj_blog
python manage.py makemigrations
python manage.py migrate
```
- Create an admin
```
python manage.py createsuperuser
```
- Runserver
```
python manage.py runserver
```


## Usage
- View new posts on home feed
- Register or login to accounts 
- Publish, edit, comment and rate posts
- Access admin panel: http://localhost:8000/admin/

## Future updates
- Pull nutrition facts automatically as you add to your recipe
- Post category tags
- Searching and filtering
- Comment replies
- Editing ratings

## Contributing
- If you'd like to contribute, please fork, clone and test the repository before opening a pull request to the `main` branch.