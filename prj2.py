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
    
for i in xml_link_list:
    driver.get(i)
    source = driver.page_source
    PublisherName = re.findall(r'<PublisherName>(.+)<', source)
    JournalTitle = re.findall(r'<JournalTitle>(.+)<', source)
    Issn = re.findall(r'<Issn>(.+)<', source)
    Volume = re.findall(r'<Volume>(.+)<', source)
    Issue = re.findall(r'<Issue>(.+)<', source)
    epublish = re.findall(r'\"epublish\">\n.+>(\d+).*\n.+>(\d+).*\n.+>(\d+).*', source)
    epublish = list(map(lambda x: ' '.join(x), epublish))
    ArticleTitle = re.findall(r'<ArticleTitle>(.[\S\s]+?)</', source)
    ArticleTitle = list(map(lambda x: x.replace('\n', ''), ArticleTitle))
    VernacularTitle = re.findall(r'<VernacularTitle>(.[\S\s]+?)</', source)
    VernacularTitle = list(map(lambda x: x.replace('\n', ''), VernacularTitle))
    FirstPage = re.findall(r'<FirstPage>(\d+)</', source)
    LastPage = re.findall(r'<LastPage>(\d+)</', source)
    ELocationID_pii = re.findall(r'\"pii.+?(\d+)</', source)
    ELocationID_doi = re.findall(r'\"doi\">(.+)</', source)
    Language = re.findall(r'<Language>(.+)</', source)
    AuthorList = re.findall(r'<AuthorList>[\s\S]+?</AuthorList>', source)  # don't use
    FirstName = list(map(lambda x: re.findall(r'<FirstName>(.+)<', x), AuthorList))  # don't use
    LastName = list(map(lambda x: re.findall(r'<LastName>(.+)<', x), AuthorList))  # don't use
    Affiliation = list(map(lambda x: re.findall(r'<Affiliation>([\s\S]+?)</Affiliation>', x), AuthorList))  # don't use
    Affiliation = list(map(lambda x: [y.replace('\n', '') for y in x], Affiliation))
    FN_LN_Aff = []
    for FN, LN, Aff in zip(FirstName, LastName, Affiliation):
        author = []
        for m, n, p in zip(FN, LN, Aff):
            author.append("%s %s: %s" % (m, n, p))
        FN_LN_Aff.append("  --  ".join(author))
    # use FN_LN_Aff
    PublicationType = re.findall(r'<PublicationType>(.+)</', source)
    received_date = re.findall(r'\"received\">\n.+?(\d+).+\n.+?(\d+).+\n.+?(\d+).+', source)
    received_date = list(map(lambda x: ' '.join(x), received_date))
    Abstract = re.findall(r'<Abstract>([\s\S]+?)</', source)
    Abstract = list(map(lambda x: x.replace('&lt;br /&gt;&lt;strong&gt; &lt;/strong&gt;', ' ').replace('\n', ' ').replace('Abstract', ' ').replace('&lt;br /&gt;', ' ').replace('&lt;span class="fontstyle0"&gt;', ' ').replace('&lt;span style="font-family: TimesNewRomanPSMT; font-size: 10pt; color: #231f20; font-style: normal; font-variant: normal;"&gt;', ' ').replace('&lt;em&gt;&lt;span style="font-family: ARTUNIV-Italic;"&gt;', ' ').replace('&lt;strong&gt; &lt;/strong&gt;  ', ' ').replace('&lt;/span&gt;', ' ').replace('&lt;span style="font-family: ARTUNIV; font-size: xx-small;"&gt;&lt;span style="font-family: ARTUNIV; font-size: xx-small;"&gt; &lt;span style="font-family: ARTUNIV;"&gt;', ' ').replace('&lt;/em&gt;&lt;span style="font-family: ARTUNIV;"&gt;', ' ').replace('&lt;sub&gt;', ' ').replace('&lt;em&gt;', ' ').replace('&lt;br style="font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-align: -webkit-auto; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px;" /&gt;', ' ').replace('&lt;/sub&gt;', ' ').replace(';/em&gt;', ' ').replace('&lt;strong&gt;.&lt;/strong&gt;', ' ').replace('&lt;/em&gt;', ' ').replace('&amp;', ' ').replace('&lt;br class="Apple-interchange-newline" /&gt;', ' ').replace('&lt', ' ').replace(';span style="font-family: ARTUNIV;"&gt;»', ' ').replace(';span style="font-family: ARTUNIV; font-size: xx-small;"&gt; ;span style="font-family: ARTUNIV; font-size: xx-small;"&gt;    ;span style="font-family: ARTUNIV;"&gt;', ' '), Abstract))
    FA_Abstract = re.findall(r'<OtherAbstract Language=\"FA\">([\s\S]+?)</', source)
    FA_Abstract = list(map(
        lambda y: y.replace('&lt;strong&gt;&lt;em&gt;', ' ').replace('&lt;/em&gt;&lt;/strong&gt;', ' ').replace('\n', ' ').replace('&lt;br /&gt;', ' ').replace('&lt;span class="fontstyle0"&gt;', ' ').replace('&lt;span style="font-family: TimesNewRomanPSMT; font-size: 10pt; color: #231f20; font-style: normal; font-variant: normal;"&gt;', ' ').replace('&lt;em&gt;&lt;span style="font-family: ARTUNIV-Italic;"&gt;', ' ').replace('&lt;strong&gt; &lt;/strong&gt;  ', ' ').replace('&lt;/span&gt;', ' ').replace('&lt;span style="font-family: ARTUNIV; font-size: xx-small;"&gt;&lt;span style="font-family: ARTUNIV; font-size: xx-small;"&gt; &lt;span style="font-family: ARTUNIV;"&gt;', ' ').replace('&lt;/em&gt;&lt;span style="font-family: ARTUNIV;"&gt;', ' ').replace('&lt;sub&gt;', ' ').replace('&lt;em&gt;', ' ').replace('&lt;br style="font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-align: -webkit-auto; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px;" /&gt;', ' ').replace('&lt;/sub&gt;', ' ').replace(';/em&gt;', ' ').replace('&lt;strong&gt;.&lt;/strong&gt;', ' ').replace('&lt;/em&gt;', ' ').replace('&amp;', ' ').replace('&lt;br class="Apple-interchange-newline" /&gt;', ' ').replace('&lt', ' ').replace(';span style="font-family: ARTUNIV;"&gt;»', ' ').replace(';span style="font-family: ARTUNIV; font-size: xx-small;"&gt; ;span style="font-family: ARTUNIV; font-size: xx-small;"&gt;    ;span style="font-family: ARTUNIV;"&gt;', ' ').replace(';sup&gt;3 ;/sup&gt;', ' '), FA_Abstract))
    pdf_link = re.findall(r'pdf\">([\s\S]+?pdf)', source)

    print("#############################NEXT LINK#################################")
    sleep(2)