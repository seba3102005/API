import requests
from PIL import Image
from io import BytesIO

def show_menu():
    print("1)cats photos\n2)random images\n3)nature images")
    

def validation(choice ,available_choices):
    if available_choices == ['y','n']:
        while choice.lower() not in available_choices:
            choice= input("please enter a valid coice(y/n): ")

    else:
        while choice.lower() not in available_choices:
            choice= input(f"please enter a valid coice from {available_choices[0]}-{available_choices[len(available_choices)-1]}: ")
    
    return choice


show_menu()
choice1 = input()
available_inputs = ['1','2','3']


while choice1 not in available_inputs:
    show_menu()
    choice1 = input("please enter a valid input (1,2,3)")
    
print()
print('-'*50)
print()
if choice1 =='1':
    cat_url = "https://api.thecatapi.com/v1/images/search?limit=10&breed_ids=beng&api_key=live_7OOoNwadKl2OS20H6U2hTpEaK5PgxdSclD8ngrJOzHMeRV3gFVfSTOtY0avnR87d"
    response = requests.get(cat_url)

    response.raise_for_status()

    data = response.json()

    no_photos = input("input the number of photos that you want in rage 1-10: ")
    available_no = [str(i) for i in range(1,11)]
    no_photos = validation(no_photos,available_no)


    i =0
    try:
        for image in data:
            i+=1
            print()
            print(f"<ID: > image {i}")
            print("<THE PHOTO'S URL: >",image['url'])
            print()
            choice = input("do you want to open the photo(y/n): ")
            availabe_choices = ['y','n']
            choice = validation(choice,availabe_choices)
            if choice.lower() =='y':
                
                response = requests.get(image['url'])
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                image.show()
                choice4 = input('do you want to save the photo(y/n): ')
                choice4 = choice4.lower()
                choice4 = validation(choice4,['y','n'])

                if choice4=='y':
                    with open(f'cat_image{i}.jpg' , 'wb') as file:
                        file .write(response.content)
                    print('the photo is saved succussefully')
                
                
                    
                
            
            if i == int(no_photos):
                break
    
    
    except:
        print('error')


elif choice1=='2':
    images_url = "https://picsum.photos/v2/list"
    response = requests.get(images_url)
    response.raise_for_status()
    data = response.json()
    photos_num = input("please enter a number between 1-30: ")
    photos_num = validation(choice=photos_num,available_choices=[str(i) for i in range(1,31)])
    i=0
    try:
        for image in data:
            i+=1
            print()
            print('<ID: >',int(image['id'])+1)
            print("<THE PHOTO'S URL: >",image['download_url'])
            print()
            choice3 = input('do you want to open the photo(y/n): ')
            choice3 = choice3.lower()
            choice3 = validation(choice3 , ['y','n'])
            
            if choice3 == 'y':
               
                response = requests.get(image['download_url'])
                response.raise_for_status()
                
                image = Image.open(BytesIO(response.content))
                image.show()
                choice5 = input('do you want to save the photo (y/n): ')
                choice5 = validation(choice5,['y','n'])
                if choice5.lower() =='y':
                    with open(f'random_image{i}.jpg','wb') as file:
                        file.write(response.content)
                
            if i==int(photos_num):
                break
                
 
    except:
        print('error')


elif choice1=='3':
    url = "https://api.pexels.com/v1/search?query=nature&per_page=80"

    headers={'Authorization':'4eIn56IGbmehglN4shDw02ufpYIFmd1pkN63gEVuHeK0h7FtrnuZS3sY'}

    response = requests.get(url ,headers=headers)
    response.raise_for_status()
    data = response.json()
    # print (len(data['photos']))
    choice10 = input('enter the number of nature photo that you want: ')
    choice10 = validation(choice10 , [str(i) for i in range(1,81)])

    i=0
    try:
        for image in data["photos"]:
            i+=1
            print()
            print(f'<ID: > image {i}')
            print("<THE PHOTO'S URL: >",image["src"]["original"])
            print("image's description: ",image['alt'])
            print()
            choice6 = input("do you want to open the photo(y/n): ")
            choice6 = choice6.lower()
            choice6 = validation(choice6,['y','n'])

            if choice6 =='y':
                response = requests.get(image['src']['original'])
                response.raise_for_status()
            
                image = Image.open(BytesIO(response.content))
                image.show()
                image.close()
                choice7 = input("do you want the saved photo(y/n): ")
                choice7 = validation(choice7,['y','n'])
                if choice7=='y':
                    with open(f'nature_image{i}.jpg','wb') as file:
                        file.write(response.content)
                
            if i==int(choice10):
                break
    except:
        print('error')

    


