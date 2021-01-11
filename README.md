# Docker
# Create volume for database postgressql
1. Создаем место на диске, где будет храниться база данных. Это место находиться в системных файлах
docker volume create --name vol_1
2. Проверяем созданный объем
docker volume ls
3. Запускаем контейнер
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5400:5432 -v vol_1:/var/lib/postgresql/data postgres:latest
4. Проверяем существующий контейнер
docker container ls
5. Останавить контейнер
docker container stop pg-docker
6. Сделать копию базы данных. 
docker run --rm -v vol_1:/volume -v /home/serg/projects/mentor:/backup alpine tar -cjf /backup/db.tar.bz2 -C /volume ./
7. Восстановить данные
`docker run --rm -v vol_1:/volume -v /tmp:/backup alpine sh -c "rm -rf /volume/* /volume/..?* /volume/.[!.]* ; tar -C /volume/ -xjf /backup/db.tar.bz2"`

# PG Admin
Host name: 0.0.0.0
Port: 5400
Database: postgres
Username: postgres
Password: docker

# Create tables
python create_tables.py


