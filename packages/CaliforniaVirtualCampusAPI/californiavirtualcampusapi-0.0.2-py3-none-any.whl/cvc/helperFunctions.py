import time
import requests
from bs4 import BeautifulSoup, Tag

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

import re
import json

from .course import course
from .courseSection import courseSection

from .sharedVariables import _getGreatestMatching

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com", 
    "Accept": "text/html,application/xhtml+xml",
}

def _getPageContentFromID(id:int):
    url = f'https://search.cvc.edu/courses/{id}'
    # Send GET request to the URL
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError("Inputted ID is invalid.", id)
        return ""

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup == None:
        raise ValueError("Inputted ID is invalid.", id)
        return ""
    return soup

def _parseCourse(soup,id:int):
    table = soup.find('div', attrs = {'class':'font-semibold text-sm md:text-base'})
    try:
        college_name_text = table.get_text(strip=True).strip()
    except (TypeError, AttributeError, ValueError) as e:
        college_name_text = ""
    #print(college_name_text)

    table = soup.find('h1', attrs = {'class':'text-2xl lg:text-3xl font-semibold sm:flex-grow-0 w-full'}) 
    try:
        class_name_text = table.get_text(strip=True)
        index = class_name_text.index('-')
        class_symbol = class_name_text[:index-1].strip()
        class_name_text = class_name_text[index+2:].strip()
        #print(class_symbol)
        #print(class_name_text)
    except (TypeError, AttributeError, ValueError) as e:
        class_name_text = ""
    
    table = soup.find('span', attrs = {'data-tooltip-title-value':'This is the CCC Course Identification Numbering System.'}) 
    try:
        C_ID = table.get_text(strip=True).strip()
        #print("C_ID: "+C_ID)
    except (TypeError, AttributeError, ValueError) as e:
        C_ID = ""
    
    table = soup.find('h2', string='Location',attrs={'class':'font-semibold text-sm mb-1 uppercase text-c_content_text_highlight'})
    table = table.find_next_siblings()[0]
    locationText = table.get_text(strip=True)

    table = soup.find('h2', string='Units',attrs={'class':'font-semibold text-sm mb-1 uppercase text-c_content_text_highlight'})
    table = table.find_next_siblings()[0]
    unitText = table.get_text(strip=True)
    if unitText:
        match = re.search(r'(\d+(\.\d+)?)\s+(semester|quarter)', unitText, re.IGNORECASE)
        if match:
            units = match.group(1)                  # i.e. "4.0"
            termType = match.group(3).capitalize()  # i.e. "semester"
        else:
            units = unitText
            termType = unitText
    else:
        units = ""
        termType = ""

    table = soup.find('div', attrs = {'class':'course-description pb-2'}) 
    coureDescriptionText = table.get_text(strip=True)
    match = re.search(r'(Prerequisite:.*?(\.|\n))', coureDescriptionText)
    prereqs = []
    if match:
        prerequisite = match.group(1)  # Store the matched sentence
        prereqs = prerequisite.replace(",", "").replace(".", "").replace("and","").replace("or","").replace("-", " ").replace("Prerequisites:","").replace("Prerequisite:","")
        prereqs = prereqs.split("  ")
        coureDescriptionText = table.get_text(strip=True).replace(prerequisite, '').strip()  # Remove it from the text
    else:
        prereqs = []
    # try:
    #     course_description = table.get_text(separator=' ',strip=True)
    # except (TypeError, AttributeError, ValueError) as e:
    #     print(e)
    #     course_description = ""
    # try:
    #     index = course_description.index('Prerequisite:')
    #     if index > -1:
    #         course_description = course_description[:index]
    #     prereqs = course_description[index+len("Prerequisite:")+1:]
    #     index = prereqs.index('all with')
    #     prereqs = prereqs[:index].replace(",", "").replace(".", "").replace("and","").replace("or","").replace("-", " ")
    #     prereqs = prereqs.split("  ")
    #     for i in range(0,len(prereqs)):
    #         prereqs[i] = prereqs[i].strip()
    #     #print(course_description)
    #     #print(prereqs)
    # except (TypeError, AttributeError, ValueError) as e:
    #     prereqs = []
    return course(id, college_name_text,class_name_text,class_symbol,C_ID,coureDescriptionText,locationText, units, termType,prereqs,_parseSections(soup))

