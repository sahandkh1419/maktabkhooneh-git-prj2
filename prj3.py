from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = 'https://aata.getty.edu/primo-explore/search?query=any,contains,stone&pfilter=pfilter,exact,articles&tab=aata' \
      '&search_scope=AATA&vid=AATA&offset=0'

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(5)
title = driver.find_elements_by_css_selector('.item-title')
window_before = driver.window_handles[0]
for i in title:
    ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).click(i).key_down(Keys.CONTROL).key_down(Keys.SHIFT).perform()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    driver.implicitly_wait(7)
    result = []
    j = 1
    while True:
        try:
            xpath = '//*[@id="item-details"]/div/div' + '[' + str(j) + ']'
            each_detail = driver.find_element_by_xpath(xpath)
            each_detail = each_detail.text.split('\n')
            value_title = each_detail[0]
            value = " ".join(each_detail[1:])
            final = '%s: %s' % (value_title, value)
            result.append(final)
            j += 1
            continue
        except:
            break
    print(result)
    print('------------------------------------------------------------------------')

    driver.close()
    driver.switch_to.window(window_before)
driver.close()
