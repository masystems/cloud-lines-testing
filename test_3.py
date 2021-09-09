from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from configparser import ConfigParser
import csv
from datetime import datetime
from tld import get_tld

class CloudLinesTestV2():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.cfg')

        self.username_user = self.config['settings']['username_user']
        self.password_user = self.config['settings']['password_user']
        self.username_admin = self.config['settings']['username_admin']
        self.password_admin = self.config['settings']['password_admin']
        self.username_breed = self.config['settings']['username_breed']
        self.password_breed = self.config['settings']['password_breed']
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

        # the type of user that is currently logged in
        self.current_user_type = None

        # create csv results file
        self.results_file = f'results/results_{datetime.now()}.csv'
        with open(self.results_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Action", "User Type", "Scenario", "Result", "Description"])

    def logout(self):
        self.browser.get(self.config['settings']['domain'] + "/account/logout")
        self.current_user_type = None
        sleep(2)

    def login(self, action, user_type, scenario):
        while self.timeout < 20:
            try:
                # if not logged in as correct user
                if self.current_user_type != user_type:
                    # logout if we're logged in as wrong user
                    if self.current_user_type:
                        self.logout()
                    # set username and password correctly
                    if user_type == 'user':
                        username = self.username_user
                        password = self.password_user
                    elif user_type == 'admin':
                        username = self.username_admin
                        password = self.password_admin
                    elif user_type == 'breed':
                        username = self.username_breed
                        password = self.password_breed
                    elif user_type == 'contrib':
                        username = self.username_contrib
                        password = self.password_contrib
                    elif user_type == 'read':
                        username = self.username_read
                        password = self.password_read
                    
                    # get login button based on which login form we're in
                    # which depends on whether there is a subdomain
                    if 'localhost' not in self.browser.current_url and '127.0.0.1' not in self.browser.current_url:
                        if get_tld(self.browser.current_url, as_object=True).subdomain:
                            login = self.browser.find_element_by_id('loginBtn')
                        else:
                            dashboard = self.browser.find_element_by_xpath('//a[@href="/dashboard"]')
                            self.browser.execute_script("arguments[0].click();", dashboard)
                            sleep(2)
                            login = self.browser.find_element_by_id('login-form-submit')
                    else:
                        dashboard = self.browser.find_element_by_xpath('//a[@href="/dashboard"]')
                        self.browser.execute_script("arguments[0].click();", dashboard)
                        sleep(2)
                        login = self.browser.find_element_by_id('login-form-submit')
                    
                    username_field = self.browser.find_element_by_name('username')
                    password_field = self.browser.find_element_by_name('password')
                    username_field.send_keys(username)
                    password_field.send_keys(password)
                    self.browser.execute_script("arguments[0].click();", login)
                    self.current_user_type = user_type
                    sleep(2)
                self.timeout = 0
                break
            except Exception as e:
                self.timeout += 1
                if self.timeout == 20:
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action, user_type.replace('_', ' '), scenario.replace('_', ' '), 'FAIL', 'Failed to login'])
                    self.timeout = 0
                    # stop the current test
                    return 'fail'
        
        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f'{action} - Login',user_type.replace('_', ' '),scenario.replace('_', ' '),'PASS','-'])

    def click_element_by_xpath(self, path, action, user_type, scenario, result, desc):
        while self.timeout < 20:
            try:
                # do click
                element = self.browser.find_element_by_xpath(path)
                self.browser.execute_script("arguments[0].click();", element)
                sleep(2)
                self.timeout = 0
                break
            except Exception as e:
                self.timeout += 1
                if self.timeout == 20:
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action, user_type.replace('_', ' '), scenario.replace('_', ' '), result, desc])
                    self.timeout = 0
                    # stop the current test
                    return 'fail'

    def add_each_pedigree(self, pedigree_file):
        # add pedigree in all the different ways as each possible user
        self.add_pedigree(pedigree_file, 'user', 'pedigree_search')
        self.add_pedigree(pedigree_file, 'user', 'pedigree_view')
        self.add_pedigree(pedigree_file, 'user', 'offspring')
        self.add_pedigree(pedigree_file, 'user', 'certificate')
        self.add_pedigree(pedigree_file, 'user', 'results_from_peds')
        self.add_pedigree(pedigree_file, 'user', 'results_from_tool')
        self.add_pedigree(pedigree_file, 'admin', 'pedigree_search')
        self.add_pedigree(pedigree_file, 'admin', 'pedigree_view')
        self.add_pedigree(pedigree_file, 'admin', 'offspring')
        self.add_pedigree(pedigree_file, 'admin', 'certificate')
        self.add_pedigree(pedigree_file, 'admin', 'results_from_peds')
        self.add_pedigree(pedigree_file, 'admin', 'results_from_tool')
        self.add_pedigree(pedigree_file, 'breed', 'pedigree_search')
        self.add_pedigree(pedigree_file, 'breed', 'pedigree_view')
        self.add_pedigree(pedigree_file, 'breed', 'offspring')
        self.add_pedigree(pedigree_file, 'breed', 'certificate')
        self.add_pedigree(pedigree_file, 'breed', 'results_from_peds')
        self.add_pedigree(pedigree_file, 'breed', 'results_from_tool')
        self.add_pedigree(pedigree_file, 'contrib', 'pedigree_search')
        self.add_pedigree(pedigree_file, 'contrib', 'pedigree_view')
        self.add_pedigree(pedigree_file, 'contrib', 'offspring')
        self.add_pedigree(pedigree_file, 'contrib', 'certificate')
        self.add_pedigree(pedigree_file, 'contrib', 'results_from_peds')
        self.add_pedigree(pedigree_file, 'contrib', 'results_from_tool')
        self.add_pedigree(pedigree_file, 'read', 'pedigree_search')
        self.add_pedigree(pedigree_file, 'read', 'pedigree_view')
        self.add_pedigree(pedigree_file, 'read', 'offspring')
        self.add_pedigree(pedigree_file, 'read', 'certificate')
        self.add_pedigree(pedigree_file, 'read', 'results_from_peds')
        self.add_pedigree(pedigree_file, 'read', 'results_from_tool')

    def add_pedigree(self, pedigree_file, user_type, addition_method):
        action = 'Add Pedigree'
        
        # ensure we're logged in as the correct user
        self.login(action, user_type, addition_method)

        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # if user is not read-only, test adding a pedigree
        if user_type != 'read':
            pedgree_reader = csv.DictReader(open(pedigree_file,newline=''))
            self.pedigree = dict(pedgree_reader.__next__())

            # access new pedigree form via pedigree search
            if addition_method == 'pedigree_search':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # go to add new pedigree
                if self.click_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open add pedigree form') == 'fail':
                    # test failed
                    return 'fail'
            # access new pedigree form via view pedigree
            elif addition_method == 'pedigree_view':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # go to view pedigree
                if self.click_element_by_xpath('//button[contains(text(), "View")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree view') == 'fail':
                    # test failed
                    return 'fail'
                # go to add new pedigree
                if self.click_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open new pedigree form') == 'fail':
                    # test failed
                    return 'fail'
            # access new pedigree form via pedigree offspring
            elif addition_method == 'offspring':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # go to view pedigree
                if self.click_element_by_xpath('//button[contains(text(), "View")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree view') == 'fail':
                    # test failed
                    return 'fail'
                # go to offspring tab
                if self.click_element_by_xpath('//a[@href="#children"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open offspring tab') == 'fail':
                    # test failed
                    return 'fail'
                # go to add new pedigree
                if self.click_element_by_xpath('//div[@id="children"]/a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open new pedigree form') == 'fail':
                    # test failed
                    return 'fail'
            # access new pedigree form via pedigree certificate
            elif addition_method == 'certificate':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # go to view pedigree
                while self.timeout < 20:
                    try:
                        # do click
                        element = self.browser.find_elements_by_xpath('//button[contains(text(), "View")]')[1]
                        self.browser.execute_script("arguments[0].click();", element)
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action, user_type.replace('_', ' '), addition_method.replace('_', ' '), 'Fail', 'Failed to open pedigree view'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to certificate tab
                if self.click_element_by_xpath('//a[@href="#cert"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open certificate tab') == 'fail':
                    # test failed
                    return 'fail'
                # go to add new pedigree
                if self.click_element_by_xpath('//div[@id="certificate"]/table/tbody/tr/td/a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open new pedigree form') == 'fail':
                    # test failed
                    return 'fail'
            # accessing new pedigree form via results page
            elif addition_method == 'results_from_peds':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control form-control-success"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # go to add new pedigree
                if self.click_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open new pedigree form') == 'fail':
                    # test failed
                    return 'fail'
            # accessing new pedigree form via results page
            elif addition_method == 'results_from_tool':
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # go to add new pedigree
                if self.click_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open new pedigree form') == 'fail':
                    # test failed
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
                    reg_no.send_keys(f"{self.pedigree['reg_no']}_{user_type}_{addition_method}")
                    tag_no = self.browser.find_element_by_id('id_tag_no')
                    tag_no.send_keys(self.pedigree['tag_no'])
                    name = self.browser.find_element_by_id('id_name')
                    name.send_keys(f"{self.pedigree['name']}_{user_type}_{addition_method}")
                    dor = self.browser.find_element_by_id('id_date_of_registration')
                    dor.send_keys(self.pedigree['dor'])
                    dob = self.browser.find_element_by_id('id_date_of_birth')
                    dob.send_keys(self.pedigree['dob'])
                    status = self.browser.find_element_by_id(self.pedigree['status'])
                    self.browser.execute_script("arguments[0].click();", status)
                    sex = self.browser.find_element_by_id(self.pedigree['sex'])
                    self.browser.execute_script("arguments[0].click();", sex)
                    litter_size = self.browser.find_element_by_id('litter_size')
                    self.browser.execute_script("arguments[0].click();", litter_size)
                    litter_size_10 = self.browser.find_element_by_xpath('//option[@value="10"]')
                    self.browser.execute_script("arguments[0].click();", litter_size_10)
                    dod = self.browser.find_element_by_id('id_date_of_death')
                    dod.send_keys(self.pedigree['dod'])
                    desc = self.browser.find_element_by_id('id_description')
                    desc.send_keys(self.pedigree['desc'])
                    desc = self.browser.find_element_by_id('id_breed')
                    desc.send_keys(self.pedigree['breed'])
                    mother = self.browser.find_element_by_id('id_mother')
                    mother.send_keys(self.pedigree['mother'])
                    father = self.browser.find_element_by_id('id_father')
                    father.send_keys(self.pedigree['father'])

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
                            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter pedigree information'])
                        self.timeout = 0
                        # stop the current test
                        return 'fail'
            if user_type == 'contrib':
                # try to click "View approvals", as user is contributor
                if self.click_element_by_xpath('//a[@href="/approvals/" and contains(text(), "View approvals")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to go to approvals page') == 'fail':
                    # test failed
                    return 'fail'
                # check that pedigree is in the approvals table
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//td[contains(text(), "' + 'ABCD145879' + '_' + user_type + '_' + addition_method + '")]')) == 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Approval was not added to table'])
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
                # login as user so check approval can be accepted
                self.login(action, 'user', addition_method)
                self.browser.get(self.config['settings']['domain'] + "/account/welcome")
                # go to approvals
                if self.click_element_by_xpath('//a[@href="/approvals/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to go to approvals page') == 'fail':
                    # test failed
                    return 'fail'
                # approve the approval
                if self.click_element_by_xpath('//button[contains(text(), "Approve")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to approve the approval') == 'fail':
                    # test failed
                    return 'fail'
                # check the approval is gone from the queue
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//td[contains(text(), "Approve")]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','The table still contains an approval'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many approvals in the queue there are", e)
                            exit(0)
            else:
                # check the save worked by trying to access new pedigree form
                while self.timeout < 20:
                    try:
                        # check there are no links to approvals page
                        if len(self.browser.find_elements_by_xpath('//a[@href="/approvals/" and contains(text(), "View approval")]')) == 0:
                            new_pedigree = self.browser.find_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]')
                            sleep(2)
                            self.browser.execute_script("arguments[0].click();", new_pedigree)
                            sleep(2)
                            self.timeout = 0
                            break
                        # add error if there is an approval link
                        else:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Approval link was presented'])
                            # stop the current test
                            return 'fail'
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to save pedigree'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                
        # if user is read-only, test that they cannot add a pedigree
        else:
            # try to access new pedigree form via pedigree search
            if addition_method == 'pedigree_search':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            elif addition_method == 'pedigree_view':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # go to view pedigree
                if self.click_element_by_xpath('//button[contains(text(), "View")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree view') == 'fail':
                    # test failed
                    return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            elif addition_method == 'offspring':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # try to go to view pedigree
                if self.click_element_by_xpath('//button[contains(text(), "View")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree view') == 'fail':
                    # test failed
                    return 'fail'
                # check you can't go to offspring tab
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="#children"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new offspring tab is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to offspring tab there are", e)
                            exit(0)
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//div[@id="children"]/a[@href="/pedigree/new_pedigree/"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            elif addition_method == 'certificate':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # try to go to view pedigree
                if self.click_element_by_xpath('//button[contains(text(), "View")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree view') == 'fail':
                    # test failed
                    return 'fail'
                # check you can't go to certificate tab
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="#cert"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new certificate tab is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to certificate tab there are", e)
                            exit(0)
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//div[@id="certificate"]/table/tbody/tr/td/a[@href="/pedigree/new_pedigree/"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            elif addition_method == 'results_from_peds':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control form-control-success"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            elif addition_method == 'results_from_tool':
                # enter text in search field and submit search
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control"]')
                    search_field.send_keys('animal_111\n')
                except Exception as e:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                        # stop the current test
                        return 'fail'
                # check we successfully went to results page
                if self.browser.current_url != f"{self.config['settings']['domain']}/pedigree/results/":
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to go to results page'])
                    # stop the current test
                    return 'fail'
                # check you can't go to add new pedigree
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'PASS','-'])

    def add_each_breeder(self, pedigree_file):
        # add pedigree in all the different ways as each possible user
        self.add_breeder(pedigree_file, 'user', 'breeders')
        self.add_breeder(pedigree_file, 'user', 'breeder_view')
        self.add_breeder(pedigree_file, 'user', 'ped_form')
        self.add_breeder(pedigree_file, 'admin', 'breeders')
        self.add_breeder(pedigree_file, 'admin', 'breeder_view')
        self.add_breeder(pedigree_file, 'admin', 'ped_form')
        self.add_breeder(pedigree_file, 'breed', 'breeders')
        self.add_breeder(pedigree_file, 'breed', 'breeder_view')
        self.add_breeder(pedigree_file, 'breed', 'ped_form')
        self.add_breeder(pedigree_file, 'contrib', 'breeders')
        self.add_breeder(pedigree_file, 'contrib', 'breeder_view')
        self.add_breeder(pedigree_file, 'contrib', 'ped_form')
        self.add_breeder(pedigree_file, 'read', 'breeders')
        self.add_breeder(pedigree_file, 'read', 'breeder_view')
        self.add_breeder(pedigree_file, 'read', 'ped_form')

    def add_breeder(self, breeder_file, user_type, addition_method):
        action = 'Add Breeder'
        
        # ensure we're logged in as the correct user
        self.login(action, user_type, addition_method)

        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # if user owner/admin they can add a breeder
        if user_type in ('user', 'admin', 'breed'):
            breeder_reader = csv.DictReader(open(breeder_file,newline=''))
            self.breeder = dict(breeder_reader.__next__())

            # access new pedigree form via breeders page
            if addition_method == 'breeders':
                # go to breeders page
                if self.click_element_by_xpath('//a[@href="/breeders/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open breeders page') == 'fail':
                    # test failed
                    return 'fail'
                # go to add new breeder
                if self.click_element_by_xpath('//a[@href="/breeders/new_breeder/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open new breeder form') == 'fail':
                    # test failed
                    return 'fail'
            # access new pedigree form via breeders page
            elif addition_method == 'breeder_view':
                # go to breeders page
                if self.click_element_by_xpath('//a[@href="/breeders/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open breeders page') == 'fail':
                    # test failed
                    return 'fail'
                # go to breeder view
                if self.click_element_by_xpath('//tr[@onclick]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open breeder view page') == 'fail':
                    # test failed
                    return 'fail'
                # go to add new breeder
                if self.click_element_by_xpath('//a[@href="/breeders/new_breeder/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open add breeder form') == 'fail':
                    # test failed
                    return 'fail'
            # access new pedigree form via add breeder button in add pedigree page
            elif addition_method == 'ped_form':
                # go to pedigree search page
                if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                    # test failed
                    return 'fail'
                # go to add pedigree form
                if self.click_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open add pedigree form') == 'fail':
                    # test failed
                    return 'fail'
                # go to add breeder form modal via add breeder button
                if self.click_element_by_xpath('//button[@id="showNewBreederModal"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open add breeder modal') == 'fail':
                    # test failed
                    return 'fail'

            # enter breeder information
            while self.timeout < 20:
                try:
                    breeding_prefix = self.browser.find_element_by_name('breeding_prefix')
                    breeding_prefix.send_keys(f"{self.breeder['breeding_prefix']}_{user_type}_{addition_method}")
                    contact_name = self.browser.find_element_by_name('contact_name')
                    contact_name.send_keys(f"{self.breeder['contact_name']}_{user_type}_{addition_method}")
                    address_1 = self.browser.find_element_by_name('address_line_1')
                    address_1.send_keys('1 Address Lane')
                    address_2 = self.browser.find_element_by_name('address_line_2')
                    address_2.send_keys('2 Address Lane')
                    phone_number1 = self.browser.find_element_by_name('phone_number1')
                    phone_number1.send_keys(self.breeder['phone_number1'])
                    phone_number2 = self.browser.find_element_by_name('phone_number2')
                    phone_number2.send_keys(self.breeder['phone_number2'])
                    email = self.browser.find_element_by_name('email')
                    email.send_keys(f"{self.breeder['email']}_{user_type}_{addition_method}")
                    active = self.browser.find_element_by_name('active')
                    self.browser.execute_script("arguments[0].click();", active)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter breeder information'])
                        self.timeout = 0
                        # stop the current test
                        return 'fail'
            # submit form in correct way given that we're in normal new breeder form
            if addition_method in ('breeders', 'breeder_view'):
                # submit new breeder form
                if self.click_element_by_xpath('//button[@type="submit" and @class="btn btn-success" and contains(text(), "Submit")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to submit breeder info') == 'fail':
                    # test failed
                    return 'fail'
            # submit form in correct way given that we're in new breeder modal
            else:
                # submit new breeder form
                if self.click_element_by_xpath('//button[@id="saveBreeder" and contains(text(), "Save breeder")]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to submit breeder info') == 'fail':
                    # test failed
                    return 'fail'
            # check the save worked by checking we're on one of the right pages
            if '/pedigree/new_pedigree' not in self.browser.current_url and '/breeders' not in self.browser.current_url:
                # add fail to reports file
                with open(self.results_file, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([action, user_type.replace('_', ' '), addition_method.replace('_', ' '), 'FAIL', 'Failed to save breeder'])
                self.timeout = 0
                # stop the current test
                return 'fail'
        
        # user is read-only/contributor, so make sure they can't access new breeder form
        else:
            # ensure you can't access new breeder form via breeder view page
            if addition_method == 'breeder_view':
                # go to breeders page
                if self.click_element_by_xpath('//a[@href="/breeders/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open breeders page') == 'fail':
                    # test failed
                    return 'fail'
                # filter for breeder ZZZZZx
                try:
                    search_field = self.browser.find_element_by_xpath('//input[@type="search"][@class="form-control form-control-sm"]')
                    search_field.send_keys('ZZZZZx')
                except Exception as e:
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Failed to enter text in filter field to search for ZZZZZx'])
                    # stop the current test
                    return 'fail'
                # go to breeder view
                if self.click_element_by_xpath('//tr[@onclick]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open breeder view page') == 'fail':
                    # test failed
                    return 'fail'
                # check you can't go to add new breeder form
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/breeders/new_breeder"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new breeder form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new breeder form there are", e)
                            exit(0)
            # ensure you can't access new breeder form via breeders page
            elif addition_method == 'breeders':
                # go to breeders page
                if self.click_element_by_xpath('//a[@href="/breeders/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open breeders page') == 'fail':
                    # test failed
                    return 'fail'
                # check you can't go to add new breeder form
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@href="/breeders/new_breeder"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new breeder form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test failed
                            print("Failed to find how many links to new breeder form there are", e)
                            exit(0)
            # ensure you can't access new pedigree form via pedigree form
            elif addition_method == 'ped_form':
                # contributor, so check the add breeder button is not on the add pedigree form
                if user_type == 'contrib':
                    # go to pedigree search page
                    if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                        # test failed
                        return 'fail'
                    # go to pedigree form
                    if self.click_element_by_xpath('//a[@href="/pedigree/new_pedigree/"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open add pedigree form') == 'fail':
                        # test failed
                        return 'fail'
                    # check add breeder button is not there
                    while self.timeout < 20:
                        try:
                            if len(self.browser.find_elements_by_xpath('//button[@id="showNewBreederModal"]')) > 0:
                                # add fail to reports file
                                with open(self.results_file, 'a+', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Button to display new breeder modal is available'])
                                # stop the current test
                                return 'fail'
                            sleep(2)
                            self.timeout = 0
                            break
                        except Exception as e:
                            self.timeout += 1
                            if self.timeout == 20:
                                # test failed
                                print("Failed to find how many buttons to display new breeder modal there are", e)
                                exit(0)
                # user is read only, so check user can't get to the add pedigree form
                else:
                    # go to pedigree search page
                    if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                            action, user_type, addition_method, 'FAIL',
                            'Failed to open pedigree search') == 'fail':
                        # test failed
                        return 'fail'
                    # check you can't go to add new pedigree
                    while self.timeout < 20:
                        try:
                            if len(self.browser.find_elements_by_xpath('//a[@href="/pedigree/new_pedigree"]')) > 0:
                                # add fail to reports file
                                with open(self.results_file, 'a+', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'FAIL','Link to new pedigree form is available'])
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
            writer.writerow([action,user_type.replace('_', ' '),addition_method.replace('_', ' '),'PASS','-'])

    def edit_each_pedigree(self):
        self.edit_pedigree('user', 'ped_form')
        self.edit_pedigree('user', 'approval')
        self.edit_pedigree('admin', 'ped_form')
        self.edit_pedigree('admin', 'approval')
        self.edit_pedigree('breed', 'ped_form')
        self.edit_pedigree('breed', 'approval')
        self.edit_pedigree('contrib', 'ped_form')
        self.edit_pedigree('contrib', 'approval')
        self.edit_pedigree('read', 'ped_form')
        self.edit_pedigree('read', 'approval')

    def edit_pedigree(self, user_type, edit_method):
        action = 'Edit Pedigree'
        
        # ensure we're logged in as the correct user
        self.login(action, user_type, edit_method)

        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # test editting via edit pedigree form
        if edit_method == 'ped_form':
            # go to pedigree search page
            if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                        action, user_type, edit_method, 'FAIL',
                        'Failed to open pedigree search') == 'fail':
                # test failed
                return 'fail'
            # search for animal_14000_edit
            try:
                search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control form-control-success"]')
                search_field.send_keys('animal_14000_edit\n')
            except Exception as e:
                    # add fail to reports file
                    with open(self.results_file, 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                    # stop the current test
                    return 'fail'
            
            # not read only, so can access the form
            if user_type != 'read':
                # go to edit pedigree
                if self.click_element_by_xpath('//a[@id="editPedigree"]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to open edit pedigree form') == 'fail':
                    # test failed
                    return 'fail'
                # enter pedigree info
                while self.timeout < 20:
                    try:
                        # increment tag number or set it to 0
                        tag_no = self.browser.find_element_by_id('id_tag_no')
                        try:
                            current_tag = int(tag_no.get_attribute('value'))
                            tag_no.clear()
                            tag_no.send_keys(current_tag + 1)
                        except ValueError:
                            tag_no.clear()
                            tag_no.send_keys(0)
                        # get date of birth
                        dob = self.browser.find_element_by_id('id_dob')
                        # increment date of registration or set to date of birth
                        dor = self.browser.find_element_by_id('id_dor')
                        try:
                            int_dor = int(dor.get_attribute('value').replace('-', ''))
                            # get dd,mm,yyyy, and rearrange so it can be input into the field
                            dd = f'{int_dor}'[6:]
                            mm = f'{int_dor}'[4:6]
                            yyyy = f'{int_dor}'[:4]
                            if yyyy == '2021':
                                yyyy = '2008'
                            int_dor = int(f'{dd}{mm}{yyyy}')
                            dor.clear()
                            dor.send_keys(int_dor + 1)
                        except ValueError:
                            int_dob = int(dob.get_attribute('value').replace('-', ''))
                            dd = f'{int_dob}'[6:]
                            mm = f'{int_dob}'[4:6]
                            yyyy = f'{int_dob}'[:4]
                            dor.clear()
                            dor.send_keys(f'{dd}{mm}{yyyy}')
                        # set status to alive if currently dead, unknown if currently alive, and dead if currently unknown
                        dead_status = self.browser.find_element_by_id('id_status_0')
                        alive_status = self.browser.find_element_by_id('id_status_1')
                        unknown_status = self.browser.find_element_by_id('id_status_2')
                        if dead_status.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", alive_status)
                        elif alive_status.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", unknown_status)
                        else:
                            self.browser.execute_script("arguments[0].click();", dead_status)
                        # if litter size 10 set to 20, etc, and if 40 set to 10
                        litter_size = self.browser.find_element_by_id('litter_size')
                        self.browser.execute_script("arguments[0].click();", litter_size)
                        litter_size_10 = self.browser.find_element_by_xpath('//option[@value="10"]')
                        litter_size_20 = self.browser.find_element_by_xpath('//option[@value="20"]')
                        litter_size_30 = self.browser.find_element_by_xpath('//option[@value="30"]')
                        litter_size_40 = self.browser.find_element_by_xpath('//option[@value="40"]')
                        if litter_size_10.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", litter_size_20)
                        elif litter_size_20.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", litter_size_30)
                        elif litter_size_30.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", litter_size_40)
                        else:
                            self.browser.execute_script("arguments[0].click();", litter_size_10)
                        # increment date of death or set to date of birth
                        dod = self.browser.find_element_by_id('id_date_of_death')
                        try:
                            int_dod = int(dod.get_attribute('value').replace('-', ''))
                            # get dd,mm,yyyy, and rearrange so it can be input into the field
                            dd = f'{int_dod}'[6:]
                            mm = f'{int_dod}'[4:6]
                            yyyy = f'{int_dod}'[:4]
                            if yyyy == '2021':
                                yyyy = '2008'
                            int_dod = int(f'{dd}{mm}{yyyy}')
                            dod.clear()
                            dod.send_keys(int_dod + 1)
                        except ValueError:
                            int_dob = int(dob.get_attribute('value').replace('-', ''))
                            dd = f'{int_dob}'[6:]
                            mm = f'{int_dob}'[4:6]
                            yyyy = f'{int_dob}'[:4]
                            dod.clear()
                            dod.send_keys(f'{dd}{mm}{yyyy}')
                        # increment description or set to 0
                        desc = self.browser.find_element_by_id('id_description')
                        try:
                            current_desc = int(desc.text)
                            desc.clear()
                            desc.send_keys(current_desc + 1)
                        except ValueError:
                            desc.clear()
                            desc.send_keys(0)
                        # save
                        save_pedigree = self.browser.find_element_by_xpath('//button[@type="submit" and @data-target=".confirmForm"]')
                        self.browser.execute_script("arguments[0].click();", save_pedigree)
                        confirm_save_pedigree = self.browser.find_element_by_xpath('//button[@type="button" and @class="btn btn-success waves-effect waves-light confirmSaveBtn"]')
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
                                writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter pedigree information'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                
                if user_type in ('user', 'admin', 'breed'):
                    # check approval wasn't created and that we can go to new pedigree form to check that the save worked
                    while self.timeout < 20:
                        try:
                            # check there are no links to approvals page
                            if len(self.browser.find_elements_by_xpath('//a[@href="/approvals/" and contains(text(), "View approval")]')) == 0:
                                # try to go to new pedigree form
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
                                    writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Approval link was presented'])
                                # stop the current test
                                return 'fail'
                        except Exception as e:
                            self.timeout += 1
                            if self.timeout == 20:
                                # add fail to reports file
                                with open(self.results_file, 'a+', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to save pedigree'])
                                self.timeout = 0
                                # stop the current test
                                return 'fail'
                # user is contributor
                else:
                    # try to click "View approval"
                    if self.click_element_by_xpath('//a[@href="/approvals/"]',
                                action, user_type, edit_method, 'FAIL',
                                'Failed to open approvals page') == 'fail':
                        # test failed
                        return 'fail'
                    # login as owner to approve the edit
                    self.login(action, 'user', edit_method)
                    # go to approvals
                    if self.click_element_by_xpath('//a[@href="/approvals/"]',
                                    action, user_type, edit_method, 'FAIL',
                                    'Failed to open approvals') == 'fail':
                        # test failed
                        return 'fail'
                    # approve the edit
                    if self.click_element_by_xpath('//button[@class="btn btn-sm btn-success mr-1" and contains(text(), "Approve")]',
                                    action, user_type, edit_method, 'FAIL',
                                    'Failed to approve edit') == 'fail':
                        # test failed
                        return 'fail'
            # user is read only
            else:
                # check they can't access edit pedigree form
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//a[@id="editPedigree"]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Link to edit pedigree form is available'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test did not work
                            print("Failed to find how many links to edit pedigree form there are", e)
                            exit(0)
        # test editting by editting an approval
        elif edit_method == 'approval':
            # create approval by editting as contributor
            self.login(action, 'contrib', edit_method)
            # go to pedigree search page
            if self.click_element_by_xpath('//a[@href="/pedigree/search"]',
                        action, user_type, edit_method, 'FAIL',
                        'Failed to open pedigree search') == 'fail':
                # test failed
                return 'fail'
            # search for animal_14000_edit
            try:
                search_field = self.browser.find_element_by_xpath('//input[@id="search"][@class="form-control form-control-success"]')
                search_field.send_keys('animal_14000_edit\n')
            except Exception as e:
                # add fail to reports file
                with open(self.results_file, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter text in search field'])
                # stop the current test
                return 'fail'
            # go to edit pedigree
            if self.click_element_by_xpath('//a[@id="editPedigree"]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to open edit pedigree form') == 'fail':
                # test failed
                return 'fail'
            # edit description to create approval
            while self.timeout < 20:
                try:
                    desc = self.browser.find_element_by_id('id_description')
                    try:
                        current_desc = int(desc.text)
                        desc.clear()
                        desc.send_keys(current_desc + 1)
                    except ValueError:
                        desc.clear()
                        desc.send_keys(0)
                    save_pedigree = self.browser.find_element_by_xpath('//button[@type="submit" and @data-target=".confirmForm"]')
                    self.browser.execute_script("arguments[0].click();", save_pedigree)
                    confirm_save_pedigree = self.browser.find_element_by_xpath('//button[@type="button" and @class="btn btn-success waves-effect waves-light confirmSaveBtn"]')
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
                            writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter pedigree description'])
                        self.timeout = 0
                        # stop the current test
                        return 'fail'
            # login as test user type
            self.login(action, user_type, edit_method)
            # go to approvals
            if self.click_element_by_xpath('//a[@href="/approvals/"]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to open approvals') == 'fail':
                # test failed
                return 'fail'
            # if owner/admin/breed admin, test that user can edit the approval
            if user_type in ('user', 'admin', 'breed'):
                # go to edit approval
                if self.click_element_by_xpath('//button[@class="btn btn-sm btn-outline-info mr-1" and contains(text(), "Edit")]',
                                action, user_type, edit_method, 'FAIL',
                                'Failed to edit approval') == 'fail':
                    # test failed
                    return 'fail'
                # edit approval
                while self.timeout < 20:
                    try:
                        tag_no = self.browser.find_element_by_id('id_tag_no')
                        try:
                            current_tag = int(tag_no.get_attribute('value'))
                            tag_no.clear()
                            tag_no.send_keys(current_tag + 1)
                        except ValueError:
                            tag_no.clear()
                            tag_no.send_keys(0)
                        # get date of birth
                        dob = self.browser.find_element_by_id('id_dob')
                        # increment date of registration, or default it to date of birth
                        dor = self.browser.find_element_by_id('id_dor')
                        try:
                            int_dor = int(dor.get_attribute('value').replace('-', ''))
                            # get dd,mm,yyyy, and rearrange so it can be input into the field
                            dd = f'{int_dor}'[6:]
                            mm = f'{int_dor}'[4:6]
                            yyyy = f'{int_dor}'[:4]
                            if yyyy == '2021':
                                yyyy = '2008'
                            int_dor = int(f'{dd}{mm}{yyyy}')
                            dor.clear()
                            dor.send_keys(int_dor + 1)
                        # default it to date of birth
                        except ValueError:
                            int_dob = int(dob.get_attribute('value').replace('-', ''))
                            dd = f'{int_dob}'[6:]
                            mm = f'{int_dob}'[4:6]
                            yyyy = f'{int_dob}'[:4]
                            dor.clear()
                            dor.send_keys(f'{dd}{mm}{yyyy}')
                        # set status to alive if currently dead, unknown if currently alive, and dead if currently unknown
                        dead_status = self.browser.find_element_by_id('id_status_0')
                        alive_status = self.browser.find_element_by_id('id_status_1')
                        unknown_status = self.browser.find_element_by_id('id_status_2')
                        if dead_status.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", alive_status)
                        elif alive_status.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", unknown_status)
                        else:
                            self.browser.execute_script("arguments[0].click();", dead_status)
                        # if litter size 10 set to 20, etc, and if 40 set to 10
                        litter_size = self.browser.find_element_by_id('litter_size')
                        self.browser.execute_script("arguments[0].click();", litter_size)
                        litter_size_10 = self.browser.find_element_by_xpath('//option[@value="10"]')
                        litter_size_20 = self.browser.find_element_by_xpath('//option[@value="20"]')
                        litter_size_30 = self.browser.find_element_by_xpath('//option[@value="30"]')
                        litter_size_40 = self.browser.find_element_by_xpath('//option[@value="40"]')
                        if litter_size_10.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", litter_size_20)
                        elif litter_size_20.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", litter_size_30)
                        elif litter_size_30.get_attribute('checked') != None:
                            self.browser.execute_script("arguments[0].click();", litter_size_40)
                        else:
                            self.browser.execute_script("arguments[0].click();", litter_size_10)
                        # increment date of death or set to date of birth
                        dod = self.browser.find_element_by_id('id_date_of_death')
                        try:
                            int_dod = int(dod.get_attribute('value').replace('-', ''))
                            # get dd,mm,yyyy, and rearrange so it can be input into the field
                            dd = f'{int_dod}'[6:]
                            mm = f'{int_dod}'[4:6]
                            yyyy = f'{int_dod}'[:4]
                            if yyyy == '2021':
                                yyyy = '2008'
                            int_dod = int(f'{dd}{mm}{yyyy}')
                            dod.clear()
                            dod.send_keys(int_dod + 1)
                        except ValueError:
                            int_dob = int(dob.get_attribute('value').replace('-', ''))
                            dd = f'{int_dob}'[6:]
                            mm = f'{int_dob}'[4:6]
                            yyyy = f'{int_dob}'[:4]
                            dod.clear()
                            dod.send_keys(f'{dd}{mm}{yyyy}')
                        # increment description or set to 0
                        desc = self.browser.find_element_by_id('id_description')
                        try:
                            current_desc = int(desc.text)
                            desc.clear()
                            desc.send_keys(current_desc + 1)
                        except ValueError:
                            desc.clear()
                            desc.send_keys(0)
                        # save!
                        save_pedigree = self.browser.find_element_by_xpath('//button[@type="submit" and @data-target=".confirmForm"]')
                        self.browser.execute_script("arguments[0].click();", save_pedigree)
                        confirm_save_pedigree = self.browser.find_element_by_xpath('//button[@type="button" and @class="btn btn-success waves-effect waves-light confirmSaveBtn"]')
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
                                writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter pedigree description'])
                            self.timeout = 0
                            # stop the current test
                            return 'fail'
                # go to approvals
                if self.click_element_by_xpath('//a[@href="/approvals/"]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to open approvals after edited') == 'fail':
                    # test failed
                    return 'fail'
                # check the approval is gone from the list
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//tr/td[contains(text(), "Pedigree")]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','There is an approval in the table'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test did not work
                            print("Failed to find how many approvals in the table there are", e)
                            exit(0)
            # if contributor/read-only, test that user can not edit the approval
            elif user_type in ('contrib', 'read'):
                # check user can't edit approval
                while self.timeout < 20:
                    try:
                        if len(self.browser.find_elements_by_xpath('//button[@class="btn btn-sm btn-outline-info mr-1" and contains(text(), "Edit")]')) > 0:
                            # add fail to reports file
                            with open(self.results_file, 'a+', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','User is able to go to edit approval'])
                            # stop the current test
                            return 'fail'
                        sleep(2)
                        self.timeout = 0
                        break
                    except Exception as e:
                        self.timeout += 1
                        if self.timeout == 20:
                            # test did not work
                            print("Failed to find how many editable approvals in the table there are", e)
                            exit(0)
                # login as owner to decline the edit
                self.login(action, 'user', edit_method)
                # go to approvals
                if self.click_element_by_xpath('//a[@href="/approvals/"]',
                                action, user_type, edit_method, 'FAIL',
                                'Failed to open approvals') == 'fail':
                    # test failed
                    return 'fail'
                # decline the edit
                if self.click_element_by_xpath('//button[@class="btn btn-sm btn-danger" and contains(text(), "Decline")]',
                                action, user_type, edit_method, 'FAIL',
                                'Failed to decline edit') == 'fail':
                    # test failed
                    return 'fail'
                # confirm decline<button id="declineFormSubmit" type="button" class="btn btn-danger waves-effect waves-light">Confirm decline</button>
                if self.click_element_by_xpath('//button[@class="btn btn-danger waves-effect waves-light" and contains(text(), "Confirm decline") and @id="declineFormSubmit"]',
                                action, user_type, edit_method, 'FAIL',
                                'Failed to confirm the edit declination') == 'fail':
                    # test failed
                    return 'fail'

        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'PASS','-'])

    def edit_each_breeder(self):
        self.edit_breeder('user')
        self.edit_breeder('admin')
        self.edit_breeder('breed')
        self.edit_breeder('contrib')
        self.edit_breeder('read')

    def edit_breeder(self, user_type):
        action = 'Edit Breeder'
        edit_method = 'breeder_form'

        # ensure we're logged in as the correct user
        self.login(action, user_type, edit_method)

        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # go to breeders page
        if self.click_element_by_xpath('//a[@href="/breeders/"]',
                        action, user_type, edit_method, 'FAIL',
                        'Failed to open breeders page') == 'fail':
            # test failed
            return 'fail'
        # filter for breeder ZZZZZ
        try:
            search_field = self.browser.find_element_by_xpath('//input[@type="search"][@class="form-control form-control-sm"]')
            search_field.send_keys('ZZZZZ')
        except Exception as e:
                # add fail to reports file
                with open(self.results_file, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter text in filter field'])
                # stop the current test
                return 'fail'
        # go to breeder view
        if self.click_element_by_xpath('//td[contains(text(), "ZZZZZ")]',
                        action, user_type, edit_method, 'FAIL',
                        'Failed to open breeder view') == 'fail':
            # test failed
            return 'fail'
        # if owner/admin, check user can edit breeder
        if user_type in ('user', 'admin', 'breed'):
            # go to edit breeder
            if self.click_element_by_xpath('//a[@id="editBreeder"]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to open edit breeder') == 'fail':
                # test failed
                return 'fail'
            # enter breeder info
            while self.timeout < 20:
                try:
                    # increment contact name (go through alphabet)
                    name = self.browser.find_element_by_id('id_contact_name')
                    try:
                        current_name = name.get_attribute('value')
                        name.clear()
                        name.send_keys(chr(ord(current_name) + 1))
                    except TypeError:
                        name.clear()
                        name.send_keys('a')
                    # increment address line 1
                    address1 = self.browser.find_element_by_name('address_line_1')
                    try:
                        current_address1 = address1.get_attribute('value')
                        address1.clear()
                        address1.send_keys(chr(ord(current_address1) + 1))
                    except TypeError:
                        address1.clear()
                        address1.send_keys('a')
                    # increment address line 2
                    address2 = self.browser.find_element_by_name('address_line_2')
                    try:
                        current_address2 = address2.get_attribute('value')
                        address2.clear()
                        address2.send_keys(chr(ord(current_address2) + 1))
                    except TypeError:
                        address2.clear()
                        address2.send_keys('a')
                    # increment phone number 1 (00000000000 to 99999999999 and back again)
                    phone1 = self.browser.find_element_by_id('id_phone_number1')
                    zeroes = '00000000000'
                    try:
                        current_phone1 = int(phone1.get_attribute('value'))
                        # increment
                        current_phone1 += 1
                        if len(f'{current_phone1}') <= 11:
                            # add zeroes to front of string to make it up to 11
                            pre_zeroes = zeroes[:11 - len(f'{current_phone1}')]
                            current_phone1 = f'{pre_zeroes}{current_phone1}'
                        else:
                            current_phone1 = zeroes
                        phone1.clear()
                        phone1.send_keys(current_phone1)
                    except ValueError:
                        phone1.clear()
                        phone1.send_keys(zeroes)
                    # increment phone number 2
                    phone2 = self.browser.find_element_by_id('id_phone_number2')
                    try:
                        current_phone2 = int(phone2.get_attribute('value'))
                        # increment
                        current_phone2 += 1
                        if len(f'{current_phone2}') <= 11:
                            # add zeroes to front of string to make it up to 11
                            pre_zeroes = zeroes[:11 - len(f'{current_phone2}')]
                            current_phone2 = f'{pre_zeroes}{current_phone2}'
                        else:
                            current_phone2 = zeroes
                        phone2.clear()
                        phone2.send_keys(current_phone2)
                    except ValueError:
                        phone2.clear()
                        phone2.send_keys(zeroes)
                    # increment email address
                    email = self.browser.find_element_by_id('id_email')
                    try:
                        # remove domain
                        current_email = int(email.get_attribute('value').replace('@test.com', ''))
                        email.clear()
                        # increment and enter, with domain
                        email.send_keys(f'{current_email + 1}@test.com')
                    except ValueError:
                        email.clear()
                        email.send_keys('0@test.com')
                    # set status
                    status = self.browser.find_element_by_id('id_active')
                    self.browser.execute_script("arguments[0].click();", status)
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Failed to enter breeder info'])
                        self.timeout = 0
                        # stop the current test
                        return 'fail'
            # submit breeder
            if self.click_element_by_xpath('//button[@type="submit" and @class="btn btn-success" and contains(text(), "Submit")]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to submit breeder') == 'fail':
                # test failed
                return 'fail'
            # check breeder saved by checking you can go to add breeder
            if self.click_element_by_xpath('//a[@href="/breeders/new_breeder/" and @class="btn float-right hidden-sm-down btn-success"]',
                            action, user_type, edit_method, 'FAIL',
                            'Failed to save breeder') == 'fail':
                # test failed
                return 'fail'
        
        # if contrib/read, check user can not edit breeder
        else:
            # check user can't go to edit breeder
            while self.timeout < 20:
                try:
                    if len(self.browser.find_elements_by_xpath('//a[@id="editBreeder"]')) > 0:
                        # add fail to reports file
                        with open(self.results_file, 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'FAIL','Link to edit breeder form is available'])
                        # stop the current test
                        return 'fail'
                    sleep(2)
                    self.timeout = 0
                    break
                except Exception as e:
                    self.timeout += 1
                    if self.timeout == 20:
                        # test failed
                        print("Failed to find how many links to edit breeder form there are", e)
                        exit(0)

        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([action,user_type.replace('_', ' '),edit_method.replace('_', ' '),'PASS','-'])

    def run_coi(self):
        action = 'Run COI'
        user_type = 'admin'
        scenario = 'metrics_page'

        # ensure we're logged in as the correct user
        self.login(action, user_type, scenario)
        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # go to metrics page
        if self.click_element_by_xpath('//a[@href="/metrics/"]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to open metrics page') == 'fail':
            # test failed
            return 'fail'
        sleep(2)
        # run coi
        if self.click_element_by_xpath('//button[@id="coiBtn"]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to click run coi button') == 'fail':
            # test failed
            return 'fail'
        # try click a breed
        if self.click_element_by_xpath('//div[@class="dropdown-menu show"]/button[contains(text(), "Old English Goat")]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to click run coi button for a OEGs') == 'fail':
            # test failed
            return 'fail'

        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'PASS','-'])

    def run_mean_kinship(self):
        action = 'Run Mean Kinship'
        user_type = 'admin'
        scenario = 'metrics_page'

        # ensure we're logged in as the correct user
        self.login(action, user_type, scenario)
        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # go to metrics page
        if self.click_element_by_xpath('//a[@href="/metrics/"]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to open metrics page') == 'fail':
            # test failed
            return 'fail'
        sleep(2)

        # run mk
        if self.click_element_by_xpath('//button[@id="meanKinshipBtn"]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to click run mk button') == 'fail':
            # test failed
            return 'fail'
        # try click a breed
        if self.click_element_by_xpath('//div[@class="dropdown-menu show"]/button[contains(text(), "Old English Goat")]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to click run mk button for a OEGs') == 'fail':
            # test failed
            return 'fail'

        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'PASS','-'])

    def stud_advisor(self):
        action = 'Stud Advisor'
        user_type = 'admin'
        scenario = 'metrics_page'

        # ensure we're logged in as the correct user
        self.login(action, user_type, scenario)
        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # go to metrics page
        if self.click_element_by_xpath('//a[@href="/metrics/"]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to open metrics page') == 'fail':
            # test failed
            return 'fail'
        sleep(2)

        # find stud advisor note
        try:
            results_note = self.browser.find_element_by_id("saMsg")
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to find stud advisor note'])
            # stop the current test
            return 'fail'
        # check that note is empty
        if len(results_note.text) > 0:
            # add fail to reports
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action, user_type.replace('_', ' '), scenario.replace('_', ' '), 'FAIL', 'Stud advisor message was displayed prematurely'])
            self.timeout = 0
            # stop the current test
            return 'fail'
        # enter reg number
        female = 'XL11341'
        try:
            sa_field = self.browser.find_element_by_xpath('//input[@id="sa_mother"]')
            sa_field.send_keys(female)
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to enter text in stud advisor field'])
            # stop the current test
            return 'fail'
        # run stud advisor
        if self.click_element_by_xpath('//button[@id="saBtn" and contains(text(), "Run Advisor")]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to run stud advisor') == 'fail':
            # test failed
            return 'fail'
        sleep(2)
        # check presence of note informing the user that sa added to results queue
        if len(results_note.text) == 0:
            # add fail to reports
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action, user_type.replace('_', ' '), scenario.replace('_', ' '), 'FAIL', 'Stud advisor message was not displayed'])
            self.timeout = 0
            # stop the current test
            return 'fail'
        # check that button to view results is present and disabled
        try:
            self.browser.find_element_by_xpath(f'//td[contains(text(), "Stud Advisor: {female}")]/following-sibling::td/button[@class="btn btn-info" and @disabled="" and contains(text(), "View")]')
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to find view button'])
            # stop the current test
            return 'fail'
        # after 10 minutes try to click the view button
        sleep(1200)
        if self.click_element_by_xpath(f'//td[contains(text(), "Stud Advisor: {female}")]/following-sibling::td/a/button[@class="btn btn-info" and contains(text(), "View")]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to go to results') == 'fail':
            # test failed
            return 'fail'
        # check we're on results page

        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'PASS','-'])

    def kinship(self):
        action = 'Kinship'
        user_type = 'admin'
        scenario = 'metrics_page'

        # ensure we're logged in as the correct user
        self.login(action, user_type, scenario)
        self.browser.get(self.config['settings']['domain'] + "/account/welcome")

        # go to metrics page
        if self.click_element_by_xpath('//a[@href="/metrics/"]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to open metrics page') == 'fail':
            # test failed
            return 'fail'
        sleep(2)

        # find kinship note
        try:
            results_note = self.browser.find_element_by_id("ksMsg")
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to find kinship note'])
            # stop the current test
            return 'fail'
        # check that note is empty
        if len(results_note.text) > 0:
            # add fail to reports
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action, user_type.replace('_', ' '), scenario.replace('_', ' '), 'FAIL', 'Kinship message was displayed prematurely'])
            self.timeout = 0
            # stop the current test
            return 'fail'
        # enter mother number
        mother = 'XL11341'
        try:
            kin_field = self.browser.find_element_by_xpath('//input[@id="id_mother"]')
            kin_field.send_keys(mother)
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to enter text in mother kinship field'])
            # stop the current test
            return 'fail'
        # enter father number
        father = 'L17983'
        try:
            kin_field = self.browser.find_element_by_xpath('//input[@id="id_father"]')
            kin_field.send_keys(father)
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to enter text in father kinship field'])
            # stop the current test
            return 'fail'
        # run kinship
        if self.click_element_by_xpath('//button[@id="ksBtn" and contains(text(), "Calculate Kinship")]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to run kinship') == 'fail':
            # test failed
            return 'fail'
        sleep(2)
        # check presence of note informing the user that sa added to results queue
        if len(results_note.text) == 0:
            # add fail to reports
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action, user_type.replace('_', ' '), scenario.replace('_', ' '), 'FAIL', 'Kinship message was not displayed'])
            self.timeout = 0
            # stop the current test
            return 'fail'
        # check that button to view results is present and disabled
        try:
            self.browser.find_element_by_xpath(f'//td[contains(text(), "Kinship: {mother} + {father}")]/following-sibling::td/button[@class="btn btn-info" and @disabled="" and contains(text(), "View")]')
        except Exception as e:
            # add fail to reports file
            with open(self.results_file, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'FAIL','Failed to find view button'])
            # stop the current test
            return 'fail'
        # after 10 minutes try to click the view button
        sleep(600)
        if self.click_element_by_xpath(f'//td[contains(text(), "Kinship: {mother} + {father}")]/following-sibling::td/a/button[@class="btn btn-info" and contains(text(), "View")]',
                        action, user_type, scenario, 'FAIL',
                        'Failed to go to results') == 'fail':
            # test failed
            return 'fail'
        # check we're on results page

        # test must have passed if we have got to the end of this function
        with open(self.results_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([action,user_type.replace('_', ' '),scenario.replace('_', ' '),'PASS','-'])

    def test(self,type,option=""):
        if type == 'login_user':
            self.login('Main Login Test', 'user', 'Main Login Test')
        if type == 'login_admin':
            self.login('Main Login Test', 'admin', 'Main Login Test')
        if type == 'login_breed':
            self.login('Main Login Test', 'breed', 'Main Login Test')
        if type == 'login_contrib':
            self.login('Main Login Test', 'contrib', 'Main Login Test')
        if type == 'login_read':
            self.login('Main Login Test', 'read', 'Main Login Test')
        if type == 'logout':
            self.logout()
        elif type == 'add_each_pedigree':
            self.add_each_pedigree('pedigree.csv')
        elif type == 'add_each_breeder':
            self.add_each_breeder('breeder.csv')
        elif type == 'edit_each_pedigree':
            self.edit_each_pedigree()
        elif type == 'edit_each_breeder':
            self.edit_each_breeder()
        elif type == 'run_coi':
            self.run_coi()
        elif type == 'run_mean_kinship':
            self.run_mean_kinship()
        elif type == 'stud_advisor':
            self.stud_advisor()
        elif type == 'kinship':
            self.kinship()
        elif type == 'complete':
            self.login('Main Login Test', 'user', 'Main Login Test')
            self.login('Main Login Test', 'admin', 'Main Login Test')
            self.login('Main Login Test', 'breed', 'Main Login Test')
            self.login('Main Login Test', 'contrib', 'Main Login Test')
            self.login('Main Login Test', 'read', 'Main Login Test')
            self.logout()
            self.add_each_pedigree('pedigree.csv')
            self.add_each_breeder('breeder.csv')
            self.edit_each_pedigree()
            self.edit_each_breeder()
            self.run_coi()
            self.run_mean_kinship()
            self.stud_advisor()
            self.kinship()


if __name__ == '__main__':
    obj = CloudLinesTestV2()
    print("1. Login as User/Owner")
    print("2. Login as Admin")
    print("3. Login as Breed")
    print("4. Login as Contributor")
    print("5. Login as Read-Only")
    print("6. Logout")
    print("7. Add Pedigree")
    print("8. Add Breeder")
    print("9. Edit Pedigree")
    print("10. Edit Breeder")
    print("11. Run COI")
    print("12. Run Mean Kinship")
    print("13. Stud Advisor")
    print("14. Kinship")
    print("15. Complete Test")
    print("_. Exit")
    ch = input("Enter Choice ")
    while ch != '_':
        try:
            if ch == "1":
                obj.test('login_user')
            if ch == "2":
                obj.test('login_admin')
            if ch == "3":
                obj.test('login_breed')
            if ch == "4":
                obj.test('login_contrib')
            if ch == "5":
                obj.test('login_read')
            if ch == "6":
                obj.test('logout')
            elif ch =="7":
                obj.test('add_each_pedigree')
            elif ch == "8":
                obj.test('add_each_breeder')
            elif ch == "9":
                obj.test('edit_each_pedigree')
            elif ch == "10":
                obj.test('edit_each_breeder')
            elif ch == "11":
                obj.test('run_coi')
            elif ch == "12":
                obj.test('run_mean_kinship')
            elif ch == "13":
                obj.test('stud_advisor')
            elif ch == "14":
                obj.test('kinship')
            elif ch == "15":
                obj.test('complete')
            ch = input("Enter Choice ")
        except:
            break