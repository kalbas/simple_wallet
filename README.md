docker-compose up -d db
docker-compose up app
docker-compose exec app pytest