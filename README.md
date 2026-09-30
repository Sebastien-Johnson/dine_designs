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
- Docker

## Quick Start
- Clone the Repository
```
git clone https://github.com/Sebastien-Johnson/dine_designs
```
- [Get api key](https://fdc.nal.usda.gov/api-key-signup#top) and set "USDA_API_KEY" in env
- Build
```
docker-compose up --build
```
- Run migrations
```
docker exec -ti dd_postgres_db python manage.py makemigrations
docker exec -ti dd_postgres_db python manage.py migrate
```

- Create an admin account
```
python manage.py createsuperuser
```

- Access database shell
```
docker exec -ti dd_postgress_db psql -U {username} -d dev_database
```

## Usage
- View new posts on home feed
- Register or login to accounts 
- Publish, edit, comment and rate posts

## Contributing
- If you'd like to contribute, please fork, clone and test the repository before opening a pull request to the `main` branch.