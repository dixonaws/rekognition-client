#!/bin/bash

# Create a new collection
aws rekognition create-collection --collection-id "dow-workshop-dixonaws"

aws rekognition index-faces \
      --image '{"S3Object":{"Bucket":"dixonaws-doorman","Name":"pics/eric_friedeberg_0.jpg"}}' \
      --collection-id "dow-workshop-dixonaws" \
      --detection-attributes "ALL" \
      --external-image-id "eric_friedeberg_0.jpg" 
    
