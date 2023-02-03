import requests
files = {'image': open('temp_files/11.jpg', 'rb')}
print(str(files['image']))
response = requests.post("https://api.imgbb.com/1/upload?expiration=600&key=d97c9fa959c55b28ca72e70cb7e16ddf", data=files)
print(response.status_code)
print(response.json())