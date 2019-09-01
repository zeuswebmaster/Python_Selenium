import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from lxml import html
import unicodecsv as csv
import time
import random
import json

raw_question_url =''
raw_off_answer_numbers = 0
raw_log_answer_numbers = 0
def parse_page(htmlstring, driver, driver1):
    
    email = 'alexander_lachinger@hotmail.com'
    pwd = 'wJm83Ikh'

    signin_button = driver.find_element_by_xpath("//div[contains(@class, 'signup_login_buttons')]")
    signin_button.click()
    time.sleep(10)
    
    account_button = driver.find_element_by_xpath("//div[contains(@class, 'form_buttons') and contains(@class, 'signup_form_buttons')]/span[1]/a[contains(@class, 'login_link')]")
    account_button.click()
    time.sleep(2)

    email_input = driver.find_elements_by_xpath("//input[contains(@class, 'text_wide')]")
    email_input[0].send_keys(email)
    time.sleep(2)

    password_input = driver.find_elements_by_xpath("//input[contains(@class, 'text_wide')]")
    password_input[1].send_keys(pwd)

    login_button = driver.find_element_by_xpath("//div[contains(@class, 'form_buttons') and contains(@class, 'p1')]")
    login_button.click()

    time.sleep(3)
    
    global raw_question_url 
    time.sleep(5)
    now_counts = driver.find_elements_by_xpath("//a[@class='question_link']")
    print("now_counts-------------------------------------->", len(now_counts))
    i = 1
    flag = True
    while (flag):
        print("all_count-------------------->", i)
        if i >= 0:
            try:
                question_url = driver.find_element_by_xpath(("//div[contains(@class, 'PagedList') and contains(@class, 'TopicAllQuestionsList')]/div[{}]//a[@class='question_link']").format(i)).get_attribute('href')
            except:
                flag = False
                # print("---------------------THE END-------------------------")    
                return
            print("question_url----------------->", question_url)
            
            raw_question_url = question_url
            driver1.get(raw_question_url)
            parse_question(driver1.page_source, driver1)
            
            
        if i % 20 == 1:
            try:
                scroll_target = driver.find_element_by_xpath("//div[contains(@class, 'PagedList') and contains(@class, 'TopicAllQuestionsList')]/div[{}]".format(i + 20))
                scroll_target.location_once_scrolled_into_view
                time.sleep(10)
            except:
                continue
                # flag = False
                # print("---------------------THE END-------------------------")
        i = i + 1

def parse_question(htmlstring, driver1):
    print("second parse---------------------------------??????----------")
    time.sleep(0.5)
    global raw_off_answer_numbers
    global raw_log_answer_numbers
    ANSWER_XPATH   = "//div[contains(@class, 'answer_count')]"
    try:
        raw_official_answer = driver1.find_element_by_xpath(ANSWER_XPATH).text
        raw_official_answers = raw_official_answer.split()
        raw_off_answer_numbers = raw_official_answers[0]
    except:
        raw_off_answer_numbers = 0

    # counts = driver1.find_elements_by_xpath("//div[contains(@class, 'pagedlist_item')]")
    # count = len(counts)

    # try:
    #     raw_log_answer = driver1.find_element_by_xpath("//div[contains(@class, 'collapse_link_wrapper')]").text
    #     raw_log_answers = raw_log_answer.split()
    #     raw_log_answer_numbers = raw_log_answers[0]
    # except:
    #     try:
    #         # response.xpath('(//div[@class="sku"])[2]/p/text()').extract()
    #         f_target = driver1.find_element_by_xpath("//div[contains(@class, 'paged_list_wrapper')]/div[{}]".format(count))
    #         f_target.location_once_scrolled_into_view
    #         time.sleep(5)
    #         s_count = len(driver1.find_elements_by_xpath("//div[contains(@class, 'pagedlist_item')]"))
    #         available = True
    #         while(available):
    #             if count != s_count:
    #                 count = s_count
    #                 s_target = driver1.find_element_by_xpath("//div[contains(@class, 'paged_list_wrapper')]/div[{}]".format(s_count))
    #                 s_target.location_once_scrolled_into_view
    #                 time.sleep(5)
    #                 s_count = len(driver1.find_elements_by_xpath("//div[contains(@class, 'pagedlist_item')]"))
    #             if count == s_count:
    #                 available = False
    #         raw_log_answer = driver1.find_element_by_xpath("//div[contains(@class, 'collapse_link_wrapper')]").text
    #         raw_log_answers = raw_log_answer.split()
    #         raw_log_answer_numbers = raw_log_answers[0]
    #     except:
    #         print("continue")

    question_log_url = raw_question_url + '/log'

    driver1.get(question_log_url)
    parse_log_question(driver1.page_source, driver1)

