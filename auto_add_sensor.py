from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
driver = webdriver.Chrome('./chromedriver',options=options)
driver.get("https://10.173.24.119/index.htm")

driver.find_element("xpath","//*[@id='details-button']").click()
driver.find_element("xpath","//*[@id='proceed-link']").click()

username = driver.find_element("xpath","//*[@id='loginusername']")
password = driver.find_element("xpath","//*[@id='loginpassword']")

username.send_keys("prtgadmin")
password.send_keys("Prtg@2022")

driver.find_element("xpath","//*[@id='submitter1']").click()

# Get list link sensor
def get_link_full(device_link_id):
    driver.get(device_link_id)
    time.sleep(4)
    link_full = driver.find_element(By.XPATH,"//*[@id='table_devicesensortable']/thead[1]/tr/th/a[@href]")
    link_full = link_full.get_attribute('href')
    return link_full

# Get list link sensor
def get_list_link_sensor(link_full):
    list_link_sensor = []
    driver.get(link_full)
    elementlinks = driver.find_elements(By.XPATH,"//*[@id='table_devicesensortable']/tbody/tr/td[2]/div/a[@href]")
    #print(elementlinks)
    time.sleep(4)
    for link in elementlinks:
        link = link.get_attribute('href')
        list_link_sensor.append(link)
    return list_link_sensor

# Rename sensor 
def rename_sensor(link_sensor,value_new_input):
    driver.get(link_sensor)
    time.sleep(2)
    sensor_input = driver.find_element("xpath","//*[@id='main']/div/ul/li[9]/a").click()
    driver.refresh()
    time.sleep(7)
    sensor_desc = driver.find_element("xpath","//*[@id='objectdataform']/fieldset[1]/div/div[1]/input")
    sensor_desc.clear()
    sensor_desc.send_keys(value_new_input)
    time.sleep(2)
    sel = Select(driver.find_element(By.ID,"primarychannel_"))
    #print(sel)
    sel.select_by_visible_text ('Pre Policy Size (kbit/s)')
    driver.find_element("xpath","//*[@id='objectdataform']/div/div/input[1]").click()
    time.sleep(2)
    
# Read file csv
def read_file_csv():
    list_description = []
    with open('description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            list_description.append(row[1])
    return list_description

if __name__ == "__main__":
    link_full = get_link_full("https://10.173.24.119/device.htm?id=11101&tabid=1")
    list_sensor = get_list_link_sensor(link_full)
    list_description = read_file_csv()
    if len(list_sensor) == len(list_description):
        for i in range(len(list_sensor)):
            rename_sensor(list_sensor[i],list_description[i])
