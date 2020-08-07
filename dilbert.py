import os
import requests
from datetime import date
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector


# Get ENV 
try:
    pushover_token = os.environ['PUSHOVER_TOKEN']
except Exception as e:
    print("ERROR: Pushover Token not found", e)

try:
    pushover_user = os.environ['PUSHOVER_USER']
except Exception as e:
    print("ERROR: Pushover User not found", e)


today = (date.today())
url = f"https://dilbert.com/strip/{today.isoformat()}"
print(url)
# example image url:
#url = "https://assets.amuniversal.com/b11775c0a81b0138120f005056a9545d"

r = requests.get(url=url)
if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html.parser')
    #all_links = soup.find_all("a")
    #for link in all_links:
        #print(link.get("href"))
    comic_image = soup.find('img', {'class': 'img-responsive img-comic'})
    print(comic_image.get('src'))
    comic_url = f"https:{comic_image.get('src')}"
    print(comic_url)
    get_comic = requests.get(url=comic_url)
    if get_comic.status_code == 200:
        with open("dilbert.jpg", 'wb') as f:
            f.write(get_comic.content)

    
#with open("dilbert.jpg", 'wb') as f:
#        f.write(r.content)
else:
    print("error getting webpage")


r = requests.post("https://api.pushover.net/1/messages.json", data = {
  "token": pushover_token,
  "user": pushover_user,
  "message": f'Dilbert Comic for {today.strftime("%A %B %d, %Y")}'
},
files = {
  "attachment": ("dilbert.jpg", open("dilbert.jpg", "rb"), "image/jpeg")
})
print(r.text)
