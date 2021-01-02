# Tradeplatform

## About project
Project imulates simple stock market or trade platform. Users can make offers to buy or sell a particular stock from other users. 
The program automatically creates a trade between two users at the best price.

## Description of the program
* #### Registration app
    Users can register on the platform and they has to confirm their email address to create offers. If user doesn't confirm his email address, he won't be able 
    to create offers. Also users can reset their password with the email confirmation, if they forgot their password. Besides, users can change their email address
    with email confirmation too. After registration users have their own profile with information about them, which they can change.
* #### Trades app
    Trades gives users the ability to perform trades. This app has script, which runs once a minute and finds suitable offers, then it makes trade between 
    the found offers. To make offers user has to sign up and confirm his email address. User can create offer with suitable currency for him. Each user has
    their own watchlist, that he can update. Each user has their own balance and inventory. Inventory stores information about the number of certain stocks 
    that the user owns.
    
## The technology used
* Django
* Django REST Framework
* Postgresql
* Celery
* Redis
* Docker
