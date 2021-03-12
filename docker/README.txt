0. Get Postgres container
> docker pull postgres

1. Edit the script
> change location of {docker} directory

2. Launch the container (with script file)
> ./run_docker_postgres

3. Enter in container
> docker exec -it docker-postgres bash

4. Enter in Postgres
> psql -U postgres

5. Create YAGO database
> create database yago;

6. Exit container and connect locally
> psql -h 127.0.0.1 -U postgres

---

A. YAGO Importer
> psql -a -d yago -h 127.0.0.1 -U postgres -f postgres.sql

---

DOCKER POSTGRES PASSWORD : password
DOCKER CONTAINER NAME : docker-postgres

Link TSV File : http://resources.mpi-inf.mpg.de/yago-naga/yago3.1/yagoTransitiveType.tsv.7z
