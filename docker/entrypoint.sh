#!/bin/sh

echo "🛠  Making migrations..."
python manage.py makemigrations --noinput

echo "🚀 Applying migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser if not exists..."
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

# Simulate conversations
echo "🤖 Simulating GPT-to-GPT conversations..."
python manage.py simulate_conversations

echo "✅ Starting server..."
python manage.py runserver 0.0.0.0:8000
