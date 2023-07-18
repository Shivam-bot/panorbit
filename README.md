# panorbit

Step for setup:-
1. Clone the repository.
2. Configure db connection in setting.py file
3. For email set your email and password. AS of now I've added the testing one.


For Linux user:-
Run these commands :- 
sudo chmod 774 panorbit.sh
./panorbit.sh
Now you are ready to use



For Window user:-
    pip install  virtualenv
    py -m venv venv
    venv/Scripts/activate
    cd panorbitproject
    pip install -r req.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    Now you are ready to use


After server start successfully
dump world.sql file in your db so that you get all the required data of country for testing purpose

