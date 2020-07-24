from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import csv

class CloudLinesTestV2():
    def __init__(self):
        f = open(".gitignore")
        self.username = f.readline().rstrip("\n")
        self.password = f.readline().rstrip("\n")
        self.browser = webdriver.Chrome(f.readline().rstrip("\n"))
        self.browser.get(f.readline().rstrip("\n"))
        self.timeout = 0
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

        for counter in range(12):
            self.pedigree = dict(pedgree_reader.__next__())
            self.breeder = dict(breeder_reader.__next__())
            self.breed = dict(breed_reader.__next__())

            # go to pedigree search page
            while self.timeout<20:
                try:
                    pedigree_link = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/search' + '"]')
                    self.browser.execute_script("arguments[0].click();", pedigree_link)
                    sleep(1)
                    self.timeout = 0
                    break
                except:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue In opening pedigree search try later ")
                        exit(0)



            # go to add new pedigree
            while self.timeout<20:
                try:
                    new_pedigree = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/new_pedigree/' + '"]')
                    self.browser.execute_script("arguments[0].click();", new_pedigree)
                    sleep(1)
                    self.timeout = 0
                    break
                except:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new pedigree try later")
                        exit(0)

            # open add new breeder modal
            while self.timeout<20:
                try:
                    new_breeder_modal = self.browser.find_element_by_id('showNewBreederModal')
                    self.browser.execute_script("arguments[0].click();", new_breeder_modal)
                    sleep(1)
                    self.timeout = 0
                    break
                except:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new breeder model try later")
                        exit(0)


            # Enter breeder information
            while self.timeout<20:
                try:
                    self.add_breeder_info(self.breeder)
                    submit_breeder = self.browser.find_element_by_id('saveBreeder')
                    self.browser.execute_script("arguments[0].click();", submit_breeder)
                    sleep(1)
                    self.timeout = 0
                    break
                except:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in saving breeder info try later")
                        exit(0)

            # Enter pedigree information
            while self.timeout<20:
                try:
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

                    if counter == 0:
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
                    sleep(1)
                    self.timeout = 0
                    break
                except:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in entering pedigree information try later")
                        exit(0)

    def add_breeder_info(self,breeder):
        # Enter breeder information
        while self.timeout < 20:
            try:
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
                sleep(1)
                self.timeout = 0
                break
            except:
                self.timeout += 1
                if self.timeout == 20:
                    print("Server Issue in adding breeder info try later")
                    exit(0)

    def add_breed_info(self, breed):
        # Enter breed information
        breed_name = self.browser.find_element_by_name('breed_name')
        breed_name.send_keys(breed['breed_name'])
        desc = self.browser.find_element_by_name('breed_description')
        desc.send_keys(breed['desc'])

    def delete_all_pedigrees(self):
        # go to pedigree search page
        pedigree_link = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/search' + '"]')
        self.browser.execute_script("arguments[0].click();", pedigree_link)

        while self.browser.find_elements_by_class_name('sorting_1'):
            pedigree_links = self.browser.find_elements_by_class_name('sorting_1')
            self.browser.execute_script("arguments[0].click();", pedigree_links[0])
            self.delete_pedigree()
            pedigree_link = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/search' + '"]')
            self.browser.execute_script("arguments[0].click();", pedigree_link)

    def delete_pedigree(self):
        # ensure you're on the right page before calling this method
        edit_pedigree = self.browser.find_element_by_id('editPedigree')
        self.browser.execute_script("arguments[0].click();", edit_pedigree)
        delete_pedigree = self.browser.find_element_by_id('deletePedigree')
        self.browser.execute_script("arguments[0].click();", delete_pedigree)
        sleep(1)
        confirm_delete_pedigree = self.browser.find_element_by_name('delete')
        self.browser.execute_script("arguments[0].click();", confirm_delete_pedigree)
        sleep(1)

    def test(self,type):
        if type == 'login':
            self.login()
        if type == 'add_pedigree':
            self.add_pedigree('pedigree.csv','breed.csv','breeder.csv')
        if type == 'delete_all_pedigree':
            self.delete_all_pedigrees()

if __name__ == '__main__':
    obj = CloudLinesTestV2()
    print ("1. Test Login")
    print ("2. Add Pedigree")
    print ("3. Delete All Pedigrees")
    print ("_. Exit")
    ch = input("Enter Choice")
    while ch != '_':
        if ch == "1":
            obj.test('login')
        elif ch == "2":
            obj.test('add_pedigree')
        elif ch == "3":
            obj.delete_all_pedigrees()
        ch = input("Enter Choice")


