# airflow-starter
Primary source of info came from [Airflow Documentation here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

## installing docker on Linux (redhat-)
  - sudo yum -y update         #updates all packages
  - sudo yum -y install docker #installs docker
  - type `docker` # returns docker options
  - command `docker --version` #version of docker installed
### install docker-compose on Linux (redhat)
  - `sudo curl -L "https://github.com/docker/compose/releases/download/v2.15.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
  
## get airflow docker image
```bash
mkdir airflow-docker
cd airflow-docker
curl -LfO 'http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/docker-compose.yaml'
```

## create necessary folders
```bash
mkdir ./dags ./plugins ./logs
```

## export env vars to ensure user and group perminssions are the same for the host folders and container folders.
```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

## Start or Stop Docker
```bash
# To start the airflow docker container, enter the docker directory and run.
docker-compose up

# to stop the server run
docker-compose down
```

One consideration before starting docker is what airflow version you want to use. A list of versions can be found on the [docker website](https://hub.docker.com/r/apache/airflow/tags). To define a sepecific version of airflow and python you'll need to update the `image` variable in the `docker-compose.yaml` file. 

```yaml
version: '3'
x-airflow-common:
  &airflow-common
  # In order to add custom dependencies or upgrade provider packages you can use your extended image.
  # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
  # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.5.1-python3.8}

# change the tag to whatever version you want.

  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.1.dev0}
```

## Installing Python packages on the container (e.g. Snowflake connector)
Add a sub-directory to the airflow docker directory called `packages`. In the new directory create a file called `requirements.txt` and alphabetically list the python packages you would like installed.

* https://medium.com/analytics-vidhya/how-to-connect-snowflake-with-airflow-on-docker-in-order-to-build-a-data-extraction-pipeline-for-e65591f011d6
* https://community.snowflake.com/s/article/How-to-connect-Apache-Airflow-to-Snowflake-and-schedule-queries-jobs

```bash
cd airflow-docker
mkdir packages
touch requirements.txt
```

The python packages should be listed in alphabetical order, only the package name is needed, each on a sperate line.
```bash
apache-airflow-providers-snowflake
snowflake-connector-python
snowflake-sqlalchemy
```

Next, add the newly created packages directory to the volumes section of the `docker-compose.yaml` file.
```yaml
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR:-.}/packages:/opt/airflow/packages
```

Now install the packages on each of the docker containers.
```bash
#look at all the container ids
docker ps

# enter the container
docker exec --user="airflow" -ti <container id> /bin/bask
cd packages && pip install -r requirements.txt
```

## Permission Denied Error on Container
This popped up once after rebooting the vm, `docker-compose` cannot bring down the container becuase of permission denied error
```bash
ERROR: for airflow-docker_airflow-worker_1  cannot stop container: a892836b5249689439df194e60582b5e324cad525ff03cd06d029373203ceb61: permission denied
```
The solution was to kill an apparmor profile.
```bash
sudo killall containerd-shim
sudo docker-compose down
```

## mounting network drives on linux
Network drives are widely used and are typically a dependency when moving data around teams and organizations.

[Redhat documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_file_systems/mounting-an-smb-share-on-red-hat-enterprise-linux_managing-file-systems#proc_manually-mounting-an-smb-share_assembly_mounting-an-smb-share-on-red-hat-enterprise-linux) explaining steps to mount smb drives.

Install the dependency that is a helper for connection to network shares.
```bash
sudo yum install cifs-utils 
```

Run this command with network username and path to network drive, you will be prompted for network password.
```bash
mount -t cifs -o username=user_name //server_name/share_name /mnt/
Password for user_name@//server_name/share_name:  password
```

This method will not persist if the machine is restarted.
