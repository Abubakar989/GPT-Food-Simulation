#!/bin/sh

echo "🛠 Applying database migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password="${DJANGO_SUPERUSER_PASSWORD}")
    print("✅ Superuser created.")
else:
    print("ℹ️  Superuser already exists.")
EOF

echo "🤖 Simulating GPT-to-GPT conversations..."
python manage.py simulate_conversations

echo "🚀 Starting Gunicorn server..."
exec gunicorn gpt_food_simulator.wsgi:application --bind 0.0.0.0:8000
