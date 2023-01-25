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
