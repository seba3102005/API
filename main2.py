import requests
from PIL import Image

url2 ="https://api.nasa.gov/planetary/apod?api_key=WTAsuPq5Lkw0F58wgOiZ9NG9UxejmRUfhOp3YeLg"
url ="https://api.thecatapi.com/v1/images/search?limit=10&breed_ids=beng&api_key=live_7OOoNwadKl2OS20H6U2hTpEaK5PgxdSclD8ngrJOzHMeRV3gFVfSTOtY0avnR87d"



response =requests.get(url)
response.raise_for_status()

data=response.json()


try:
    for image in data:
        print(image['id'])
        print(image['url'])
        print(image['width'])
        print(image['height'])
        image_response = requests.get(image['url'])
        image_response.raise_for_status()  # Check for request errors
        with open('photo.jpg', 'wb') as file:
            file.write(image_response.content)
        image = Image.open('photo.jpg')
        image.show()
    
except:
    print('error')