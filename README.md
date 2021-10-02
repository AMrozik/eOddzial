# eOddzial
Web application created to make easier managing of space and time in hospital ward

## For developers

### Installation
to run application you need to first install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)

django web application and postgreSQL database are running in different containers that communicates with each other. To start them both:

```bash
docker-compose up --build
```

**NOTE:** on linux-based systems docker and docker-compose are by default installed with root permissions so you need to add _sudo_ to all the commads that utilises them.
If you feel really bad with that you can try [this](https://docs.docker.com/engine/install/linux-postinstall/) to change those permissions. But i have never mess with that so can't help if any issues occur

You don't need to install django explicitly by yourself to run and test application but if you use Pycharm it may be more convenient to install django to have syntax highlight and proper hints in IDE.
However I strongly recommend to install django in seperate [virtual environment](https://docs.python.org/3/tutorial/venv.html)

### !!! CAUTION !!!
**!!! please describe every commit you make clearly and tell what you have changed. Make new branches when working with new functionalities and [_create pull request_](https://github.com/AMrozik/eOddzial/pulls) when finished and functionality works properly !!!**

It will help the others in team to reviev code and revert changes if something go wrong


### Connecting to the PSQL server via CLI:

it might be helpful to manage database on development stage

1. Find the _docker-container-id_ in which the postgres is running using the below command.
```bash
docker ps -a
```
2. Run the below command to enter into the container (with the ID from step-1).
```bash
docker exec -it <PSQL-Container-ID> bash
```
3. Authenticate to start using as postgres user.
```bash
psql -h localhost -p 5432 -U postgres -W
```
4. Enter the password used while creating the PSQL server container. (inside docker-compose.yaml)
