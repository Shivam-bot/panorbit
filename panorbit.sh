#!/usr/bin/env bash

pip install  virtualenv

python3 -m venv venv

source venv/bin/activate

cd panorbitproject

pip install -r req.txt

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver
