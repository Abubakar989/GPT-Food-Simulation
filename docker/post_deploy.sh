#!/bin/bash

echo " Applying Django database migrations..."
docker compose -f docker-compose-prod.yml exec web python manage.py migrate --noinput

echo " Collecting static files..."
docker compose -f docker-compose-prod.yml exec web python manage.py collectstatic --noinput


echo " Running conversation simulation..."
docker compose -f docker-compose-prod.yml exec web python manage.py simulate_conversations

echo " Post-deployment tasks completed!"
