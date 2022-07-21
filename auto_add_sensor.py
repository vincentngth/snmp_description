from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(r'C:\Users\tulam\get_snmp_script\chromedriver.exe')
driver.maximize_window()
driver.get("http://10.173.24.120/index.htm")
eleButton=driver.find_element("xpath","//*[@id='details-button']")

eleButton.click()
eleLink = driver.find_element("xpath","//*[@id='proceed-link']")
eleLink.click()

username = driver.find_element("xpath","//*[@id='loginusername']")
password = driver.find_element("xpath","//*[@id='loginpassword']")

username.send_keys("prtgadmin")
password.send_keys("Prtg@2022")

driver.find_element("xpath","//*[@id='submitter1']").click()

def get_link_device_update_description(device_link):
    device_link = driver.get(device_link)
    sensor_links = device_link.find_element(By.CSS_SELECTOR,".col-sensor")
    #sensor_links.click()
    for sensor in sensor_links:
        print(sensor)
    

def update_description():
    pass

def update_primary_channel():
    pass

if __name__ == "__main__":
    get_link_device_update_description("https://10.173.24.120/device.htm?id=8253&tabid=1")
