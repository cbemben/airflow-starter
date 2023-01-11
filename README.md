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
