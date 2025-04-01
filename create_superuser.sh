#!/bin/bash

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('adminMahmoud', 'admin@example.com', 'password_Mahmoud_123') if not User.objects.filter(username='adminMahmoud').exists() else print('Superuser already exists')" | python manage.py shell
