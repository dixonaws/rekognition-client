### rekognition-client: A simple wrapper around the AWS Boto3/Rekognition Python API

installation:
* install the AWS CLI and configure credentials
* create a virtualenv with something like <code>virtualenv venv && source venv/bin/activate</code>
* install requirements with <code>pip install -r requirements.txt</code>
* create an AWS Rekognition Collection (https://docs.aws.amazon.com/rekognition/latest/dg/create-collection-procedure.html)
* compare a face to a rekognition collection: <code>python test-rekognition.py ["path_to_test_image"] ["rekognition_collection_id"]

