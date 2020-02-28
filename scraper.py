import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# import the webdriver, chrome driver is recommended
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.images': 2})
driver = webdriver.Chrome(chrome_options=chrome_options)

months = ('jan','feb','apr','apr','may','jun','jul','aug','sep','oct','nov','dec')
# insert the tripadvisor's website of one attraction 
driver.get("https://www.tripadvisor.com/Attraction_Review-g187895-d191153-Reviews-or2000-Gallerie_Degli_Uffizi-Florence_Tuscany.html")

# function to check if the button is on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


#time.sleep(2)
#driver.find_element_by_xpath('//span[contains(@class, "ExpandableReview")]').click()
time.sleep(2)

# open the file to save the review
csvFile = open("uffizi_tripadvisor.csv", 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

# change the value inside the range to save more or less reviews
for i in range(0,6000):
    if (check_exists_by_xpath("//span[contains(@class, 'location-review-review-list-parts-ExpandableReview')]")):
        # to expand the review
        
        driver.find_element_by_xpath("//span[contains(@class,'location-review-review-list-parts-ExpandableReview')]").click()
        time.sleep(5)
        
    container = driver.find_elements_by_xpath("//div[contains(@class, 'location-review-card')]")
    num_page_items = len(container);
    #print(container)
    print(num_page_items)
    for j in range(num_page_items):
        # to save the rating
        string = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
        # to save in a csv file readable the star and the review [Ex: 50,"I love this place"]
        data = string.split("_")
        rating = int(data[3])/10
        poster_name = container[j].find_element_by_xpath(".//a[contains(@class,'social-member-event-Member')]").text.replace("\n","")
        #print(poster_name)
        try:
            poster_hometown = container[j].find_element_by_xpath(".//span[contains(@class, 'social-member-common-MemberHometown')]").text.replace('\n',"")
        except NoSuchElementException:
            poster_hometown ='n/a'
        #print(poster_hometown)
        date_block = container[j].find_element_by_xpath(".//div[contains(@class, 'social-member-event-MemberEventOnObjectBlock__event_type')]").text.replace('\n',"")

        
        datax = date_block.split(" ")
        datax = datax[::-1]
        #try:
            #if int(datax[0]) > 0:
        date = str(datax[2]+ ' ' +datax[1])+ " " + str(datax[0])
        #except:
         #   date = str(datax[0])
        #print(date)

        try:
            contributions = container[j].find_element_by_xpath(".//span[contains(@class,'social-member-MemberHeaderStats__stat_item')]").text
        except NoSuchElementException:
            contributions = '0'
        #print(contributions)
        try:
            votes = container[j].find_element_by_xpath(".//span[contains(@class,'social-member-MemberHeaderStats__stat_item')]//following-sibling::span").text
        except:
            votes ='0'
        #print(votes)
        contributions = contributions.strip().split(' ')[0]
        votes = votes.strip().split(' ')[0]
        #print(contributions)
        #print(votes)
        review_text = container[j].find_element_by_xpath(".//q[contains(@class, 'reviewText')]").text.replace("\n", "")
        print(str(rating) + "  " + poster_name + ' ' + poster_hometown + "  " + date + " " + str(contributions) +" contributions  "  +str(votes) + '\n' + review_text) 
        csvWriter.writerow([str(rating),poster_name, poster_hometown, date,contributions,votes,review_text.encode('ascii', 'ignore').decode('ascii') ])

    # to change the page
    driver.find_element_by_xpath('//a[contains(@class, "next")]').click()
    time.sleep(6)

    
driver.close()
