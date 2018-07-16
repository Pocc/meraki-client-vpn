#!/usr/bin/python3

# Library imports
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QMessageBox
from PyQt5.QtGui import QIcon
from sys import platform
from os import system

# Local imports
from src.modules.modal_dialogs import error_dialog, feature_in_development
from src.modules.pyinstaller_path_helper import resource_path

# This should run after a connection has resulted in failure


class TroubleshootVpnFailure:
    def __init__(self):
        super(TroubleshootVpnFailure, self).__init__()
        # TODO REQUIRED VARS #################################################
        self.fw_status_text = ''
        self.ddns_address = ''
        self.firewall_ip = ''
        self.client_vpn_text = ''
        # TODO ###############################################################
        """
        This method will check all of these values and show which are invalid
        User should not be able to connect if there are any tests that fail (i.e grayed out button)
        Each test should be clickable so that the user can find out more information
        """
        self.validation_list = QListWidget()
        self.validation_textlist = [
            "Is the MX online?",
            "Can the client ping the firewall's public IP?",
            "Is the user behind the firewall?",
            "Is Client VPN enabled?",
            "Is authentication type Meraki Auth?",
            "Are UDP ports 500/4500 port forwarded through firewall?"]
        # "Is the user authorized for Client VPN?",
        self.has_passed_validation = [True] * 6  # False for failed, True for passed
        for i in range(len(self.validation_textlist)):  # For as many times as items in the validation_textlist
            item = QListWidgetItem(self.validation_textlist[i])  # Initialize a QListWidgetItem out of a string
            self.validation_list.addItem(item)  # Add the item to the QListView

        self.run_tests()

    def run_tests(self):
        # Go through tests and then show results
        self.test0_is_mx_online()
        self.test1_is_fw_reachable()
        self.test2_is_user_behind_fw()
        self.test3_is_client_vpn_enabled()
        self.test4_is_auth_type_meraki()
        self.test5_incompatible_port_forwards()

        self.show_results()

    def test0_is_mx_online(self):
        # Tests whether there is an MX in the appliance network
        is_online_status_code = int(self.fw_status_text[self.fw_status_text.find("status#") + 9])
        # Default for has_passed_validation is true, so else isn't necessary
        if is_online_status_code != 0:  # 0 is online, 2 is unreachable. There are probably other statuses
            self.has_passed_validation[0] = False

        """ try except clause will be more useful if we know exactly which error it causes so we can except it
        try:
        except:
            # No 'status#' in HTML means there is no firewall in that network
            error_dialog("There is no device in this network!")
        """

    def test1_is_fw_reachable(self):
        # Verify
        # Ping 4 times
        if platform == 'win32':  # Identifies any form of Windows
            ping_string = "ping " + self.ddns_address  # ping 4 times every 1000ms
        else:  # *nix of some kind
            ping_string = "ping -c 5 -i 0.2 " + self.ddns_address  # ping 4 times every 200ms
        ping_response = system(ping_string)
        if ping_response != 0:  # Ping responses other than 0 mean failure. Error codes are OS-dependent
            self.has_passed_validation[1] = False
            # Failure error dialog and then return
            error_dialog("Cannot connect to device!")

    def test2_is_user_behind_fw(self):
        # *** TEST 2 ***
        # Is the user behind the firewall?
        # This IP is the source public IP that the user is connecting with
        ip_start = self.fw_status_text.find("\"request_ip\":") + 14  # Start of IP position
        ip_end = self.fw_status_text[ip_start:].find('\"') + ip_start  # Get the position of the IP end quote
        src_public_ip = self.fw_status_text[ip_start:ip_end]
        # If public IP address of client == MX IP
        # Then the user is behind their firewall and client vpn won't work
        if src_public_ip == self.firewall_ip:
            self.has_passed_validation[2] = False

        """try except clause will be more useful if we know what type of error to except    
        try:
        except:
        #    error_dialog("Exception during source public IP == MX IP test")
        """

    def test3_is_client_vpn_enabled(self):
        # *** TEST 3 ***
        # Is Client VPN enabled?
        if self.client_vpn_text[self.client_vpn_text.find(",\"client_vpn_enabled\"") + 22] != 't':
            self.has_passed_validation[3] = False

    def test4_is_auth_type_meraki(self):
        # *** TEST 4 ***
        # Authentication type is Meraki Auth?
        # User fixes (for now)
        """ When an auth type is selected, we get one of these in the client VPN HTML depending on user's auth choice:
        Meraki cloud</option></select>
        Active Directory</option></select>
        RADIUS</option></select>
        """
        # String find returns -1 if the string isn't found
        meraki_select_type1 = self.client_vpn_text.find('Meraki cloud</option></select>')
        meraki_select_type2 = self.client_vpn_text.find('<option value="meraki" selected="selected">')
        if meraki_select_type1 == -1 and meraki_select_type2 == -1:
            self.has_passed_validation[4] = False
            error_dialog("ERROR: Please select Meraki cloud authentication")

    def test5_incompatible_port_forwards(self):
        # *** TEST 5 ***
        """
        If the following text exists, they're port forwarding ports 500 or 4500:
        "public_port":"500"
        "public_port":"4500"
        """
        # -1 is returned by string find if a match is not found
        is_forwarding_500 = self.client_vpn_text.find('"public_port":"500"') != -1
        is_forwarding_4500 = self.client_vpn_text.find('"public_port":"4500"') != -1
        if is_forwarding_500:
            error_dialog("ERROR: You are forwarding port 500!")
            self.has_passed_validation[5] = False

        if is_forwarding_4500:
            error_dialog("ERROR: You are forwarding port 4500!")
            self.has_passed_validation[5] = False

        # *** TEST 6 *** : CURRENTLY ON HOLD
        # Is user authorized for Client VPN?
        # By definition, if you can log in as a user, you have a user in the Client VPN users page

        # This is the only test which requires us to scrape data from a table. Tables in dashboard use javascript,
        # So we need to scrape differently.
        # https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
        """ from selenium import webdriver
         from selenium.webdriver.chrome.options import Options
         options = Options()
         options.add_argument('--headless')
         # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
         driver = webdriver.Chrome('/usr/bin/google-chrome', chrome_options=options)
         driver.get(self.client_vpn_url)
         print(driver.find_elements_by_css_selector('td.ft.notranslate.email'))
        """

    def show_results(self):
        # ----------------------------------------------
        # Add checkboxes/x-marks to each validation test
        for i in range(len(self.validation_textlist)):
            print("has passed" + str(i) + str(self.has_passed_validation[i]))
            if self.has_passed_validation[i]:
                self.validation_list.item(i).setIcon(QIcon(resource_path('src/media/checkmark-16.png')))
            else:
                self.validation_list.item(i).setIcon(QIcon(resource_path('src/media/x-mark-16.png')))

            # All the error messages! Once we know what the error dialog landscape looks like down here,
            # we might want to turn this into an error method with params
        if not self.has_passed_validation[3]:
            self.validation_list.item(3).setIcon(QIcon(resource_path('src/media/x-mark-16.png')))
            # Error message popup that will take control and that the user will need to acknowledge
            force_enable_client_vpn = error_dialog('Client VPN is not enabled in Dashboard for this network.'
                                                   '\nWould you like this program to enable it for you?')
            if force_enable_client_vpn == QMessageBox.Yes:
                self.enable_client_vpn()

    @staticmethod
    def enable_client_vpn():
        feature_in_development()
        pass