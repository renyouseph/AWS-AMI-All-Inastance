# AWS-AMI-All-Inastance

This script will take the AMI of all running and stopped instance in the specified region with instance tag 'backup' and removed the previously taken AMI's as per the retention has set.

## Server Requirements:
* Python    # apt-get install python3
* OpenSSL   # apt-get install libssl-dev -y
* Pip       # apt-get install -y python3-pip
* AWS CLI   # pip3 install awscli  # aws configure
* Boto3     # pip install boto3

### Configuration:

* Set your Region in 'Region'
* Set the Retetion required.