def parse_log_question(htmlstring, driver1):
    
    raw_category_item = ''
    time.sleep(0.5)
    print("-------------------------Question Start-------------------")
    # try:
    QUESTION_XPATH = "//span[contains(@class, 'ui_qtext_rendered_qtext')]"
    CATEGORY_XPATH = "//div[contains(@class, 'u-inline-block')]//span[contains(@class, 'TopicNameSpan') and contains(@class, 'TopicName')]"
    
    # FOLLOWER_XPATH = "//div[contains(@class, 'HighlightRow') and contains(@class, 'FollowersRow')]"
    FOLLOWER_XPATH = "//div[@class='QuestionStats']/div[2]/span[1]/div"
    
    FOLLOWER_XPATH_2 = "//div[contains(@class, 'HighlightRow') and contains(@class, 'FollowersRow')]"

    VIEW_XPATH     = "//div[@class='QuestionStats']/div[2]/span[2]/div"
    
    raw_question    = driver1.find_element_by_xpath(QUESTION_XPATH).text
    raw_categories  = driver1.find_elements_by_xpath(CATEGORY_XPATH)
    # raw_answer_counts = len(driver1.find_elements_by_xpath(ANSWER_XPATH))
    raw_follower    = driver1.find_element_by_xpath(FOLLOWER_XPATH).text
    raw_view        = driver1.find_element_by_xpath(VIEW_XPATH).text

    raw_followers = raw_follower.split()
    raw_follower_counts = raw_followers[0]

    raw_views = raw_view.split()
    raw_view_counts = raw_views[0]


    n = 1
    for raw_category in raw_categories:
        if n == len(raw_categories):
            raw_category_item = raw_category_item + raw_category.text
        else:
            raw_category_item = raw_category_item + raw_category.text + ", "
        n = n + 1

    print("raw_question--------------------------------------->", raw_question)
    print("raw_question_url----------------------------------->", raw_question_url)
    print("raw_category_item---------------------------------->", raw_category_item)
    print("raw_off_answer_numbers----------------------------->", raw_off_answer_numbers)
    # print("raw_log_answer_numbers----------------------------->", raw_log_answer_numbers)
    print("raw_follower_counts-------------------------------->", raw_follower_counts)
    print("raw_view_counts------------------------------------>", raw_view_counts)

    document = {
        "Question"      :  raw_question,
        "Question_URL"  : raw_question_url,
        "Categories"    : raw_category_item,
        "Number_Ans_Official"    : raw_off_answer_numbers,
        "Number_Foll"   : raw_follower_counts,
        "Number_View"   : raw_view_counts
    }

    print(document)

    writer.writerow(document)
    # except:
    #     return

# https://www.quora.com/topic/Accounting/all_questions
#set selenium driver
path = "driver\\chromedriver.exe"
driver = Chrome(executable_path=path)
driver.get("https://www.quora.com/topic/Accounting/all_questions")
# driver.get("hhttps://www.quora.com/topic/Investing/all_questions")
time.sleep(2)

driver1 = Chrome(executable_path=path)
time.sleep(3)

# maximize browser
driver.maximize_window()
driver1.maximize_window()
time.sleep(2)

csvfile = open("quora_business.csv", "wb")
fieldnames = ["Question", "Question_URL", "Categories", "Number_Ans_Official", "Number_Foll", "Number_View"]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
writer.writeheader()

parse_page(driver.page_source, driver, driver1)