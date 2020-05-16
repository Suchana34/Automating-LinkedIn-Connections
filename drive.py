import parameters
import csv
from parsel import Selector
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
#keyboard keys

writer = csv.writer(open(parameters.result_file, 'w')) #output csv file
writer.writerow(['name', 'job_title', 'education', 'ln_url'])

#download chrome web driver and store in drive C
driver = webdriver.Chrome('C:\webdriver\chromedriver')
driver.maximize_window
sleep(0.5)

#let us test with linkedIn
driver.get('https://www.linkedin.com/')
sleep(5)

#click on the sign in button
driver.find_element_by_xpath('//a[text()= "Sign in"]').click()
sleep(5)

#sign in details
username_input = driver.find_element_by_name('session_key')
username_input.send_keys(parameters.username)
sleep(0.6)

password_input = driver.find_element_by_name('session_password')
password_input.send_keys(parameters.password)
sleep(0.6)

# click the button
driver.find_element_by_xpath('//button[text() = "Sign in"]').click()
sleep(5)

# scraping the data
driver.get('https://www.google.com/')
sleep(5)

# type the query for search in search area of google
#driver.find_element_by_xpath('//input[@name = "q"]')
search_input = driver.find_element_by_name('q')
search_input.send_keys(parameters.search_query)
sleep(1)

search_input.send_keys(Keys.RETURN)
#pressing the return key
sleep(3)

#checking the heading of each link
profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
#len(profiles) = 10

#to iterate over each link
profiles = [profile.get_attribute('href') for profile in profiles]

#to iterate over each profile
for profile in profiles:
    driver.get(profile)
    sleep(5)

    sel = Selector(text = driver.page_source)
    #sel.xpath('//title/text()').extract_first()
    # but this doesnt return in list, so
    name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
    job_title = sel.xpath('//h2/text()').extract_first().strip()
    education = sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract()
    ln_url = driver.current_url

    #store in csv file
    writer.writerow([name, job_title, education, ln_url])

    try:
        #connect people
        #when more than 2nd degree connection
        driver.find_element_by_xpath('//*[text() = "More..."]').click()
        driver.find_element_by_xpath('//*[text() = "Connect"]').click()
        driver.find_element_by_xpath('//*[text() = "Send now"]').click()
        
    except:
        pass

driver.quit()

