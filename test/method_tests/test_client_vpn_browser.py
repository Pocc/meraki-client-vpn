# -*- coding: utf-8 -*-
# Copyright 2018 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test dashboard browser class."""
import unittest
from merlink.browsers.client_vpn import ClientVpnBrowser


class TestClientVpnBrowser(unittest.TestCase):
    """Test the dashboard browser class."""

    @staticmethod
    def set_up():
        """Set up the test."""
        pass

    @staticmethod
    def test_a_fn():
        """Test these functions... eventually.
        'check_firewall_connectivity',
        'check_firewall_page_errors',
        'check_nat_rules',
        'get_client_vpn_address',
        'get_client_vpn_data',
        'get_client_vpn_psk',
        'is_client_vpn_enabled',
        'troubleshoot_client_vpn'
        """
        browser = ClientVpnBrowser()
        browser.org_data_setup()


if __name__ == '__main__':
    unittest.main()
