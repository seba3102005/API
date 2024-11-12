import requests
from PIL import Image
from io import BytesIO
import time
import json

json_data = {}

def show_menu():
    print("1)cats photos\n2)random images\n3)nature images\n4)Exit")
    

def validation(choice ,available_choices):
    if available_choices == ['y','n']:
        while choice.lower() not in available_choices:
            choice= input("please enter a valid coice(y/n): ")

    else:
        while choice.lower() not in available_choices:
            choice= input(f"please enter a valid coice from {available_choices[0]}-{available_choices[len(available_choices)-1]}: ")
    
    return choice



#generates 5 images per yield in order not to load all the data at once
#generates a list of dictionaries of the 5 images
def generator (data,size=5):
    for partOfdata in range(0,len(data),size):
        yield data[partOfdata:partOfdata+size]

def time_taken_request(func ):
    
    def wrapper(*args,**kwargs):

        b_time = time.time()
        data = func(*args ,**kwargs)
        e_time = time.time()
        #print what happens in the wrapper
        print(f"the request's time including any retries: {e_time-b_time} seconds")
        #then return the original return of the called function
        return data

    return wrapper

def failed_requests(func,retries=3):

    def wrapper(*args,**kwargs):
        attempts=0
        while attempts<retries:
            try:
                
                
                data = func(*args ,**kwargs)
                return data
        
            except:
                attempts+=1
                print ("this request is failed trying out one more time")
                
    return wrapper



@time_taken_request  
@failed_requests
def make_request(url ,headers):
    if headers ==False:
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data

        except:
            raise
            
        
    else :
        try:
            response = requests.get(url,headers=headers)
            response.raise_for_status()
            data = response.json()
            return data

        except:
            raise
    
    
with open('data.json','r') as file:
    try:
        json_data = json.load(file)
    except:
        print('error in reading the file')
    



