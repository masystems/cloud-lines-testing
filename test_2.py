from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from configparser import ConfigParser
import csv
from datetime import datetime

class CloudLinesTestV2():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.cfg')

        self.username_user = self.config['settings']['username_user']
        self.password_user = self.config['settings']['password_user']
        self.username_admin = self.config['settings']['username_admin']
        self.password_admin = self.config['settings']['password_admin']
        self.username_contrib = self.config['settings']['username_contrib']
        self.password_contrib = self.config['settings']['password_contrib']
        self.username_read = self.config['settings']['username_read']
        self.password_read = self.config['settings']['password_read']

        self.browser = webdriver.Chrome(self.config['settings']['driverpath'])
        self.browser.get(self.config['settings']['domain'])
        self.timeout = 0
        self.pedigree = None
        self.breeder = None
        self.breed = None
        self.user = None

        self.current_user_type = None

        # create csv results file
        self.results_file = f'results/results_{datetime.now()}.csv'
        with open(self.results_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Action", "User Type", "Scenario", "Result", "Description"])

    def login_user(self):
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username_user)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password_user)
        login = self.browser.find_element_by_id('loginBtn')
        self.browser.execute_script("arguments[0].click();", login)
        self.current_user_type = '_user'
        sleep(2)

    def login_admin(self):
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username_admin)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password_admin)
        login = self.browser.find_element_by_id('loginBtn')
        self.browser.execute_script("arguments[0].click();", login)
        self.current_user_type = '_admin'
        sleep(2)

    def login_contrib(self):
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username_contrib)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password_contrib)
        login = self.browser.find_element_by_id('loginBtn')
        self.browser.execute_script("arguments[0].click();", login)
        self.current_user_type = '_contrib'
        sleep(2)

    def login_read(self):
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username_read)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password_read)
        login = self.browser.find_element_by_id('loginBtn')
        self.browser.execute_script("arguments[0].click();", login)
        self.current_user_type = '_read'
        sleep(2)

    def logout(self):
        self.browser.get(self.config['settings']['domain'] + "/account/logout")
        self.current_user_type = None
        sleep(2)

    def add_pedigree(self,pedigree_file,breed_file,breeder_file):
        self.browser.get(self.config['settings']['domain'] + "/account/welcome")
        pedgree_reader = csv.DictReader(open(pedigree_file,newline=''))
        breeder_reader = csv.DictReader(open(breeder_file,newline=''))
        breed_reader = csv.DictReader(open(breed_file,newline=''))

        for counter in range(12):
            self.pedigree = dict(pedgree_reader.__next__())
            self.breeder = dict(breeder_reader.__next__())
            self.breed = dict(breed_reader.__next__())

            # go to pedigree search page
            while self.timeout < 20:
                try:
                    pedigree_link = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                    self.browser.execute_script("arguments[0].click();", pedigree_link)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue In opening pedigree search try later ", e,"at",counter,"insertion")
                        exit(0)



            # go to add new pedigree
            while self.timeout < 20:
                try:
                    new_pedigree = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                    self.browser.execute_script("arguments[0].click();", new_pedigree)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new pedigree try later", e,"at",counter,"insertion")
                        exit(0)

            # open add new breeder modal
            while self.timeout < 20:
                try:
                    new_breeder_modal = self.browser.find_element_by_id('showNewBreederModal')
                    self.browser.execute_script("arguments[0].click();", new_breeder_modal)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in adding new breeder model try later", e,"at",counter,"insertion")
                        exit(0)


            # Enter breeder information
            while self.timeout < 20:
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
                        print("Server Issue in saving breeder info try later", e,"at",counter,"insertion")
                        exit(0)

            # Enter pedigree information
            while self.timeout < 20:
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
                    born_as = self.browser.find_element_by_id(self.pedigree['born_as'])
                    self.browser.execute_script("arguments[0].click();", born_as)
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
                    confirm_save_pedigree = self.browser.find_element_by_id('confirmSaveBtn')
                    self.browser.execute_script("arguments[0].click();", confirm_save_pedigree)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        print("Server Issue in entering pedigree information try later", e,"at",counter,"insertion")
                        exit(0)
 
    def add_each_single_pedigree(self, pedigree_file):
        # add pedigree in all the different ways as each possible user
        self.add_single_pedigree(pedigree_file, '_user', '_pedigree_search')
        self.add_single_pedigree(pedigree_file, '_user', '_pedigree_view')
        self.add_single_pedigree(pedigree_file, '_user', '_offspring')
        self.add_single_pedigree(pedigree_file, '_user', '_certificate')
        self.add_single_pedigree(pedigree_file, '_user', '_results_from_peds')
        self.add_single_pedigree(pedigree_file, '_user', '_results_from_tool')
        self.add_single_pedigree(pedigree_file, '_admin', '_pedigree_search')
        self.add_single_pedigree(pedigree_file, '_admin', '_pedigree_view')
        self.add_single_pedigree(pedigree_file, '_admin', '_offspring')
        self.add_single_pedigree(pedigree_file, '_admin', '_certificate')
        self.add_single_pedigree(pedigree_file, '_admin', '_results_from_peds')
        self.add_single_pedigree(pedigree_file, '_admin', '_results_from_tool')
        self.add_single_pedigree(pedigree_file, '_contrib', '_pedigree_search')
        self.add_single_pedigree(pedigree_file, '_contrib', '_pedigree_view')
        self.add_single_pedigree(pedigree_file, '_contrib', '_offspring')
        self.add_single_pedigree(pedigree_file, '_contrib', '_certificate')
        self.add_single_pedigree(pedigree_file, '_contrib', '_results_from_peds')
        self.add_single_pedigree(pedigree_file, '_contrib', '_results_from_tool')
        self.add_single_pedigree(pedigree_file, '_read', '_pedigree_search')
        self.add_single_pedigree(pedigree_file, '_read', '_pedigree_view')
        self.add_single_pedigree(pedigree_file, '_read', '_offspring')
        self.add_single_pedigree(pedigree_file, '_read', '_certificate')
        self.add_single_pedigree(pedigree_file, '_read', '_results_from_peds')
        self.add_single_pedigree(pedigree_file, '_read', '_results_from_tool')

    def add_single_pedigree(self, pedigree_file, user_type, addition_method):
        # login as the correct user
        if self.current_user_type != user_type:
            # logout if we're logged in as wrong user
            if self.current_user_type:
                self.logout()
            # login as correct user
            if user_type == '_user':
                self.login_user()
            elif user_type == '_admin':
                self.login_admin()
            elif user_type == '_contrib':
                self.login_contrib()
            elif user_type == '_read':
                self.login_read()

        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # if user is not read-only, test adding a pedigree
        if user_type != '_read':
            pedgree_reader = csv.DictReader(open(pedigree_file,newline=''))
            self.pedigree = dict(pedgree_reader.__next__())

            # access new pedigree form via pedigree search
            if addition_method == '_pedigree_search':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to add new pedigree
                while self.timeout < 20:
                    try:
                        add_ped = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                        self.browser.execute_script("arguments[0].click();", add_ped)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open add pedigree form'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
            # access new pedigree form via view pedigree
            elif addition_method == '_pedigree_view':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        ped_view = self.browser.find_element_by_xpath('//button[contains(text(), "View")]')
                        self.browser.execute_script("arguments[0].click();", ped_view)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to add new pedigree
                while self.timeout < 20:
                    try:
                        add_ped = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                        self.browser.execute_script("arguments[0].click();", add_ped)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open new pedigree form'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
            # access new pedigree form via pedigree offspring
            elif addition_method == '_offspring':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Server Issue In opening pedigree search try later ", e)
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        ped_view = self.browser.find_element_by_xpath('//button[contains(text(), "View")]')
                        self.browser.execute_script("arguments[0].click();", ped_view)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Server Issue In opening pedigree view try later ", e)
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to offspring tab
                while self.timeout < 20:
                    try:
                        offspring = self.browser.find_element_by_xpath('//a[@href="#children"]')
                        self.browser.execute_script("arguments[0].click();", offspring)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open offspring tab'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to add new pedigree
                while self.timeout < 20:
                    try:
                        add_ped = self.browser.find_element_by_xpath('//div[@id="children"]/a[@href="/pedigree/new_pedigree/"]')
                        self.browser.execute_script("arguments[0].click();", add_ped)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open new pedigree form within offspring tab'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
            # access new pedigree form via pedigree certificate
            elif addition_method == '_certificate':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Server Issue In opening pedigree search try later ", e)
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        ped_view = self.browser.find_element_by_xpath('//button[contains(text(), "View")]')
                        self.browser.execute_script("arguments[0].click();", ped_view)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Server Issue In opening pedigree view try later ", e)
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to certificate tab
                while self.timeout < 20:
                    try:
                        certificate = self.browser.find_element_by_xpath('//a[@href="#cert"]')
                        self.browser.execute_script("arguments[0].click();", certificate)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to certificate tab'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to add new pedigree
                while self.timeout < 20:
                    try:
                        add_ped = self.browser.find_element_by_xpath('//div[@id="certificate"]/table/tbody/tr/td/a[@href="/pedigree/new_pedigree/"]')
                        self.browser.execute_script("arguments[0].click();", add_ped)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open new pedigree form'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
            # accessing new pedigree form via results page
            elif addition_method == '_results_from_peds':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control form-control-success"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # go to add new pedigree
                while self.timeout < 20:
                    try:
                        add_ped = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                        self.browser.execute_script("arguments[0].click();", add_ped)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open new pedigree form'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
            # accessing new pedigree form via results page
            elif addition_method == '_results_from_tool':
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # go to add new pedigree
                while self.timeout < 20:
                    try:
                        add_ped = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                        self.browser.execute_script("arguments[0].click();", add_ped)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Server Issue in adding new pedigree try later", e)
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open new pedigree form'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'

            # Enter pedigree information
            while self.timeout < 20:
                try:
                    breeder = self.browser.find_element_by_id('id_breeder')
                    breeder.send_keys(self.pedigree['breeder'])
                    current_owner = self.browser.find_element_by_id('id_current_owner')
                    current_owner.send_keys(self.pedigree['breeder'])
                    self.browser.find_element_by_name('reg_no').clear()
                    reg_no = self.browser.find_element_by_name('reg_no')
                    reg_no.send_keys(f"{self.pedigree['reg_no']}{user_type}{addition_method}")
                    tag_no = self.browser.find_element_by_id('id_tag_no')
                    tag_no.send_keys(self.pedigree['tag_no'])
                    name = self.browser.find_element_by_id('id_name')
                    name.send_keys(f"{self.pedigree['name']}{user_type}{addition_method}")
                    dor = self.browser.find_element_by_id('id_date_of_registration')
                    dor.send_keys(self.pedigree['dor'])
                    dob = self.browser.find_element_by_id('id_date_of_birth')
                    dob.send_keys(self.pedigree['dob'])
                    status = self.browser.find_element_by_id(self.pedigree['status'])
                    self.browser.execute_script("arguments[0].click();", status)
                    sex = self.browser.find_element_by_id(self.pedigree['sex'])
                    self.browser.execute_script("arguments[0].click();", sex)
                    born_as = self.browser.find_element_by_id(self.pedigree['born_as'])
                    self.browser.execute_script("arguments[0].click();", born_as)
                    dod = self.browser.find_element_by_id('id_date_of_death')
                    dod.send_keys(self.pedigree['dod'])
                    desc = self.browser.find_element_by_id('id_description')
                    desc.send_keys(self.pedigree['desc'])
                    desc = self.browser.find_element_by_id('id_breed')
                    desc.send_keys(self.pedigree['breed'])

                    # Save!
                    save_pedigree = self.browser.find_element_by_id('submitPedigree')
                    self.browser.execute_script("arguments[0].click();", save_pedigree)
                    confirm_save_pedigree = self.browser.find_element_by_id('confirmSaveBtn')
                    self.browser.execute_script("arguments[0].click();", confirm_save_pedigree)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter pedigree information'])
                        self.timeout = 0
                        # stop the current test
                        return 'fail'
            if user_type == '_contrib':
                # try to click "View approvals", as user is contributor
                while self.timeout < 20:
                    try:
                        new_pedigree = self.browser.find_element_by_xpath('//a[@href="/approvals/" and contains(text(), "View approval")]')
                        self.browser.execute_script("arguments[0].click();", new_pedigree)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to approvals page'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # check that pedigree is in the approvals table
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//td[contains(text(), "' + 'ABCD145879' + user_type + addition_method + '")]')) == 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Approval was not added to table'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new pedigree form there are", e)
                            exit(0)
            else:
                # check the save worked by trying to access new pedigree form
                while self.timeout < 20:
                    try:
                        # check there are no links to approvals page
                        if len(self.browser.find_elements_by_xpath('//a[@href="/approvals/" and contains(text(), "View approval")]')) == 0:
                            new_pedigree = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                            self.browser.execute_script("arguments[0].click();", new_pedigree)
                            sleep(2)
                            self.timeout = 0
                            break
                        # add error if there is an approval link
                        else:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Approval link was presented'])
                            # stop the current test
                            return 'fail'
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to save pedigree'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                
        # if user is read-only, test that they cannot add a pedigree
        else:
            # try to access new pedigree form via pedigree search
            if addition_method == '_pedigree_search':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new pedigree form there are", e)
                            exit(0)
            # try to access new pedigree form via view pedigree
            elif addition_method == '_pedigree_view':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        ped_view = self.browser.find_element_by_xpath('//button[contains(text(), "View")]')
                        self.browser.execute_script("arguments[0].click();", ped_view)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new pedigree form there are", e)
                            exit(0)
            # try to access new pedigree form via pedigree offspring
            elif addition_method == '_offspring':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        ped_view = self.browser.find_element_by_xpath('//button[contains(text(), "View")]')
                        self.browser.execute_script("arguments[0].click();", ped_view)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to offspring tab
                while self.timeout < 20:
                    try:
                        offspring = self.browser.find_element_by_xpath('//a[@href="#children"]')
                        self.browser.execute_script("arguments[0].click();", offspring)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open offspring tab'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//div[@id="children"]/a[@href="/pedigree/new_pedigree/"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new pedigree form there are", e)
                            exit(0)
            # try to access new pedigree form via pedigree certificate
            elif addition_method == '_certificate':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        ped_view = self.browser.find_element_by_xpath('//button[contains(text(), "View")]')
                        self.browser.execute_script("arguments[0].click();", ped_view)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to certificate tab
                while self.timeout < 20:
                    try:
                        certificate = self.browser.find_element_by_xpath('//a[@href="#cert"]')
                        self.browser.execute_script("arguments[0].click();", certificate)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open certificate tab'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//div[@id="certificate"]/table/tbody/tr/td/a[@href="/pedigree/new_pedigree/"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            print("Failed to find how many links to the new pedigree form were available from the certificate tab", e)
                            exit(0)
            # try to access new pedigree form via results page
            elif addition_method == '_results_from_peds':
                # go to pedigree search page
                while self.timeout < 20:
                    try:
                        ped_search = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                        self.browser.execute_script("arguments[0].click();", ped_search)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to open pedigree search'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control form-control-success"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new pedigree form there are", e)
                            exit(0)
            # try to access new pedigree form via results page
            elif addition_method == '_results_from_tool':
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new pedigree form there are", e)
                            exit(0)
        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Add Pedigree',user_type.replace('_', ' '),addition_method.replace('_', ' '),'PASS','-'])

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
                    print("Server Issue in adding breeder info try later", e,"at breeder prefix",breeder['breeding_prefix'])
                    exit(0)

    def add_each_single_breeder(self, pedigree_file):
        # add pedigree in all the different ways as each possible user
        self.add_single_breeder(pedigree_file, '_user', '_breeders')
        self.add_single_breeder(pedigree_file, '_user', '_breeder_view')
        self.add_single_breeder(pedigree_file, '_user', '_ped_form_breeder')
        self.add_single_breeder(pedigree_file, '_user', '_ped_form_owner')
        self.add_single_breeder(pedigree_file, '_admin', '_breeders')
        self.add_single_breeder(pedigree_file, '_admin', '_breeder_view')
        self.add_single_breeder(pedigree_file, '_admin', '_ped_form_breeder')
        self.add_single_breeder(pedigree_file, '_admin', '_ped_form_owner')
        self.add_single_breeder(pedigree_file, '_contrib', '_breeders')
        self.add_single_breeder(pedigree_file, '_contrib', '_breeder_view')
        self.add_single_breeder(pedigree_file, '_contrib', '_ped_form_breeder')
        self.add_single_breeder(pedigree_file, '_contrib', '_ped_form_owner')
        self.add_single_breeder(pedigree_file, '_read', '_breeders')
        self.add_single_breeder(pedigree_file, '_read', '_breeder_view')
        self.add_single_breeder(pedigree_file, '_read', '_ped_form_breeder')
        self.add_single_breeder(pedigree_file, '_read', '_ped_form_owner')

    def add_single_breeder(self, pedigree_file, user_type, addition_method):
        self.logout()
        # login as the correct user
        if user_type == '_user':
            self.login_user()
        elif user_type == '_admin':
            self.login_admin()
        elif user_type == '_contrib':
            self.login_contrib()
        elif user_type == '_read':
            self.login_read()

        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

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
                    print("Server Issue in adding breed info try later", e," at breed name",breed['breed_name'])
                    exit(0)

    def delete_all_pedigrees(self):
        # go to pedigree search page
        pedigree_link = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
        self.browser.execute_script("arguments[0].click();", pedigree_link)
        sleep(2)
        while self.browser.find_element_by_class_name('odd'):
            while True:
                try:
                    pedigree_links = self.browser.find_element_by_class_name('odd')
                    self.browser.execute_script("arguments[0].click();", pedigree_links)
                    self.delete_pedigree()
                    pedigree_link = self.browser.find_element_by_xpath('//a[@href="/pedigree/search"]')
                    self.browser.execute_script("arguments[0].click();", pedigree_link)
                    sleep(2)
                except Exception as e:
                    print("All Pedigree Deleted ")
                    return

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
        breeders_link = self.browser.find_element_by_xpath('//a[@href="/breeders/"]')
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
                        self.browser.execute_script("arguments[0].click();", edit_breeders)
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
                            print("All Breeders Deleted")
                            return
            except:
                print("All Breeders Deleted ")
                return
    def delete_all_breeds(self):
        # go to breed page
        breed_link = self.browser.find_element_by_xpath('//a[@href="/breeds/"]')
        self.browser.execute_script("arguments[0].click();", breed_link)
        try:
            while self.browser.find_element_by_class_name('btn-outline-info'):
                edit_breed_links = self.browser.find_elements_by_class_name('btn-outline-info')
                self.browser.execute_script("arguments[0].click();", edit_breed_links[0])
                self.delete_breed()
                breed_link = self.browser.find_element_by_xpath('//a[@href="/breeds/"]')
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
        self.browser.get(self.config['settings']['domain']+"/account/settings")
        sleep(2)
        users_link = self.browser.find_element_by_xpath('//a[@href="#users"]')
        self.browser.execute_script("arguments[0].click();", users_link)
        user_reader = csv.DictReader(open(user_file, newline=''))

        for user in user_reader:
            create_new = self.browser.find_element_by_id('createNew')
            self.browser.execute_script("arguments[0].click();", create_new)
            sleep(1)
            fname = self.browser.find_element_by_id('firstName')
            fname.send_keys(user['first_name'])
            lname = self.browser.find_element_by_id('lastName')
            lname.send_keys(user['second_name'])
            uname = self.browser.find_element_by_id('register-form-username')
            uname.send_keys(user['username'])
            email = self.browser.find_element_by_id('register-form-email')
            email.send_keys(user['email'])
            status = self.browser.find_element_by_id('status')
            status.send_keys(user['status'])
            modal_save = self.browser.find_elements_by_id('userFormBtn')
            self.browser.execute_script("arguments[0].click();", modal_save[0])
            sleep(5)
        return


    def delete_users(self,idx = 1):
        self.browser.get(self.config['settings']['domain'] + "/account/settings")
        sleep(2)
        while True:
            try:
                users_link = self.browser.find_element_by_xpath('//a[@href="#users"]')
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
        self.browser.get(self.config['settings']['domain'] + "/account/settings")
        sleep(2)
        customisation_link = self.browser.find_element_by_xpath('//a[@href="#customisation"]')
        self.browser.execute_script("arguments[0].click();", customisation_link)
        mum = self.browser.find_element_by_id('mother')
        mum.clear()
        mum.send_keys(mother)
        dad = self.browser.find_element_by_id('father')
        dad.clear()
        dad.send_keys(father)
        confirm_update = self.browser.find_element_by_id('selectTitleSettings')
        self.browser.execute_script("arguments[0].click();", confirm_update)

    def edit_column_load(self):
        self.browser.get(self.config['settings']['domain'] + "/account/settings")
        sleep(2)
        customisation_link = self.browser.find_element_by_xpath('//a[@href="#customisation"]')
        self.browser.execute_script("arguments[0].click();", customisation_link)
        checks = ['checkbox6', 'checkbox16', 'checkbox23', 'checkbox24']
        for ids in checks:
            ele = self.browser.find_element_by_id(ids)
            self.browser.execute_script("arguments[0].click();", ele)
        saveBtn = self.browser.find_element_by_id('selectPedigreeColumnsBtn')
        self.browser.execute_script("arguments[0].click();", saveBtn)


    def run_coi(self):
        self.browser.get(self.config['settings']['domain'] + "/metrics")
        sleep(2)
        run_coi_btn = self.browser.find_element_by_id('coiBtn')
        self.browser.execute_script("arguments[0].click();", run_coi_btn)

    def run_mean_kinship(self):
        self.browser.get(self.config['settings']['domain'] + "/metrics")
        sleep(2)
        run_mk_btn = self.browser.find_element_by_id('meanKinshipBtn')
        self.browser.execute_script("arguments[0].click();", run_mk_btn)
    def run_stud_selector(self,val_mum):
        self.browser.get(self.config['settings']['domain'] + "/metrics")
        sleep(2)
        mum_sa = self.browser.find_element_by_id('sa_mother')
        mum_sa.send_keys(val_mum)
        run_stud_btn = self.browser.find_element_by_id('saBtn')
        self.browser.execute_script("arguments[0].click();", run_stud_btn)

    def test(self,type,option=""):
        if type == 'login_user':
            self.login_user()
        if type == 'login_admin':
            self.login_admin()
        if type == 'login_contrib':
            self.login_contrib()
        if type == 'login_read':
            self.login_read()
        if type == 'logout':
            self.logout()
        elif type == 'add_pedigree':
            self.add_pedigree('pedigree.csv','breed.csv','breeder.csv')
        elif type == 'add_each_single_pedigree':
            self.add_each_single_pedigree('pedigree.csv')
        elif type == 'delete_all_pedigrees':
            self.delete_all_pedigrees()
        elif type == 'delete_all_breeders':
            self.delete_all_breeders(option)
        elif type == 'delete_all_breeds':
            self.delete_all_breeds()
        elif type == "add_users":
            self.add_user('user.csv')
        elif type == 'delete_users':
            self.delete_users(int(input("Enter the index from which you want to start deleting ")))
        elif type == 'update_parent_titles':
            self.edit_parent_titles(input("Enter Mother Title "),input("Enter Father Title "))
        elif type == 'edit_column_load':
            self.edit_column_load()
        elif type == 'run_coi':
            self.run_coi()
        elif type == 'run_mean_kinship':
            self.run_mean_kinship()
        elif type == 'run_stud_selector':
            mum = input('Enter Mother Name ')
            self.run_stud_selector(mum)



