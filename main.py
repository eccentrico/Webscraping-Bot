from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
CHROME_DRIVER_PATH="C:\Dev\chromedriver"

ZILLOW_URL="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
GOOGLE_SHEET="https://forms.gle/66cybL4j5nzw2PLb8"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9,hi;q=0.8"
}
response=requests.get(url=ZILLOW_URL,headers=headers).text
soup=BeautifulSoup(response,"html.parser")


a_links=soup.select(".list-card-top a")
#all the links for the houses
element_list=[]

for element in a_links:
    if "https" not in element:
        new=f"https://www.zillow.com/homedetails{element['href']}"
        element_list.append(new)
    else:
        element_list.append(element["href"])

addr=soup.select(".list-card-addr")
#getting the addresses of properties
#list containing the addresses
locations=[]
for addresses in addr:
    locations.append(addresses.text)

#getting the prices 
prices=soup.find_all(name="div",class_="list-card-price")
######list containing the prices 
p_list=[]
for amount in prices:
    p_list.append(amount.text)



########FILLING THE FORM USING SELENIUM
driver=webdriver.Chrome(CHROME_DRIVER_PATH)
for val in range(len(locations)):
    form=driver.get(GOOGLE_SHEET)
    time.sleep(10)
    address=driver.find_element_by_css_selector('.whsOnd.zHQkBf ')
    price=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    address.send_keys(locations[val])
    price.send_keys(p_list[val])
    property_link.send_keys(element_list[val])
    submit_button.click()
		

answer=driver.get('https://docs.google.com/forms/d/1zsjvN04kuUt9ZqNpZttm6H_aUgYykDf9O-mzHe_Mo0w/edit#responses')
time.sleep(3)
spreadsheet=driver.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div/div/span/span/div/div[1]')
spreadsheet.click()



   
        
   

        


   
    
    




