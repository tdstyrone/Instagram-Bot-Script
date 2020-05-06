from selenium import webdriver
from time import sleep


class InstaBot:

    def __init__(self, username, password):
        self.username = username

        # Opens Instagram Website
        self.driver = webdriver.Chrome('chromedriver.exe')#Insert path to chromedriver on Mac
        self.driver.get('https://www.instagram.com/')
        sleep(4)

        # Login
        self.driver.find_element_by_name("username")\
            .send_keys(username)
        self.driver.find_element_by_name("password")\
            .send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]') \
            .click()
        sleep(5)

        # Close Notification Pop-up
        self.driver.find_element_by_xpath('//button[contains(text(),"Not Now")]') \
            .click()
        sleep(2)

    # Gets the users who don't follow back and prints them to the screen
    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)) \
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]") \
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]") \
            .click()
        followers = self._get_names()
        not_following_back = [names for names in following if names not in followers]
        print(f"\nNumber of people that are not following you back: {len(not_following_back)}")
        print("The users that are not following you back are: ")
        for users in not_following_back:
            print(users)

    # Gets usernames and store them in array
    def _get_names(self):
        sleep(4)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_height, current_height = 0, 1
        while last_height != current_height:
            last_height = current_height
            sleep(2)
            current_height = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;""", scroll_box)
        name_links = scroll_box.find_elements_by_tag_name('a')
        name_array = [name.text for name in name_links if name.text != '']
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
            .click()
        return name_array

def main():
    print("Instagram Bot - Program Started\n")

    # Variables for Login
    instagram_username = input("Enter your Username/Email/Phone Number: ")
    instagram_password = input("Enter your password: ")

    # Instance of instgram bot
    user_bot = InstaBot(instagram_username, instagram_password)
    user_bot.get_unfollowers()
pass

main()