def _parseSections(soup):
    table = soup.find('h3', attrs={'class':'font-semibold mb-4 border-b-2 border-c_content_text_highlight pb-2'})
    currentSem = None
    sections = []
    if table == None:
        return []
    for sem in table.parent:
        semester_text = sem.get_text(strip=True).strip()
        if(len(semester_text.replace(" ",""))==0):
            continue
        if(" - Semester" in semester_text):
            index = semester_text.index(' - Semester')
            semester_text = semester_text[:index]
            currentSem = semester_text
            continue
        if isinstance(sem, Tag):
            while True:
                section_id = sem.find('span', attrs={'class': 'text-sm font-medium section-details-crn'})
                sectionIdText = ""
                if section_id:
                    sectionIdText = section_id.get_text(strip=True)
                    section_id.extract()
                else:
                    break
                duration = sem.find('div', attrs={'class': 'w-full sm:w-auto font-semibold text-c_content_text_highlight section-details-date'})
                durationText = duration.get_text(strip=True)
                duration.extract()

                format = sem.find('button', attrs={'class': 'text-sm font-medium'})
                formatText = format.get_text(strip=True)
                format.extract()

                time = sem.find('span', text='Time:',attrs={'class': 'font-semibold text-c_content_text_highlight text-xs mr-1'})
                neighbors = list(time.find_next_siblings())
                times = []
                
                for n in neighbors:
                    if n.name == 'ul':
                        li_items = n.find_all('li', recursive=False)
                        for li in li_items:
                            times.append(li.get_text(strip=True))
                        continue
                    times.append(n.get_text(strip=True))
                if time:
                    time.extract()
                
                prof = sem.find('span', attrs={'class': 'text-xs font-medium section-details-professor'})
                profText = prof.get_text(strip=True)
                prof.extract()

                seatCount = sem.find('span', attrs={'class': 'seat-count-live seat-count'})
                seatCountText = seatCount.get_text(strip=True)
                seatCount.extract()
                index = seatCountText.index("available")
                seatCountText = seatCountText[:index]

                sectionNotes = sem.find('div', attrs={'class': 'text-xs section-details-notes'})
                sectionNotesText = sectionNotes.get_text(separator=' ',strip=True)
                sectionNotes.extract()

                tuition = sem.find('span', attrs={'class': 'font-semibold text-lg text-c_link'})
                tuitionText = tuition.get_text(strip=True)
                tuition.extract()
                index = tuitionText.index(":")
                tuitionText = tuitionText[index+2:]

                zeroTextbookCost = False
                zeroTextbookCostItem = sem.find('span', attrs={'data-tooltip-title-value': 'Zero Textbook Cost courses have no textbook-related costs or access fees for online materials.'})
                if zeroTextbookCostItem:
                    zeroTextbookCost = True
                    zeroTextbookCostItem.extract()
                
                registration = ""
                startingDate = sem.find('span', text=' Already Started ',attrs={'class': 'text-sm font-semibold'})
                if startingDate:
                    registration = "Already Open"
                else:    
                    startingDate = sem.find('span',attrs={'class': 'text-sm font-semibold'})
                    if startingDate != None:
                        startingDate = startingDate.find('span', attrs={'class':'text-c_content_text_highlight'})
                        if startingDate != None:
                            registration = startingDate.get_text(strip=True).replace(" Registration Opens ","")


                foundSection = courseSection(currentSem,durationText,sectionIdText,formatText,zeroTextbookCost,times,profText,seatCountText,tuitionText,registration,sectionNotesText)
                #foundSection.printAll()
                sections.append(foundSection)
    return sections

def _getCourseContentByID(id:int):
    soup = _getPageContentFromID(id)
    return _parseCourse(soup,id)

