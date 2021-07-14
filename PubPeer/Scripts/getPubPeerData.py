
from selenium.webdriver.support.wait import WebDriverWait

from Utils.ExelUtil import ExcelUtil
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from Utils.Utils import  Utils
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Firefox()
driver.get("https://pubpeer.com/")

"""
driver.find_element_by_name("q").send_keys("Sunil Mukhi")
driver.find_element_by_xpath("//form[@role = 'search']//button").click()
result = driver.find_element_by_xpath("//h3[@class = 'list-description']/span").get_attribute('innerHTML')
print(result)
#time.sleep(10)
"""
rownum = 1
ch_ord = ord("D")
for row in ExcelUtil.getdata(Utils.data_sheet_path,"Sheet1"):
    authname = row[1]



    driver.find_element_by_name("q").send_keys(authname)
    driver.find_element_by_xpath("//form[@role = 'search']//button").click()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mySearchResults")))
    time.sleep(5)
    result = driver.find_element_by_xpath("//h3[@class = 'list-description']/span").get_attribute('innerHTML')
    print(authname+" : "+ result)
    result = result.split(" ")
    ExcelUtil.writedataSingleCell(Utils.data_sheet_path,"Sheet1",'C', rownum,result[0] )
    if result[0] == '0':
        resulttext = driver.find_element_by_xpath("//div[@class = 'recent-comments']/div//h3").text
        print("resulttext : "+resulttext)
        ExcelUtil.writedataSingleCell(Utils.data_sheet_path, "Sheet1", 'D', rownum, resulttext)
    else:
        for i in range (1, int(result[0])+1):
            resultHref = driver.find_element_by_xpath("//div[@class = 'recent-comments']/div[@class = 'publication-list']/div["+str(i)+"]//a").get_attribute(
                'href')

            ExcelUtil.writedataSingleCell(Utils.data_sheet_path, "Sheet1", chr(ch_ord), rownum, resultHref)
            ch_ord +=1

    driver.find_element_by_name("q").clear()
    rownum +=1

#for results
#//div[@class = 'recent-comments']/div[@class = 'publication-list']/div[1]//a
#for 0 results
#//div[@class = 'recent-comments']/div//h3

driver.quit()
