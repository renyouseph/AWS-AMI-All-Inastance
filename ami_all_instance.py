import boto3
import datetime

Region = 'us-east-1'


##### Retention in count ######
Retention = 2                 #
###############################
#
#This scipt takes AMI of all instances in the region configured in AWS-CLI
#This will take AMI of all running and stopped instances with tag 'backup' and 'yes'
#
##### Server Requirements ####################
# Python    # apt-get install python3
# apt-get install libssl-dev -y
# Pip     - # apt-get install -y python3-pip
# AWS CLI - # pip3 install awscli , # aws configure
# Boto3   - # pip install boto3
##############################################
#
# Written by Reny Ouseph
# renyouseph@gmail.com +91 9072997607
#
##############################################

ec2Client = boto3.client('ec2',region_name=Region)
ec2Resource = boto3.resource('ec2',region_name=Region)

curDate = datetime.datetime.now().strftime("%d/%m/%Y")

Filter = [ {'Name':'tag:backup' , 'Values':['yes']} ]

imageCounter = {}
images = ec2Resource.images.filter(Owners=['self'])

for image in images.all():
    imageInstanceName,imageCreationDate = image.name.split('-')
    if imageInstanceName not in imageCounter:
        imageCounter[imageInstanceName] = []
        imageCounter[imageInstanceName].append((imageCreationDate,image.id))
    else:
        imageCounter[imageInstanceName].append((imageCreationDate,image.id))
        

def getImageDate(tup):
    return datetime.datetime.strptime(tup[0],'%d/%m/%Y')


####### Delete old images if retention meets or exceeded #######

def deleteOldImages(instanceName):
    FetchFromDate = (Retention-1) * -1
    sortedList = sorted(imageCounter[instanceName],key=getImageDate)
    for amiDate,amiId in sortedList[:FetchFromDate]:
        ec2Client.deregister_image(ImageId=amiId,DryRun=False)
        print('Deleting Image : {}'.format(amiId))

####### Retention check ###########

for instance in ec2Resource.instances.filter(Filters=Filter):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            instanceName = tag['Value']
            instanceId = instance.id
            amiCount = len(imageCounter.get(instanceName,[]))
            if amiCount >= Retention:
                deleteOldImages(instanceName)
            imageInfo = ec2Client.create_image(InstanceId=instanceId,Name='{}-{}'.format(instanceName,curDate),NoReboot=True,DryRun=False)
            print('Creating Image : {}'.format(imageInfo['ImageId']))
