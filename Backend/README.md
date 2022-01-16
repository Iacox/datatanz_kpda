# Backend part

# CryptAppBack

### Create image
```
docker build -t web-image ./Controller
```
### Project build
```
docker-compose up -d --build
docker exec web python manage.py collectstatic
```

### Project run
```
docker-compose up -d
```

### Run script
```
docker-compose exec web {script} 
```

### Swarm
```
docker swarm init --advertise-addr 127.0.0.1:2377
docker stack deploy -c docker-compose.yml
```  
### Remove swarm 
```
docker stack rm proj
docker swarm leave --force
```
### URL
```
REST API: localhost:90/api 
Flower: localhost:5555
```
#### Примечание
```
При переходе по ссылке на REST API слеоите за портом, он автоматически переходит на 80
```
