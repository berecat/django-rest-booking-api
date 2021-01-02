# Tradeplatform

## About project
Project imulates simple stock market or trade platform. Users can make offers to buy or sell a particular stock from other users. 
The program automatically creates a trade between two users at the best price.

## Description of the project
* #### Registration app
    Users can register on the platform and they has to confirm their email address to create offers. If user doesn't confirm his email address, he won't be able 
    to create offers. Also users can reset their password with the email confirmation, if they forgot their password. Besides, users can change their email address
    with email confirmation too. After registration users have their own profile with information about them, which they can change.
* #### Trades app
    Trades gives users the ability to perform trades. This app has script, which runs once a minute and finds suitable offers, then it makes trade between 
    the found offers. To make offers user has to sign up and confirm his email address. User can create offer with suitable currency for him. Each user has
    their own watchlist, that he can update. Each user has their own balance and inventory. Inventory stores information about the number of certain stocks 
    that the user owns.
    
## Functionality of the project
* List all currencies, get detail information about currency
* List all items, get detail information about item
* List all watchlists, get detail watchlist and update only watchlist, which belongs to requested user
* List all prices of items, get detail information about price
* List all offers, create new offer, get detail information about offer, update offer, delete offer, which belongs to requested user
* List all balances, get detail information about balance
* List all inventories, get detail information about inventory
* List all trades, get detail information about trade
* List all users, get detail information about user
* List all user's profiles, get detail information about user's profile, update user's profile, which belongs to requested user
* Sign up to API
* Email confirmation
* Reset user's password
* Change user's email address
* Script, which runs once a minute and find suitable offers to create trade between them
* Users, that didn't confirm they email address, can't create offers
* User has to sign up to API or they have just read-only ability
* Admin can post new currencies and items
* User can search, filter the given result or choose ordering field to order result by it
* All users has their own balance, watchlist and profile after registration
    
## The technology used
* Django
* Django REST Framework
* Postgresql
* Celery
* Redis
* Docker
