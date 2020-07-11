import os
from selenium import webdriver
import pandas as pd
import argparse

## Taking 2 paths as an input using argparser

parser = argparse.ArgumentParser(description='GPS Converter')

parser.add_argument("--input_dir", default=None,
                    help="Path to the folder where GPS files to be converted are located. "
                         "Please enclose path in double quotes.") #Argument for taking input directory path
parser.add_argument("--driver_path", default=None,
                    help="Path to firefox driver which needs to be downloaded. "
                         "Visit https://github.com/mozilla/geckodriver/releases to download required driver as per system specs. "
                         "Please enclose path in double quotes.") #Argument for taking downloaded driver path

args = parser.parse_args()

##Setting Firefox profile preferences to avoid popping of download dialog box

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.manager.showAlertOnComplete",False)
fp.set_preference("browser.download.dir", args.input_dir) #Sets the default directory to download files
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream") #Direct download mentioned file type

##Opening Firefox browser with above profile preferences

driver = webdriver.Firefox(firefox_profile = fp, executable_path = args.driver_path + "\\geckodriver.exe")

##Navigating to GPS visualizer website

driver.get('https://www.gpsvisualizer.com/convert_input')

##Loop for accessing all the files in the specified folder for conversion

for file in os.listdir(args.input_dir):

    browse_button = driver.find_element_by_xpath('//*[@id="input:uploaded_file_1"]')
    browse_button.send_keys(args.input_dir + '\\' + file) #Selecting file under browse button

    convert_button = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td/form/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/input")
    convert_button.click() #Pressing convert button

    download_button = driver.find_element_by_link_text("following link")
    download_link = download_button.get_attribute('href') #Getting download link
    download_file = download_link.split('/')[-1] #Getting downloaded filename

    download_button.click() #Downloading file by pressing 'following link' provided

    os.rename(args.input_dir + '\\' + download_file,args.input_dir + '\\' +  file.split('.')[0] + '.txt') #Renaming downloaded file to event id

    convert_homepage = driver.find_element_by_xpath("/html/body/div/table/tbody/tr/td[2]/table/tbody/tr/td[2]/p[2]/a")
    convert_homepage.click() #Going back to convert homepage

##Loop to access downloaded files and remove time, sat and hdop columns & saving as csv files

for filename in os.listdir(args.input_dir):
    
    if filename.split('.')[1] == 'txt':   #Checking whether file is a downloaded text file

        data = pd.read_table(args.input_dir + '\\' + filename, delimiter = '\t', keep_default_na = False, na_values  = " ") #Reading text file into a dataframe
        data = data.drop(columns=['sat','hdop']) #Removing sat and hdop columns
        
        for row_number in range(len(data)): #Loop to replace time with 1,2,3... sec
            data.loc[row_number,'time'] = row_number+1
            
        data.to_csv(args.input_dir + '\\' + filename.split('.')[0] + '.csv',index = False) #Saving as csv file