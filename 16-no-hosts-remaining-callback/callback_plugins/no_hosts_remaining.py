from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'no_hosts_remaining'
    CALLBACK_NEEDS_ENABLED = False

    def v2_playbook_on_no_hosts_remaining(self):
        print("NO HOSTS REMAINING!")
