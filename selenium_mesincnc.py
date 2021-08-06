from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo
import time
import datetime



def make_data():
    #driver setup
    driver = webdriver.Chrome('D:\chromedriver.exe')


    #mongo connect
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['mesin-cnc']
    mycol = mydb["raw_photo_value"]
    myseccol = mydb["machine_status"]
    
    temp_dict = {}
    curDT = datetime.datetime.now()
    strCurDT = str(curDT.day)+'-'+str(curDT.month)+'|'+str(curDT.hour)+':'+str(curDT.minute)+':'+str(curDT.second)+':'+str(curDT.microsecond)
    temp_dict['time_get_data'] = strCurDT

    #scraping
    driver.get('http://192.168.12.35/')
    text = driver.find_element_by_xpath("/html/body").text.split(" ")
    s1 = int(text[3])
    s2 = int(text[7])
    temp_dict['ldr_sensor_a'] = s1
    temp_dict['ldr_sensor_b'] = s2
    temp_dict['machine_name'] = 'Bystronic Laser Cutting'
    temp_dict['location'] = 'Workshop Heavy Machining Center'
    if(s1<200):
        temp_dict['lampu_a'] = False
    else:
        temp_dict['lampu_a'] = True

    if(s2<450):
        temp_dict['lampu_b'] = False
    else:
        temp_dict['lampu_b'] = True
    if (s1<200 and s2<450):
        temp_dict['status_mesin'] = 0
    elif (s1<200 and s2>450):
        temp_dict['status_mesin'] = 3
    elif (s1>200 and s2<450):
        temp_dict['status_mesin'] = 1
    elif (s1>200 and s2>450):
        temp_dict['status_mesin'] = 2
    else:
        temp_dict['status_mesin'] = 400

    myseccol.insert_one(temp_dict)
    driver.close()

if __name__ == "__main__":
    while True:
        make_data()
        time.sleep(60)


