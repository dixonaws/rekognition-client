import boto3
import argparse
import time
import sys


def main():
	intStartTime = int(time.time())
	sys.stdout.write('Matching face... ')

	strRegion = 'us-east-1'

	rekognitionClient = boto3.client('rekognition', region_name=strRegion)

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

	print('Matches > 70%: ' + str(len(dictFaceMatches)))

	for match in dictFaceMatches:
		print('FaceId:' + match['Face']['FaceId'])
		print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")


# // main

main()
