from bs4 import BeautifulSoup
from requests import get
from urllib3 import disable_warnings
class UdemyParser():
  def __init__(self, url) -> None:
    self.url = url
  def parse(self) -> dict:
    disable_warnings()
    r =get(self.url) 
    soup = BeautifulSoup(r.content, "lxml")
    soup_content = str(soup)
    title = soup.find("h1",{"data-purpose":"lead-title"}).text.strip(" ").strip("\n")
    rate = soup.find("span",{"class":"udlite-heading-sm star-rating--rating-number--2o8YM"}).text #.split("Rating:")[1].split("out of")[0].strip(" ")
    total_registry = soup.find("div",{"data-purpose":"enrollment"}).text.replace("öğrenci","").replace("students","").replace(",",".").strip("\n").strip(" ")
    language = soup.find("div", {"data-purpose":"lead-course-locale"}).text.replace("\n","")
    description = soup.find("div",{"class":"udlite-text-md clp-lead__headline"}).text.strip("\n")
    last_update = soup.find("div",{"class":"last-update-date"}).text.strip("\n")
    last_update = last_update.split("Last updated")[1].strip(" ") if "Last updated" in last_update else last_update.split("Son güncelleme tarihi:")[1].strip(" ")
    instructor = soup.find("a",{"class":"udlite-btn udlite-btn-large udlite-btn-link udlite-heading-md udlite-text-sm udlite-instructor-links"}).text
    image_src = [x["src"] for x in soup.select("img[src]")][2]
    soup_content = str(soup)
    durate =  soup_content.find('"video_content_length":') if soup_content.find('"video_content_length":') > 0 else soup_content.find('video_content_length')
    if '"video_content_length":' not in soup_content:
      start_index=soup_content.find('video_content_length')
      hours = soup_content[start_index+33:start_index+45:1]
      length = ""
      y = hours.split(",")
      if "dak " not in soup_content:
        if "," in hours:
          for x in hours.split(","):
            if x.isdigit():
              length += x
            else:
              for i in x:
                if i in "0123456789":
                  length+=f",{i}"
        else:
            for x in hours:
              if x.isdigit():
                length+=x
      else:
        length = "1"
    else:
      if "mins " not in soup_content:
        start_index=soup_content.find('"video_content_length":')
        hours = soup_content[start_index+24:start_index+35]
        length = ""
        if "." in hours:
          y = hours.split(",")
          for x in hours.split("."):
            if x.isdigit():
              length += x
            else:
              for i in x:
                if i in "0123456789":
                  length+=f".{i}"
    
        else:
          for x in hours:
            if x.isdigit():
              length+=x
      else:
        length = "1"      

    if "," in length or "." in length:
        if "," in length: length = length.split(",")[0]
        else: length = length.split(".")[0]
    return {"title":title, "language":language, "instructor":instructor,"rate":rate, "total_student":total_registry, "description":description,"last_update":last_update,"duration":length, "course_banner_uri":image_src }
  
URL = "https://www.udemy.com/course/sifirdan-flutter-ile-android-ve-ios-apps-development/"
cli = UdemyParser(URL)
result = cli.parse()

print(result)

# Output:
"""
{'title': 'Sıfırdan Flutter ile Android ve Ios Apps Development', 'language': 'Türkçe', 'instructor': 'Emre Altunbilek','rate': '4,6','total_student': '12.016',
'description': "Dart & Flutter SDK'yı sıfırdan öğrenip; Android ve IOS'da çalışabilen yüksek performanslı native uygulamalar geliştirin", 'last_update': '1/2022', 'duration': '90',
'course_banner_uri': 'https://img-b.udemycdn.com/course/240x135/2102110_e157_4.jpg?secure=gUbXtUVP7Tfl8e7h99ZVMw%3D%3D%2C1643040035'}
"""

