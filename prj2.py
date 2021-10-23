from selenium import webdriver
import re
from time import sleep
import xlsxwriter
from tinydb import TinyDB

db = TinyDB('db.json')
workbook = xlsxwriter.Workbook('result1.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_string(0, 0, 'Publisher Name')
worksheet.write_string(0, 1, 'Journal Title')
worksheet.write_string(0, 2, 'Issn')
worksheet.write_string(0, 3, 'Volume')
worksheet.write_string(0, 4, 'Issue')
worksheet.write_string(0, 5, 'epublish')
worksheet.write_string(0, 6, 'Article Title')
worksheet.write_string(0, 7, 'Vernacular Title')
worksheet.write_string(0, 8, 'First Page')
worksheet.write_string(0, 9, 'Last Page')
worksheet.write_string(0, 10, 'ELocationID pii')
worksheet.write_string(0, 11, 'ELocationID doi')
worksheet.write_string(0, 12, 'Language')
worksheet.write_string(0, 13, 'Authors')
worksheet.write_string(0, 14, 'Publication Type')
worksheet.write_string(0, 15, 'received date')
worksheet.write_string(0, 16, 'Abstract')
worksheet.write_string(0, 17, 'FA Abstarct')
worksheet.write_string(0, 18, 'pdf link')
row = 1

url = 'http://dam.journal.art.ac.ir/'
driver = webdriver.Chrome()
driver.get(url)
ik = driver.find_element_by_xpath('/html/body/div[1]/div/a').click()
title = driver.find_elements_by_css_selector('.fa-plus')
for i in title:
    i.click()
    sleep(1)
links = driver.find_elements_by_css_selector('.issue_dv a')
xml_link_list = []
for i in links:
    page_link = i.get_attribute('href')
    xml_link_code = re.findall(r'.+_(\d+).', page_link)[0]
    xml_link = 'http://dam.journal.art.ac.ir/?_action=xml&issue=' + xml_link_code
    xml_link_list.append(xml_link)  