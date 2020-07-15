from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException


class cloudlinesTest():
    def __init__(self):
        self.username = 'username'
        self.password = 'password'

        self.browser = webdriver.Chrome('chromedriver/path')
        self.browser.get('https://dev.cloud-lines.com')

        self.pedigree = {'breeder': 'Test Breeder',
                         'reg_no': 'ABC12345',
                         'tag_no': 'TAG12345',
                         'name': 'Test Pedigree',
                         'dor': '01/02/2019',
                         'dob': '01/02/2019',
                         'status': 'id_status_0',
                         'sex': 'id_sex_0',
                         'dod': '01/03/2010',
                         'mother': '',
                         'mother_notes': '',
                         'father': '',
                         'father_notes': '',
                         'desc': """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.""",
                         'breed': 'Test Breed',
        }
        self.breeder = {'breeding_prefix': 'Test Breeder',
                         'contact_name': 'Test Contact',
                         'address': ' Test Street',
                         'phone_number1': '0123456789',
                         'phone_number2': '0987654321',
                         'email': 'test@test.com',
                         }
        self.breed = {'breed_name': 'Test Breed',
                       'desc': """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.""",
                       }

        self.user = {'first_name': 'firstname',
                     'second_name': 'secondName',
                     'username': 'testuser',
                     'email': 'testuser@test.com',
                     }

    def test(self):
        self.login()
        for inc in range(0, 10):
            self.add_pedigree(self.pedigree, self.breeder, self.breed, str(inc))

        self.site_settings(self.user)


        # DELETE EVERYTHING
        self.delete_all_pedigrees()
        self.delete_all_breeders()
        self.delete_all_breeds()
        self.delete_all_users()

        self.add_breeders()
        self.add_breed()
        self.delete_all_breeders()
        self.delete_all_breeds()


        self.logout()

    def login(self):
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password)
        login = self.browser.find_element_by_id('loginBtn')
        self.browser.execute_script("arguments[0].click();", login)

    def logout(self):
        logout = self.browser.find_element_by_xpath('//a[@href="'+'/account/logout'+'"]')
        self.browser.execute_script("arguments[0].click();", logout)

    def add_pedigree(self, pedigree, breeder, breed, inc):
        # go to pedigree search page
        pedigree_link = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/search' + '"]')
        self.browser.execute_script("arguments[0].click();", pedigree_link)

        # go to add new pedigree
        new_pedigree = self.browser.find_element_by_xpath('//a[@href="' + '/pedigree/new_pedigree/' + '"]')
        self.browser.execute_script("arguments[0].click();", new_pedigree)

        # open add new breeder modal
        new_breeder_modal = self.browser.find_element_by_id('showNewBreederModal')
        self.browser.execute_script("arguments[0].click();", new_breeder_modal)
        # Enter breeder information
        sleep(1)
        self.add_breeder_info(breeder, inc)
        submit_breeder = self.browser.find_element_by_id('saveBreeder')
        self.browser.execute_script("arguments[0].click();", submit_breeder)
        sleep(1)

        # Enter pedigree information
        breeder = self.browser.find_element_by_id('id_breeder')
        breeder.send_keys(pedigree['breeder'] + inc)
        current_owner = self.browser.find_element_by_id('id_current_owner')
        current_owner.send_keys(pedigree['breeder'] + inc)
        self.browser.find_element_by_name('reg_no').clear()
        reg_no = self.browser.find_element_by_name('reg_no')
        reg_no.send_keys(pedigree['reg_no'] + inc)
        tag_no = self.browser.find_element_by_id('id_tag_no')
        tag_no.send_keys(pedigree['tag_no'] + inc)
        name = self.browser.find_element_by_id('id_name')
        name.send_keys(pedigree['name'] + inc)
        dor = self.browser.find_element_by_id('id_date_of_registration')
        dor.send_keys(pedigree['dor'])
        dob = self.browser.find_element_by_id('id_date_of_birth')
        dob.send_keys(pedigree['dob'])
        status = self.browser.find_element_by_id(pedigree['status'])
        self.browser.execute_script("arguments[0].click();", status)
        sex = self.browser.find_element_by_id(pedigree['sex'])
        self.browser.execute_script("arguments[0].click();", sex)
        dod = self.browser.find_element_by_id('id_date_of_death')
        dod.send_keys(pedigree['dod'])
        desc = self.browser.find_element_by_id('id_description')
        desc.send_keys(pedigree['desc'])

        if inc == '0':
            # open add new breed modal
            new_breed_modal = self.browser.find_element_by_id('showNewBreedModal')
            self.browser.execute_script("arguments[0].click();", new_breed_modal)
            # Enter breeder information
            sleep(1)
            self.add_breed_info(breed)
            submit_breed = self.browser.find_element_by_id('saveBreed')
            self.browser.execute_script("arguments[0].click();", submit_breed)
            sleep(1)
        else:
            try:
                breed = self.browser.find_element_by_id('id_breed')
                breed.send_keys(pedigree['breed'])
            except ElementNotInteractableException:
                # means only one breed can be added to it's greyed out
                pass

        # Save!
        save_pedigree = self.browser.find_element_by_id('submitPedigree')
        self.browser.execute_script("arguments[0].click();", save_pedigree)

    def add_breeder_info(self, breeder, inc):
        # Enter breeder information
        breeding_prefix = self.browser.find_element_by_name('breeding_prefix')
        breeding_prefix.send_keys(breeder['breeding_prefix'] + inc)
        contact_name = self.browser.find_element_by_name('contact_name')
        contact_name.send_keys(breeder['contact_name'] + inc)
        address = self.browser.find_element_by_name('address')
        address.send_keys(inc + breeder['address'])
        phone_number1 = self.browser.find_element_by_name('phone_number1')
        phone_number1.send_keys(breeder['phone_number1'])
        phone_number2 = self.browser.find_element_by_name('phone_number2')
        phone_number2.send_keys(breeder['phone_number2'])
        email = self.browser.find_element_by_name('email')
        email.send_keys(inc + breeder['email'])
        active = self.browser.find_element_by_name('active')
        self.browser.execute_script("arguments[0].click();", active)

    def add_breed_info(self, breed, inc=''):
        # Enter breed information
        breed_name = self.browser.find_element_by_name('breed_name')
        breed_name.send_keys(breed['breed_name'] + inc)
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

    def delete_all_breeders(self):
        # go to breeder page
        breeder_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeders/' + '"]')
        self.browser.execute_script("arguments[0].click();", breeder_link)

        while self.browser.find_elements_by_class_name('sorting_1'):
            breeder_links = self.browser.find_elements_by_class_name('sorting_1')
            self.browser.execute_script("arguments[0].click();", breeder_links[0])
            self.delete_breeder()
            breeder_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeders/' + '"]')
            self.browser.execute_script("arguments[0].click();", breeder_link)

    def delete_breeder(self):
        # ensure you're on the right page before calling this method
        edit_breeder = self.browser.find_element_by_id('editBreeder')
        self.browser.execute_script("arguments[0].click();", edit_breeder)
        delete_breeder = self.browser.find_element_by_id('deleteBreeder')
        self.browser.execute_script("arguments[0].click();", delete_breeder)
        sleep(1)
        confirm_delete_breeder = self.browser.find_element_by_name('delete')
        self.browser.execute_script("arguments[0].click();", confirm_delete_breeder)
        sleep(1)

    def delete_all_breeds(self):
        # go to breed page
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
        sleep(1)
        confirm_delete_breed = self.browser.find_element_by_name('delete')
        self.browser.execute_script("arguments[0].click();", confirm_delete_breed)
        sleep(1)

    def site_settings(self, usr):
        site_settings = self.browser.find_element_by_xpath('//a[@href="' + '/account/settings' + '"]')
        self.browser.execute_script("arguments[0].click();", site_settings)

        users_tab = self.browser.find_element_by_xpath('//a[@href="' + '#users' + '"]')
        self.browser.execute_script("arguments[0].click();", users_tab)

        for inc in range(0, 5):
            create_new = self.browser.find_element_by_id('createNew')
            self.browser.execute_script("arguments[0].click();", create_new)
            sleep(1)
            self.add_user(usr, str(inc))
            site_settings = self.browser.find_element_by_xpath('//a[@href="' + '/account/settings' + '"]')
            self.browser.execute_script("arguments[0].click();", site_settings)
            users_tab = self.browser.find_element_by_xpath('//a[@href="' + '#users' + '"]')
            self.browser.execute_script("arguments[0].click();", users_tab)

    def add_user(self, usr, inc):
        first_name = self.browser.find_element_by_id('firstName')
        first_name.send_keys(usr['first_name'])
        last_name = self.browser.find_element_by_id('lastName')
        last_name.send_keys(usr['second_name'])
        username = self.browser.find_element_by_id('register-form-username')
        username.send_keys(usr['username'] + inc)
        email = self.browser.find_element_by_id('register-form-email')
        email.send_keys(inc + usr['email'])
        add_user = self.browser.find_element_by_id('userFormBtn')
        self.browser.execute_script("arguments[0].click();", add_user)

    def delete_all_users(self):
        site_settings = self.browser.find_element_by_xpath('//a[@href="' + '/account/settings' + '"]')
        self.browser.execute_script("arguments[0].click();", site_settings)

        users_tab = self.browser.find_element_by_xpath('//a[@href="' + '#users' + '"]')
        self.browser.execute_script("arguments[0].click();", users_tab)
        try:
            while self.browser.find_element_by_id('userDeleteBtn'):
                delete_button = self.browser.find_elements_by_id('userDeleteBtn')
                self.browser.execute_script("arguments[0].click();", delete_button[0])
                confirm_delete_user = self.browser.find_element_by_name('delete')
                self.browser.execute_script("arguments[0].click();", confirm_delete_user)
                sleep(1)
                users_tab = self.browser.find_element_by_xpath('//a[@href="' + '#users' + '"]')
                self.browser.execute_script("arguments[0].click();", users_tab)
        except NoSuchElementException:
            pass

    def add_breeders(self):
        breeder_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeders/' + '"]')
        self.browser.execute_script("arguments[0].click();", breeder_link)

        for inc in range(0, 10):
            add_new_breeder_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeders/new_breeder/' + '"]')
            self.browser.execute_script("arguments[0].click();", add_new_breeder_link)

            self.add_breeder_info(self.breeder, str(inc))

            save_breed = self.browser.find_element_by_class_name('btn-success')
            self.browser.execute_script("arguments[0].click();", save_breed)

    def add_breed(self):
        breed_link = self.browser.find_element_by_xpath('//a[@href="' + '/breeds/' + '"]')
        self.browser.execute_script("arguments[0].click();", breed_link)

        for inc in range(0, 10):
            add_new_breed = self.browser.find_element_by_class_name('btn-success')
            self.browser.execute_script("arguments[0].click();", add_new_breed)

            self.add_breed_info(self.breed, str(inc))

            save_new_breed = self.browser.find_element_by_class_name('btn-success')
            self.browser.execute_script("arguments[0].click();", save_new_breed)


if __name__ == '__main__':
    cloudlinesTest().test()
