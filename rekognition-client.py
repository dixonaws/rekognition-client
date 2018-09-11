import boto3
import argparse
import time
import sys
from boto3.dynamodb.conditions import Key, Attr

def main():
    intStartTime = int(time.time())
    sys.stdout.write('Matching face... ')

    strRegion = 'us-east-1'

    rekognitionClient = boto3.client('rekognition', region_name=strRegion)
    dynamodb = boto3.resource('dynamodb', region_name=strRegion)

    parser = argparse.ArgumentParser(description='Compare a given face with a given collection')
    parser.add_argument('FaceToCompare',
                        help='Input face to compare against the collection, must be a jpeg or png file')
    parser.add_argument('CollectionId', help='Existing Rekognition collectionId')

    args = parser.parse_args()

    strFaceToCompare = args.FaceToCompare
    strCollectionId = args.CollectionId

    with open(strFaceToCompare, 'rb') as image:
        response = rekognitionClient.search_faces_by_image(CollectionId=strCollectionId,
                                                           Image={'Bytes': image.read()},
                                                           FaceMatchThreshold=70,
                                                           MaxFaces=1)

    intEndTime = int(time.time())

    print('done (' + str(intEndTime - intStartTime) + 'ms)')
    dictFaceMatches = response['FaceMatches']

    print()

    intNumberOfMatches = len(dictFaceMatches)
    print('Matches > 70%: ' + str(intNumberOfMatches))

    if (intNumberOfMatches == 0):
        #  call Phaedra
        snsClient = boto3.client('sns')
        print('Unidentified guest!')

        # text eric
        response = snsClient.publish(
            PhoneNumber='+19893274105',
            Message='An unidentified guest is at the CDMC front entrance!',
            Subject='Unidentified guest!'
        )

        # text phaedra
        response = snsClient.publish(
            PhoneNumber='+18478044119',
            Message='An unidentified guest is at the CDMC front entrance!',
            Subject='Unidentified guest!'
        )



    else:
        # positive ID on face
        # print each matchng face with their faceid
        strFaceId=''

        table = dynamodb.Table('cdmc-users')

        for match in dictFaceMatches:
            strFaceId = match['Face']['FaceId']
            print('FaceId:' + strFaceId)
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")

            response = table.query(KeyConditionExpression=Key('FaceId').eq(strFaceId))

            # todo: this will need to be adjusted
            print(response['Items'][0]['name'])


# // main

main()
