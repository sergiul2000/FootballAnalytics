import json
import os
import requests
# import sys

CONFIG_PATH='credentials.cfg.py'
GENERIC_SEARCH_url='https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={termen}&searchType=image&imgSize=xlarge&alt=json&num=1&start=1'

IMAGE_OUTPUT_DIR='images'

def localConfig():
    with open(CONFIG_PATH) as cfg:
        return json.load(cfg)

def getUrl(cx,api_key,termen):
    url=GENERIC_SEARCH_url.format(
        cx=cx,
        api_key=api_key,
        termen=termen
    )
    print(url)
    return url

def saveImage(imageRaw,imagePath):
    with open(imagePath,'wb') as imageFile:
        imageFile.write(imageRaw)

def getImages(url):
    request = requests.get(url)
    if request.status_code == 200:
        content = json.loads(request.content)
        if content and 'items' in content:
            for item in content['items']:
                if item and 'link' in item:
                    imageUrl = item['link']
                    print(imageUrl)
                    imageRequest = requests.get(imageUrl)
                    if imageRequest.status_code == 200:
                        if imageRequest.content:
                            yield imageRequest.content
                    else:
                        print(imageRequest.status_code)

def main(terms):
    if len(terms) >0:
        if not os.path.isdir(IMAGE_OUTPUT_DIR):
            os.mkdir(IMAGE_OUTPUT_DIR)
        if os.path.isfile(CONFIG_PATH):
            config = localConfig()
            if config:
                origSearchTerm = terms[0]
                # searchTerm=terms[0]
                searchTerms=','.join(terms)
                for iterator in terms:
                    searchCounter = 0
                    url=getUrl(config['CX'],config['API_KEY'],iterator)
                    for imageRaw in getImages(url):
                        imagePath=os.path.join(
                            # IMAGE_OUTPUT_DIR,iterator+str(searchCounter)+'.jpg')
                            IMAGE_OUTPUT_DIR,iterator+'.jpg')
                        print(imagePath)
                        saveImage(imageRaw,imagePath)
                        searchCounter += 1
        else:
            print('bad configuration')
            return
        return

if __name__=='__main__':
    main(['car','messi','ronaldo'])