if __name__ == '__main__':
    obj = CloudLinesTestV2()
    #obj.login()
    print("1. Login as User/Owner")
    print("2. Login as Admin")
    print("3. Login as Contributor")
    print("4. Login as Read-Only")
    print("5. Logout")
    print("6. Add Pedigree")
    print("7. Add Single Pedigree")
    print("8. Delete All Pedigrees")
    print("9. Delete All Breeders")
    print("10. Add Users")
    print("11. Delete Users")
    print("12. Edit Parent Titles")
    print("13. Add and Delete All Pedrigrees, Breeders, Breeds")
    print("14. Edit Pedigree Columns Load")
    print("15. Run COI")
    print("16. Run Mean Kinship")
    print("17. Run Stud Selector")
    print("_. Exit")
    ch = input("Enter Choice ")
    while ch != '_':
        try:
            if ch == "1":
                obj.test('login_user')
            if ch == "2":
                obj.test('login_admin')
            if ch == "3":
                obj.test('login_contrib')
            if ch == "4":
                obj.test('login_read')
            if ch == "5":
                obj.test('logout')
            elif ch == "6":
                obj.test('add_pedigree')
            elif ch == "7":
                obj.test('add_each_single_pedigree')
            elif ch == "8":
                obj.test('delete_all_pedigrees')
            elif ch == "9":
                obj.test('delete_all_breeders',input("Enter Breeder Prefix "))
            elif ch == "10":
                obj.test('add_users')
            elif ch == "11":
                obj.test('delete_users')
            elif ch == "12":
                obj.test('update_parent_titles')
            elif ch == "13":
                obj.test('add_pedigree')
                obj.delete_all_breeds()
                obj.test('delete_all_breeders', input("Enter Breeder Prefix "))
                obj.test('delete_all_pedigrees')
            elif ch == "14":
                obj.test('edit_column_load')
            elif ch == "15":
                obj.test('run_coi')
            elif ch == "16":
                obj.test('run_mean_kinship')
            elif ch == "17":
                obj.test('run_stud_selector')
            ch = input("Enter Choice ")
        except:
            break