while True:
    show_menu()
    api_choice = input()
    api_choice = validation(api_choice,['1','2','3','4'])
    print()
    print('-'*50)
    print()

    if api_choice =='1':
        cat_url = "https://api.thecatapi.com/v1/images/search?limit=10&breed_ids=beng&api_key=live_7OOoNwadKl2OS20H6U2hTpEaK5PgxdSclD8ngrJOzHMeRV3gFVfSTOtY0avnR87d"
        
        

        data = make_request(cat_url, False)
        if data == None:
            print ("the requset to this website fails")
            continue
        


        no_photos = input("input the number of photos that you want in range 1-10: ")
        available_no = [str(i) for i in range(1,11)]
        no_photos = validation(no_photos,available_no)
        
        flag2 = False
        i =0
        
        try:
            for image in generator(data):
                indx = 0
                for j in range(5):

                
                    i+=1
                    print()
                    print(f"<ID: > image {i}")
                    print("<THE PHOTO'S URL: >",image[indx]['url'])
                    print()

                    

                    is_opened = input("do you want to open the photo(y/n): ")
                    availabe_choices = ['y','n']
                    is_opened = validation(is_opened ,availabe_choices)
                    is_opened  = is_opened .lower()
                    if is_opened  =='y':
                
                        response = requests.get(image[indx]['url'])
                        response.raise_for_status()
                        image2 = Image.open(BytesIO(response.content))
                        image2.show()
                        is_saved  = input('do you want to save the photo(y/n): ')
                        is_saved  = is_saved .lower()
                        is_saved  = validation(is_saved ,['y','n'])

                        if is_saved =='y':
                            with open(f'cat_image{i}.jpg' , 'wb') as file:
                                file .write(response.content)
                            print('the photo is saved succussefully')
                            json_data[image[indx]['url']]=f'saved_cat_image{i}.jpg'

                        elif is_saved =='n':
                            json_data[image[indx]['url']]=f'opened_cat_image{i}.jpg'
                    
                    elif is_opened =='n':
                        json_data[image[indx]['url']]=f'NotOpened_cat_image{i}.jpg'
                
                
                    
                
                    
                    if i == int(no_photos):
                        flag2=True
                        break
                    indx+=1
                if flag2 ==True:
                    break
    
    
        except requests.RequestException as e:
            print("An error occurred while fetching the image:", e)
            


    elif api_choice=='2':
        
        images_url = "https://picsum.photos/v2/list"
        data = make_request(images_url ,False)
        
        
        photos_num = input("please enter a number between 1-30: ")
        photos_num = validation(choice=photos_num,available_choices=[str(i) for i in range(1,31)])
        i=0
        
        flag2=False
        try:
            for image in generator(data):
                indx = 0
                for j in range(5):
                    
                    i+=1
                    print()
                    print('<ID: >',int(image[indx]['id'])+1)
                    print("<THE PHOTO'S URL: >",image[indx]['download_url'])
                    print()
                    is_opened = input('do you want to open the photo(y/n): ')
                    is_opened = is_opened.lower()
                    is_opened = validation(is_opened , ['y','n'])
            
                    if is_opened == 'y':
               
                        response = requests.get(image[indx]['download_url'])
                        response.raise_for_status()
                
                        image2 = Image.open(BytesIO(response.content))
                        image2.show()
                        is_saved  = input('do you want to save the photo (y/n): ')
                        is_saved  = validation(is_saved ,['y','n'])
                        is_saved  = is_saved.lower()
                        if is_saved  =='y':
                            with open(f'random_image{i}.jpg','wb') as file:
                                file.write(response.content)
                            json_data[image[indx]['url']]=f'saved_random_image{i}.jpg'

                        elif is_saved =='n':
                            json_data[image[indx]['url']]=f'opened_random_image{i}.jpg'
                    
                    elif is_opened =='n':
                        json_data[image[indx]['url']]=f'NotOpened_random_image{i}.jpg'
                
                
                
                    if i==int(photos_num):
                        flag2=True
                        break
                    indx+=1
                if flag2 ==True:
                    break
 
        except requests.RequestException as e:
            print("An error occurred while fetching the image:", e)
            


    elif api_choice=='3':
        url = "https://api.pexels.com/v1/search?query=nature&per_page=80"

        headers={'Authorization':'4eIn56IGbmehglN4shDw02ufpYIFmd1pkN63gEVuHeK0h7FtrnuZS3sY'}

        data = make_request(url ,headers)

        # print (data)
        no_photos = input('enter the number of nature photo that you want(1-80): ')
        no_photos = validation(no_photos , [str(i) for i in range(1,81)])
        
        i=0
        flag2= False
        try:
            
            for image in generator(data['photos']):
                indx = 0
                
                for j in range(5):

                
                    i+=1
                    print()
                    print(f'<ID: > image {i}')
                    print("<THE PHOTO'S URL: >",image[indx]["src"]["original"])
                    print("image's description: ",image[indx]['alt'])
                    print()
                    is_opened = input("do you want to open the photo(y/n): ")
                    is_opened = is_opened.lower()
                    is_opened = validation(is_opened,['y','n'])

                    if is_opened =='y':
                        response = requests.get(image[indx]['src']['original'])
                        response.raise_for_status()
            
                        image2 = Image.open(BytesIO(response.content))
                        image2.show()
                        image2.close()
                        is_saved = input("do you want the saved photo(y/n): ")
                        is_saved = validation(is_saved,['y','n'])
                        is_saved = is_saved.lower()
                        if is_saved=='y':
                            with open(f'nature_image{i}.jpg','wb') as file:
                                file.write(response.content)
                            json_data[image[indx]['url']]=f'saved_nature_image{i}.jpg'

                        elif is_saved=='n':
                            json_data[image[indx]['url']]=f'opened_nature_image{i}.jpg'
                    
                    elif is_opened =='n':
                        json_data[image[indx]['url']]=f'NotOpened_nature_image{i}.jpg'
                
                
                
                    if i==int(no_photos):
                        flag2 =True
                        break
                    indx+=1
                if flag2 ==True:
                    break
        except requests.RequestException as e:
            print("An error occurred while fetching the image:", e)
            


    elif api_choice == '4':
        with open('data.json','w') as file:
            json.dump(json_data,file)
        print('all data has the images status has be saved')
        print ("exitting the program")
        break

   


    


