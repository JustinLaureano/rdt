# RDT Market Rebound

Project for r/RealDayTrading Market Rebound research.



## Building Containers

To build a container from the `docker-compose.yaml` file, run the following command:

```bash
docker-compose build <container_name>
```

You can also build without using the Docker cache:
```bash
docker-compose build --no-cache <container_name>
```

## Running Containers

You can start and run a container with the following command:

```bash
docker-compose up <container_name>
```

You can start multiple containers by entering all container names to start
```bash
docker-compose up <container_name1> <container_name2>
```

The `-d` flag will start and run the containers in the background
```bash
docker-compose up -d <container_name>
```

To build and run a container with one command, run the following:
```bash
docker-compose up --build <container_name>
```

To view running containers, run:
```bash
docker ps
```

## Entering Containers

Once a container is running, you can enter the terminal of the container with the following command:
```bash
docker exec -it <container_name> bash
```

You can also enter a running container as non-default user:
```bash
docker exec -it --user <username> <container_name> bash
```

To leave a running container, run `exit` from the terminal.

## Stopping Containers

To stop a container from running, enter the following command:
```bash
docker-compose stop <container_name>
```

To gracefully shut down all server containers running, run the following:
```bash
docker-compose down
```

## Removing Containers

To remove a container from your local machine, run the following:
```bash
docker container rm <container_name>
```

## Removing Images

If you need to remove the image that the container runs from, run the following:
```bash
docker image rm servers_<container_name>
```

## Removing Volumes

If you need to remove a volume for a container, run the following:
```bash
docker volume rm servers_<container_name>
```

## Environment Variables

The `.env` file allows you to set custom veriables that are unique to your own development environment. This includes ports that Docker will map to your local machine, as well as default users and passwords for databases.

## Database Entrypoint Init Setup

The files located inside the `docker-entrypoint-initdb.d` directory for any of the database setup folders will be run one time when the container is created and started for the first time. This makes a good place to run schema init commands, create users and give permissions, or run any seeder data that may be needed.

If you want to rerun the files in this directory, you will need to remove the container, image, and volume from your local machine, then rebuild and start the container. A command to do this may look something like this:
```bash
docker container rm <container_name> && docker image rm servers_<container_name> && docker volume rm servers_<container_name> && docker-compose build --no-cache <container_name> && docker-compose up -d <container_name>
```
