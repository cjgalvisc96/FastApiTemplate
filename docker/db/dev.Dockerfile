FROM mysql/mysql-server:5.7

COPY ./docker/db/init_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh
