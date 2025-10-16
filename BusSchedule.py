#BusSchedule.py
#Name: Michelle Diaz
#Date:
#Assignment: Homework 2

from datetime import datetime # time module
from zoneinfo import ZoneInfo # timezones
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents



def main():
  Direction = "East"
  Route = "11"
  Stop_Code = "2269"

  url = "https://myride.ometro.com/Schedule?stopCode="+Stop_Code+"&routeNumber="+Route+"&directionName="+Direction
  c1 = loadURL(url) #loads the web page
  #c1 = loadTestPage() #loads the test page
  c1 = c1.split("\n")

  times =[]
  for word in c1:
    if ("AM" in word or "PM" in word) and len(word) < 8:
      times.append(word)
    
  bus_times = []
  for time in times:
     total_minutes = getMinutes(time) + (60*gethours(time))
     bus_times.append(total_minutes)
  
  #print(bus_times)
  
  currTime = datetime.now(ZoneInfo("America/Chicago")).time()
  userTime = currTime.strftime("%I:%M %p")
  userTime = getMinutes(userTime) + (60*gethours(userTime))
  #print(userTime)
  # busTime = datetime.strptime("8:00PM", "%I:%M%p").time()
  time_to_next = 0
  following_bus = 0
  need_following = False
  for time in bus_times:
    if time >= userTime and not need_following:
        time_to_next = time - userTime
        need_following = True
    elif time >= userTime and need_following:
        following_bus = time - userTime
        break
    
  print(f"The current time is {currTime.strftime("%I:%M %p")}")
  print("The next bus will arrive in", time_to_next, "minutes")
  print("The following bus will arrive in", following_bus, "minutes")

  
def getMinutes(time):
    time = time.split(":")
    return int(time[1][0:2])
    
def gethours(time):
    time = time.split(":")
    time_half = time[1][-2:] 
    if time_half == "PM": 
       hour = 12 + int(time[0]) %12
    else:
       hour = int(time[0]) 
    return hour
        
  

main()
