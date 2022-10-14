# Systems Integration Development Kit #
## Basic instructions ##

This work environment allows you to easily install the development dependencies needed for your Integrated Systems project.

### How to I setup my development environment? ###

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Run the following command (in the root folder of this project) to install the development environment:
```
docker-compose up --build -d
```
* Once your are done working in this project, you can remove everything by running:
```
docker-compose down
```
* **NOTE:** once you run the command above, the data in the database will be reset. Consider just stoping the container if you want to keep the data.

### Available Resources ###


#### PostgreSQL Database ####

* Available at localhost:5432
  * user: is
  * password: is
  * database: is

#### Python Dev Environment ####

* Python 3.9.15
* You can add pre-installed packages to the **requirements.txt** file
* You can easily use this python environment by opening up a terminal with the following command
```
# (linux/mac users)
docker exec -it is-dev /bin/bash

# (windows users)
docker exec -it is-dev powershell
```
* You can, for instance, try the database access script in the new shell
```
python db-access/main.py
```