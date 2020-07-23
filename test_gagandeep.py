from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import sys
import csv
"""
drv = webdriver.Firefox("D:/PyCharmProjects/MaSystems/")
drv.maximize_window()
"""
class CloudLinesTestV2():
    def __init__(self):
        self.browser = webdriver.Chrome("D:/PyCharmProjects/MaSystems/chromedriver.exe")
        self.browser.get('https://dev.cloud-lines.com')
        self.username = sys.argv[1]
        self.password = sys.argv[2]
        self.pedigree = None
        self.breeder = None
        self.breed = None

    def login(self):
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password)
        login = self.browser.find_element_by_id('loginBtn')
        self.browser.execute_script("arguments[0].click();", login)
        sleep(2)

    def add_pedigree(self,pedigree_file,breed_file,breeder_file):
        self.login()
        pedgree_reader = csv.DictReader(open(pedigree_file,newline=''))
        breeder_reader = csv.DictReader(open(breeder_file,newline=''))
        breed_reader = csv.DictReader(open(breed_file,newline=''))

        for _ in range(12):
            self.pedigree = dict(pedgree_reader.__next__())
            self.breeder = dict(breeder_reader.__next__())
            self.breed = dict(breed_reader.__next__())

            # go to pedigree search page
            pedigree_link = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/search' + '"]')
            self.browser.execute_script("arguments[0].click();", pedigree_link)

            # go to add new pedigree
            new_pedigree = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/new_pedigree/' + '"]')
            self.browser.execute_script("arguments[0].click();", new_pedigree)
            sleep(1)

            # open add new breeder modal
            new_breeder_modal = self.browser.find_element_by_id('showNewBreederModal')
            self.browser.execute_script("arguments[0].click();", new_breeder_modal)
            sleep(1)

            # Enter breeder information
            self.add_breeder_info(self.breeder)
            submit_breeder = self.browser.find_element_by_id('saveBreeder')
            self.browser.execute_script("arguments[0].click();", submit_breeder)
            sleep(3)

            # Enter pedigree information
            breeder = self.browser.find_element_by_id('id_breeder')
            breeder.send_keys(self.pedigree['breeder'])
            current_owner = self.browser.find_element_by_id('id_current_owner')
            current_owner.send_keys(self.pedigree['breeder'])
            self.browser.find_element_by_name('reg_no').clear()
            reg_no = self.browser.find_element_by_name('reg_no')
            reg_no.send_keys(self.pedigree['reg_no'])
            tag_no = self.browser.find_element_by_id('id_tag_no')
            tag_no.send_keys(self.pedigree['tag_no'])
            name = self.browser.find_element_by_id('id_name')
            name.send_keys(self.pedigree['name'])
            dor = self.browser.find_element_by_id('id_date_of_registration')
            dor.send_keys(self.pedigree['dor'])
            dob = self.browser.find_element_by_id('id_date_of_birth')
            dob.send_keys(self.pedigree['dob'])
            status = self.browser.find_element_by_id(self.pedigree['status'])
            self.browser.execute_script("arguments[0].click();", status)
            sex = self.browser.find_element_by_id(self.pedigree['sex'])
            self.browser.execute_script("arguments[0].click();", sex)
            dod = self.browser.find_element_by_id('id_date_of_death')
            dod.send_keys(self.pedigree['dod'])
            desc = self.browser.find_element_by_id('id_description')
            desc.send_keys(self.pedigree['desc'])

            if _ == 0:
                # open add new breed modal
                new_breed_modal = self.browser.find_element_by_id('showNewBreedModal')
                self.browser.execute_script("arguments[0].click();", new_breed_modal)
                # Enter breeder information
                sleep(1)
                self.add_breed_info(self.breed)
                submit_breed = self.browser.find_element_by_id('saveBreed')
                self.browser.execute_script("arguments[0].click();", submit_breed)
                sleep(1)
            else:
                try:
                    breed = self.browser.find_element_by_id('id_breed')
                    breed.send_keys(self.pedigree['breed'])
                except ElementNotInteractableException:
                    # means only one breed can be added to it's greyed out
                    pass

            # Save!
            save_pedigree = self.browser.find_element_by_id('submitPedigree')
            self.browser.execute_script("arguments[0].click();", save_pedigree)

    def add_breeder_info(self,breeder):
        # Enter breeder information
        breeding_prefix = self.browser.find_element_by_name('breeding_prefix')
        breeding_prefix.send_keys(breeder['breeding_prefix'])
        contact_name = self.browser.find_element_by_name('contact_name')
        contact_name.send_keys(breeder['contact_name'])
        address = self.browser.find_element_by_name('address')
        address.send_keys(breeder['address'])
        phone_number1 = self.browser.find_element_by_name('phone_number1')
        phone_number1.send_keys(breeder['phone_number1'])
        phone_number2 = self.browser.find_element_by_name('phone_number2')
        phone_number2.send_keys(breeder['phone_number2'])
        email = self.browser.find_element_by_name('email')
        email.send_keys(breeder['email'])
        active = self.browser.find_element_by_name('active')
        self.browser.execute_script("arguments[0].click();", active)

    def add_breed_info(self, breed):
        # Enter breed information
        breed_name = self.browser.find_element_by_name('breed_name')
        breed_name.send_keys(breed['breed_name'])
        desc = self.browser.find_element_by_name('breed_description')
        desc.send_keys(breed['desc'])

    def test(self,type):
        if type == 'login':
            self.login()
        if type == 'add_pedigree':
            self.add_pedigree('pedigree.csv','breed.csv','breeder.csv')

if __name__ == '__main__':
    obj = CloudLinesTestV2()
    print ("1. Test Login")
    print ("2. Add Pedigree")
    print ("_. Exit")
    ch = input("Enter Choice")
    while ch != '_':
        if ch == "1":
            obj.test('login')
        elif ch == "2":
            obj.test('add_pedigree')
        ch = input("Enter Choice")


