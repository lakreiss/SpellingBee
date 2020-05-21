from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele
        str1 += "\n"

    # return string
    return str1

def dictToString(d):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in d.keys():
        str1 += ele
        str1 += " : "
        str1 += d[ele]
        str1 += "\n"

    # return string
    return str1

class SpellingBeeBot():
    def __init__(self):

        self.driver = webdriver.Chrome()
        sleep(1)
        # self.driver.set_window_size(1024, 600)
        # self.driver.maximize_window()

    def get_letters_from_nyt(self):
        self.driver.get('https://www.nytimes.com/puzzles/spelling-bee')

        #click play button
        self.driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button').click()
        sleep(1)

        letter_string = ""
        #get each letter, add to letter_string
        for cell_letter in self.driver.find_elements_by_class_name('cell-letter'):
            letter_string += cell_letter.get_attribute('innerHTML')

        return letter_string

    def get_all_words(self, letters):
        self.driver.get('https://liamkreiss.me/html/spelling_bee.html' + "#" + letters)
        sleep(5)

        #click solve button
        self.driver.find_element_by_xpath('//*[@id="solve_button"]').click()
        sleep(0.5)

        all_words = []
        for i in range(3):
            cur_col = self.driver.find_element_by_xpath('//*[@id="all_words_col' + str(i) + '"]')
            cur_words = cur_col.get_attribute('innerHTML').split("<br>")
            all_words.extend(cur_words)

        # print(all_words)
        return all_words

    def enter_all_words(self, all_words):
        self.driver.get('https://www.nytimes.com/puzzles/spelling-bee')

        #sign in
        self.driver.find_element_by_xpath('//*[@id="js-global-nav"]/div[3]/a[2]').click()
        sleep(1)

        try:
            print("found it")
            self.driver.find_element_by_xpath('//*[@id="email"]').send_keys('liam98765228@berkeley.edu')
            self.driver.find_element_by_xpath('//*[@id="myAccountAuth"]/div[1]/div/form/div/div[2]/button').click()
            self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('*')

        except NoSuchElementException:
            print("didn't find it")
            self.driver.find_element_by_xpath('//*[@id="username"]').send_keys('liam98765228@berkeley.edu')
            self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('*')
            sleep(1)

            self.driver.find_element_by_css_selector('#myAccountAuth > div.css-1xd1ug7-Container.edabiy60 > div > form > div > div.css-1696vl4-buttonWrapper-Button > button').click()



        #click play button
        # self.driver.find_element_by_xpath('//*[@id="portal-game-modals"]/div/div/div/div/div/div/div[3]/button').click()
        # sleep(1)
        #
        # for word in all_words:
        #     actions = ActionChains(self.driver)
        #     actions.send_keys(word)
        #     actions.send_keys(Keys.RETURN)
        #     actions.perform()

        # sleep(1)
        #
        # all_classes = []
        #
        # selections = self.driver.find_elements_by_class_name("VirtualizedSelectOption")
        # for element in selections:
        #     all_classes.append(element.get_attribute('innerHTML'))
        #
        # self.go_down(entry_box, 21)
        #
        # for i in range(30):
        #     selections = self.driver.find_elements_by_class_name("VirtualizedSelectOption")
        #     for element in selections:
        #         innerHTML = element.get_attribute('innerHTML')
        #         in_split = innerHTML.split(" ")
        #         if (in_split[1][0] == "W" and "WEL" not in in_split[1]):
        #             all_classes.append(innerHTML)
        #         else:
        #             print("didnt append", innerHTML)
        #     self.go_down(entry_box, 16)
        #
        # return all_classes

    def go_down(self, entry_box, n=10):
        for i in range(n):
            entry_box.send_keys(Keys.DOWN)

    def scroll_up(self, n=0):
        self.driver.execute_script("window.scrollTo(0," + str(n) + ")")


    def clear_entry(self, entry_box, word):
        for i in range(len(word)):
            entry_box.send_keys(Keys.BACKSPACE)

    def print_to_file(self, file_name, input):
        print(type(input))
        if isinstance(input,dict):
            f = open(file_name, "w")
            f.write(dictToString(input))
            f.close()
        elif isinstance(input,list):
            f = open(file_name, "w")
            f.write(listToString(input))
            f.close()

def find_invalid_words(words, valid_words):
    valid_words = [v_word.lower() for v_word in valid_words]
    for word in words:
        if word not in valid_words:
            print(word)

bot = SpellingBeeBot()
letters = bot.get_letters_from_nyt();
words = bot.get_all_words(letters);
words.sort()
print(words)

bot.enter_all_words(words) #NYT does a bot checker which keeps stumping me

# letters = "labcnoy"
# valid_words = ["Balcony", "Ably", "Allay", "Alloy", "Ally", "Anal", "Anally", "Annal", "Ball", "Ballboy", "Balloon", "Banal", "Banally", "Blab", "Blabby", "Blob", "Blobby", "Bloc", "Bola", "Boll", "Bolo", "Cabal", "Cabala", "Call", "Calla", "Callaloo", "Canal", "Cannonball", "Canola", "Clan", "Clay", "Cloaca", "Clonal", "Cloy", "Coal", "Cola", "Colcannon", "Colon", "Colony", "Cool", "Coolly", "Coyly", "Lacy", "Llano", "Loan", "Lobby", "Lobo", "Local", "Locally", "Loco", "Loll", "Loon", "Loony", "Loyal", "Loyally", "Nobly", "Nonlocal", "Nylon", "Onlay", "Only"]
