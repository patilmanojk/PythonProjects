import math

from selenium.webdriver.support.wait import WebDriverWait

from Utils.ExelUtil import ExcelUtil
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from Utils.Utils import  Utils
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
###########################################################
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "enter account sid"
# Your Auth Token from twilio.com/console
auth_token  = "enter auth token"

client = Client(account_sid, auth_token)



###########################################################
#driver = webdriver.Firefox()
driver.get("https://www.cowin.gov.in/home")

#//li[@class = 'availability-date']
#(//div[@class='row-disp'])[246]
#(//div[contains(@class, 'center-box')]//ul[@class = 'slot-available-wrap']//div[contains(@class , 'vaccine-box')])[84]

#Search keywords and get results and save in the Spreadsheet

driver.find_element_by_xpath("//div[contains(@class, 'status-switch')]").click()
driver.find_element_by_xpath("//div[@id = 'mat-select-value-1']").click()
driver.find_element_by_xpath("//mat-option[@id = 'mat-option-21']").click()
time.sleep(1)
driver.find_element_by_xpath("//mat-select[@id = 'mat-select-2']").click()
driver.find_element_by_xpath("//mat-option[@id = 'mat-option-61']").click()
driver.find_element_by_xpath("//button[text()= 'Search']").click()
time.sleep(5)
dates = driver.find_elements_by_xpath("//li[@class = 'availability-date']")
#print("No of dates booking avilable for : {0}".format(len(dates)))
Hospitals = driver.find_elements_by_xpath("//div[@class='row-disp']")
#print("No of Hospitals  avilable for booking: {0}".format(len(Hospitals)))
AvailableSlot= []
noOfWeeks = len(dates)//7
#noOfWeeks = 1
for i in range(noOfWeeks):
    if (len(dates)%7 ==0 ):
        DaysinWeek = 7
    elif ( i == noOfWeeks -1 ):
        DaysinWeek = len(dates)%7
    Hospitals = driver.find_elements_by_xpath("//div[@class='row-disp']")
    #print("No of Hospitals  avilable for booking: {0}".format(len(Hospitals)))
    BkgSlots = driver.find_elements_by_xpath("//div[contains(@class, 'center-box')]//ul[@class = 'slot-available-wrap']//div[contains(@class , 'vaccine-box')]")
    #for x in BkgSlots:
    #    print(x.text)
    #print("No of booking slots :{0}".format(len(BkgSlots)))
    bkidx = 0
    for k in range(len(Hospitals)):
        for j in range(DaysinWeek):
            """

            print(dates[j].text)
            print(Hospitals[k].text)
            print(BkgSlots[bkidx].text)
            
            print(bkidx)

            """
            if (BkgSlots[bkidx].text != 'NA' and "Booked" not in BkgSlots[bkidx].text
            and "Age 18+" in BkgSlots[bkidx].text):
                #print(dates[j].text)
                #print(Hospitals[k].text)
                #print(BkgSlots[bkidx].text)

                if ("411" in Hospitals[k].text):
                    AvailableSlot.append(dates[j].text+ " Hospital: "+ Hospitals[k].text)

            bkidx += 1
            #print(bkidx)
    #print("Week {0} completed".format(i))
    driver.find_element_by_xpath("//a[@class = 'right carousel-control carousel-control-next ng-star-inserted']").click()
    time.sleep(5)

if len(AvailableSlot) > 0:
    print("{0} Slots available in Pune City".format(len(AvailableSlot)))
    message = client.messages.create(
        to="+919503132885",
        from_="+17028305161",
        body="{0} Slots available in Pune City".format(len(AvailableSlot)))
    print(message.sid)
else:
    print("Slots not available in Pune City")



driver.quit()
