# airflow-starter

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

## Installing Python packages on the container (e.g. Snowflake connector)
Add a sub-directory to the airflow docker directory called `packages`. In the new directory create a file called `requirements.txt` and alphabetically list the python packages you would like installed.
```bash
cd airflow-docker
mkdir packages
touch requirements.txt
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