def _getCourseIDsByLandingPage(collegeName:str, C_ID:str, courseSymbol:str, courseName:str):
    maxScore = 0
    if C_ID != "":
        maxScore+=1
        C_ID = C_ID.lower().strip()
    if courseSymbol != "":
        maxScore += 1
        courseSymbol = courseSymbol.lower().strip()
    if courseName != "":
        maxScore += 1
        courseName = courseName.lower().strip()
    driver = _getDriver()
    driver.get('https://search.cvc.edu/embedded_search') 

    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script('return window.jQuery && jQuery.active == 0')
    )
    # with open("page_source.html", "w", encoding="utf-8") as file:
    #     file.write(driver.page_source)    
    radio_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "filter[search_all_universities]"))
    )
    input_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "filter_university_id-selectized"))
    )
    input_box.send_keys(collegeName, Keys.RETURN)

    HomeCollegeText = driver.find_element(By.XPATH, "//span[text()='Home College Course Name']").find_element(By.XPATH, '..').find_element(By.XPATH, ".//input[@id='filter_search_type_course']")
    actions = ActionChains(driver)
    actions.move_to_element(HomeCollegeText).click().perform()
    HomeCollegeText.click()

    input_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "filter_query-selectized"))
    )
    # print((courseSymbol + " " + "(C-ID: "+C_ID + ") " + courseName).strip())
    input_box.send_keys((courseSymbol + " " + C_ID + " " + courseName).strip())
    time.sleep(1)
    input_box.send_keys(Keys.RETURN)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    courses = soup.find_all('div', attrs={'class':'option'})
    courseIDs = []
    for course in courses:
        score = 0
        if("course-" not in course.get('id')):
            continue
        courseID = course.get('id').replace("course-","")
        result = course.get_text().lower()
        result = result.replace(" Show substitutes for ","")
        result = result.strip()
        if C_ID != "":
            match = re.search(r"\((.*?)\)", result)
            if match:
                foundC_ID = match.group(1)
                foundC_ID = foundC_ID.replace("(C-ID: ","").replace(")","").lower().strip()
                if C_ID in foundC_ID:
                    score += 1
        if maxScore == score:
            courseIDs.append(courseID)
            continue
        result = re.sub(r"\(.*?\)", "", result)

        if courseSymbol != "":
            if courseSymbol in result:
                result = result.replace(courseSymbol, "")
                score +=1
        if maxScore == score:
            courseIDs.append(courseID)
            continue
        
        if courseName != "":
            if courseName in result:
                score +=1
        if maxScore == score:
            courseIDs.append(courseID)
            continue
    if len(courseIDs) > 0:
        return courseIDs
    else:
        print("No course could be found with these parameters.")
        return []
    driver.quit()

def _getDriver():
    """
    Creates a webdriver to be used with Selenium to scrape a page. So far used in _getCourseIDsByLandingPage.

    Returns:
    webdriver: A Chrome browser which will handle automated interaction.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppresses INFO and WARNING
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.set_capability("browserVersion", "117")
    driver = webdriver.Chrome(options=options) #service=Service(ChromeDriverManager().install())
    return driver

def _getCourseIDsBySearch(collegeName:str, C_ID:str, courseSymbol:str, courseName:str):
    #https://search.cvc.edu/api/search.json?query=cd&university_id=48&only_visible=true
    #https://search.cvc.edu/api/search.json?query=cs&university_id=48&only_visible=true
    #https://search.cvc.edu/api/search.json?query=fun%20stuff&university_id=48&only_visible=true
    url = f'https://search.cvc.edu/api/search.json?query={(courseSymbol + " " + C_ID + " " + courseName).strip()}&university_id={_getGreatestMatching(collegeName)}&only_visible=false'
    # Send GET request to the URL
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError("No course could be found. Status code:", response.status_code)
        return []
    data = response.json()
    data = data['results']
    courseIDs = []
    for course in data:
        courseIDs.append(course['id'].replace("course-",""))
    return courseIDs
