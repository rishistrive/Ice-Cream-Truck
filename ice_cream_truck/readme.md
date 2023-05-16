Project name :- Ice-Cream-Truck
Description:- In this project we have auth_app and food_app

1) first activate virtual env with command :- source myenv/bin/activate
2) install requirements.txt file :- pip install -r requirements.txt
3) run command :- python manage.py makemigrations 
4) run command :- python manage.py migrate

for running test case :- run command :- python manage.py test

for run server :- python manage.py runserver 

1) create a User registration by :-
URL ;- http://127.0.0.1:8000/auth/login/
data :-    {"username": "username1","password": "password1","email": "username1@mailinator.com","is_truck_owner": true}
method:- POST

2) create truck by:-
URL:- http://127.0.0.1:8000/api/trucks/
Data :- {"user":1}
method:-POST
also keep basic authentication with username and password otherwise we will be unable to create truck

3)create fooditem by:-
URL:- http://127.0.0.1:8000/food/fooditems/
Data:- {"truck":1,"name":"ice_cream","price":30,"flavors":"butter"}
method:-POST
also keep basic authentication with username and password otherwise we will be unable to create truck

4)create invetory by truch owner
URL:-http://127.0.0.1:8000/food/food-item-inventories/
data:- {"food_item":2,"amount_count":7,"truck_owner":1,"food_item": 2}
method :- POST
also keep basic authentication with username and password otherwise we will be unable to create truck

5) to BUY food 
URL:-http://127.0.0.1:8000/food/buy-food-items/
DATA:-{"food_item":1,"amount_count":1,"truck_owner":1}
method  ;- POST

6) TO see inventory :-
URL:-http://127.0.0.1:8000/food/food-item-inventories/
method:- GET


