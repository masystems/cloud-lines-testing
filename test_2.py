from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from configparser import ConfigParser
import csv

class CloudLinesTestV2():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.cfg')
        self.username = self.config['settings']['username']
        self.password = self.config['settings']['password']
        self.browser = webdriver.Chrome(self.config['settings']['driverpath'])
        self.browser.get(self.config['settings']['domain'])
        self.timeout = 0
        self.pedigree = None
        self.breeder = None
        self.breed = None
        self.user = None

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
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue In opening pedigree search try later ",e,"at",counter,"insertion")
                        exit(0)



            # go to add new pedigree
            while self.timeout<20:
                try:
                    new_pedigree = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/new_pedigree/' + '"]')
                    self.browser.execute_script("arguments[0].click();", new_pedigree)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new pedigree try later",e,"at",counter,"insertion")
                        exit(0)

            # open add new breeder modal
            while self.timeout<20:
                try:
                    new_breeder_modal = self.browser.find_element_by_id('showNewBreederModal')
                    self.browser.execute_script("arguments[0].click();", new_breeder_modal)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new breeder model try later",e,"at",counter,"insertion")
                        exit(0)


            # Enter breeder information
            while self.timeout<20:
                try:
                    self.add_breeder_info(self.breeder)
                    submit_breeder = self.browser.find_element_by_id('saveBreeder')
                    self.browser.execute_script("arguments[0].click();", submit_breeder)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in saving breeder info try later",e,"at",counter,"insertion")
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
                        sleep(2)
                        self.add_breed_info(self.breed)
                        submit_breed = self.browser.find_element_by_id('saveBreed')
                        self.browser.execute_script("arguments[0].click();", submit_breed)
                        sleep(2)
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
                    confirm_save_pedigree = self.browser.find_element_by_name('confirmSaveBtn')
                    self.browser.execute_script("arguments[0].click();", confirm_save_pedigree)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in entering pedigree information try later",e,"at",counter,"insertion")
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
                sleep(2)
                self.timeout = 0
                break
            except Exception as e:
                self.timeout += 1
                if self.timeout == 20:
                    print("Server Issue in adding breeder info try later",e,"at breeder prefix",breeder['breeding_prefix'])
                    exit(0)

    def add_breed_info(self, breed):
        # Enter breed information
        while self.timeout < 20:
            try:
                breed_name = self.browser.find_element_by_name('breed_name')
                breed_name.send_keys(breed['breed_name'])
                desc = self.browser.find_element_by_name('breed_description')
                desc.send_keys(breed['desc'])
                sleep(2)
                self.timeout = 0
                break
            except Exception as e:
                self.timeout += 1
                if self.timeout == 20:
                    print("Server Issue in adding breed info try later",e," at breed name",breed['breed_name'])
                    exit(0)

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
        sleep(2)
        confirm_delete_pedigree = self.browser.find_element_by_name('delete')
        self.browser.execute_script("arguments[0].click();", confirm_delete_pedigree)
        sleep(2)

    def delete_all_breeders(self,prefix=""):
        # go to breed page
        self.login()
        breeders_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeders/' + '"]')
        self.browser.execute_script("arguments[0].click();", breeders_link)
        while True:
            breeders_filter = self.browser.find_element_by_xpath('//div[@id="table_filter"]/label/input[1]')
            breeders_filter.send_keys(prefix)
            try:
                edit_breeders_row = self.browser.find_element_by_class_name('odd')
                self.browser.execute_script("arguments[0].click();", edit_breeders_row)
                while self.timeout < 20:
                    try:
                        edit_breeders = self.browser.find_element_by_id('editBreeder')
                        self.browser.execute_script("arguments[0].click();",edit_breeders)
                        sleep(2)
                        delete_breeders_but = self.browser.find_element_by_id('deleteBreeder')
                        self.browser.execute_script("arguments[0].click();", delete_breeders_but)
                        confirm_delete_breeder = self.browser.find_element_by_name('delete')
                        self.browser.execute_script("arguments[0].click();", confirm_delete_breeder)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Server Issue in adding breed info try later", e)
                            exit(0)
            except:
                print("All Breeders Deleted ")
                return
    def delete_all_breeds(self):
        # go to breed page
        self.login()
        breed_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeds/' + '"]')
        self.browser.execute_script("arguments[0].click();", breed_link)
        try:
            while self.browser.find_element_by_class_name('btn-outline-info'):
                edit_breed_links = self.browser.find_elements_by_class_name('btn-outline-info')
                self.browser.execute_script("arguments[0].click();", edit_breed_links[0])
                self.delete_breed()
                breed_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeds/' + '"]')
                self.browser.execute_script("arguments[0].click();", breed_link)
        except NoSuchElementException:
            # all breeds deleted
            pass



    def delete_breed(self):
        # ensure you're on the right(edit_breed) page before calling this method
        delete_breed = self.browser.find_element_by_id('deleteBreed')
        self.browser.execute_script("arguments[0].click();", delete_breed)
        sleep(2)
        confirm_delete_breed = self.browser.find_element_by_name('delete')
        self.browser.execute_script("arguments[0].click();", confirm_delete_breed)
        sleep(2)


    def add_user(self,user_file):
        self.login()
        self.browser.get(self.config['settings']['domain']+"/account/settings")
        sleep(2)
        user_reader = csv.DictReader(open(user_file, newline=''))
        for counter in range(2):
            while self.timeout < 20:
                try:
                    self.user = dict(user_reader.__next__())
                    users_link = self.browser.find_element_by_xpath('//a[@href="' + '#users' + '"]')
                    self.browser.execute_script("arguments[0].click();", users_link)
                    create_new = self.browser.find_element_by_id('createNew')
                    self.browser.execute_script("arguments[0].click();", create_new)
                    sleep(2)
                    fname = self.browser.find_element_by_id('firstName')
                    fname.send_keys(self.user['first_name'])
                    lname = self.browser.find_element_by_id('lastName')
                    lname.send_keys(self.user['second_name'])
                    uname = self.browser.find_element_by_id('register-form-username')
                    uname.send_keys(self.user['username'])
                    email = self.browser.find_element_by_id('register-form-email')
                    email.send_keys(self.user['email'])
                    modal_save = self.browser.find_elements_by_id('userFormBtn')
                    self.browser.execute_script("arguments[0].click();", modal_save[0])
                    sleep(5)
                    self.timeout = 0
                    break
                except NoSuchElementException as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new user try later",e)
                        exit(0)
    def delete_users(self,idx = 1):
        self.login()
        self.browser.get(self.config['settings']['domain'] + "/account/settings")
        sleep(2)
        while True:
            try:
                users_link = self.browser.find_element_by_xpath('//a[@href="' + '#users' + '"]')
                self.browser.execute_script("arguments[0].click();", users_link)
                delete_btns = self.browser.find_elements_by_xpath('//*[@id="'+'userDeleteBtn'+'"]')
                self.browser.execute_script("arguments[0].click();", delete_btns[idx])
                sleep(2)
                confirm_delete = self.browser.find_element_by_id('userDelete')
                self.browser.execute_script("arguments[0].click();", confirm_delete)
                sleep(3)
            except:
                break

    def edit_parent_titles(self,mother="Mother",father="Father"):
        self.login()
        self.browser.get(self.config['settings']['domain'] + "/account/settings")
        sleep(2)
        customisation_link = self.browser.find_element_by_xpath('//a[@href="' + '#customisation' + '"]')
        self.browser.execute_script("arguments[0].click();", customisation_link)
        mom = self.browser.find_element_by_id('mother')
        mom.clear()
        mom.send_keys(mother)
        dad = self.browser.find_element_by_id('father')
        dad.clear()
        dad.send_keys(father)
        confirm_update = self.browser.find_element_by_id('selectTitleSettings')
        self.browser.execute_script("arguments[0].click();", confirm_update)

    def test(self,type,option=""):
        if type == 'login':
            self.login()
        elif type == 'add_pedigree':
            self.add_pedigree('pedigree.csv','breed.csv','breeder.csv')
        elif type == 'delete_all_pedigree':
            self.delete_all_pedigrees()
        elif type == 'delete_all_breeders':
            self.delete_all_breeders(option)
        elif type == 'delete_all_breeds':
            self.delete_all_breeds()
        elif type == "add_users":
            self.add_user('user.csv')
        elif type == 'delete_users':
            self.delete_users(int(input("Enter the index from which you want to start deleting")))
        elif type == 'update_parent_titles':
            self.edit_parent_titles(input("Enter Mother Title "),input("Enter Father Title "))


if __name__ == '__main__':
    obj = CloudLinesTestV2()
    obj.test('update_parent_titles')
    # print ("1. Test Login")
    # print ("2. Add Pedigree")
    # print ("3. Delete All Pedigrees")
    # print ("4. Delete All Breeders")
    # print ("5. Add Users")
    # print ("6. Delete Users")
    # print ("7. Edit Parent Titles")
    # print ("_. Exit")
    # ch = input("Enter Choice")
    # while ch != '_':
    #     if ch == "1":
    #         obj.test('login')
    #     elif ch == "2":
    #         obj.test('add_pedigree')
    #     elif ch == "3":
    #         obj.test('delete_all_pedigrees')
    #     elif ch == "4":
    #         obj.test('delete_all_breeders',input("Enter Breeder Prefix"))
    #     elif ch == "5":
    #         obj.test('add_users')
    #     elif ch == "6":
    #         obj.test('delete_users')
    #     elif ch == "7":
    #         obj.test('update_parent_titles')
    #     ch = input("Enter Choice")