docker compose down
docker system prune -f
docker compose build --no-cache
docker compose up