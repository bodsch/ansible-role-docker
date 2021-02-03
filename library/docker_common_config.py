#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os
import json
import hashlib

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

# ---------------------------------------------------------------------------------------


class DockerCommonConfig(object):
    """
      Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self):
        """
          Initialize all needed Variables
        """
        self.state = module.params.get("state")
        #
        self.log_driver = module.params.get("log_driver")
        self.log_opts = module.params.get("log_opts")
        self.log_level = module.params.get("log_level")
        self.data_root = module.params.get("data_root")
        self.max_concurrent_downloads = module.params.get("max_concurrent_downloads")
        self.max_concurrent_uploads = module.params.get("max_concurrent_uploads")
        self.debug = module.params.get("debug")
        self.selinux_enabled = module.params.get("selinux_enabled")
        self.experimental = module.params.get("experimental")
        self.group = module.params.get("group")
        self.bridge = module.params.get("bridge")
        self.bip = module.params.get("bip")
        self.ip = module.params.get("ip")
        self.fixed_cidr = module.params.get("fixed_cidr")
        self.fixed_cidr_v6 = module.params.get("fixed_cidr_v6")
        self.default_gateway = module.params.get("default_gateway")
        self.default_gateway_v6 = module.params.get("default_gateway_v6")
        self.insecure_registries = module.params.get("insecure_registries")

        self.config_file = "/etc/docker/daemon.json"
        self.config_checksum = "/etc/docker/.checksum"

    def run(self):
        """
            run
        """
        if(self.state == 'absent'):
            """
                remove created files
            """
            if(os.path.isfile(self.config_file)):
                os.remove(self.config_file)

            if(os.path.isfile(self.config_checksum)):
                os.remove(self.config_checksum)

            return dict(
                changed = True,
                failed = False,
                msg = "config removed"
            )

        _old_checksum = ''
        _data_changed = False

        data = dict()

        if(self.log_driver):
            data["log-driver"] = self.log_driver

        if(self.log_opts):
            data["log-opts"] = self.log_opts

        if(self.log_level):
            data["log-level"] = self.log_level

        if(self.data_root):
            data["data-root"] = self.data_root

        if(self.max_concurrent_downloads):
            data["max-concurrent-downloads"] = self.max_concurrent_downloads

        if(self.max_concurrent_uploads):
            data["max-concurrent-uploads"] = self.max_concurrent_uploads

        if(self.debug):
            data["debug"] = self.debug

        if(self.selinux_enabled):
            data["selinux-enabled"] = self.selinux_enabled

        if(self.experimental):
            data["experimental"] = self.experimental

        if(self.group):
            data["group"] = self.group

        if(self.bridge):
            data["bridge"] = self.bridge

        if(self.bip):
            data["bip"] = self.bip

        if(self.ip):
            data["ip"] = self.ip

        if(self.fixed_cidr):
            data["fixed-cidr"] = self.fixed_cidr

        if(self.fixed_cidr_v6):
            data["fixed-cidr-v6"] = self.fixed_cidr_v6

        if(self.default_gateway):
            data["default-gateway"] = self.default_gateway

        if(self.default_gateway_v6):
            data["default-gateway-v6"] = self.default_gateway_v6

        if(self.insecure_registries):
            data["insecure-registries"] = self.insecure_registries

        # create checksum of our data
        _checksum = self.__checksum(json.dumps(data, sort_keys=True))

        if(os.path.isfile(self.config_checksum)):
            with open(self.config_checksum, "r") as _sum:
                _old_checksum = _sum.readlines()[0]

        # compare both checksums
        if(_old_checksum != _checksum):
            with open(self.config_file, 'w') as fp:
                json.dump(data, fp, indent=2, sort_keys=False)

            with open(self.config_checksum, 'w') as fp:
                fp.write(_checksum)

            _data_changed = True

        return dict(
            changed = _data_changed,
            failed = False,
            msg = "config created"
        )

    def __checksum(self, plaintext):
        """
            create checksum from string
        """
        password_bytes = plaintext.encode('utf-8')
        password_hash = hashlib.sha256(password_bytes)
        checksum = password_hash.hexdigest()

        return checksum


# ---------------------------------------------------------------------------------------
# Module execution.
#

def main():
    global module
    module = AnsibleModule(
        argument_spec = dict(
            state = dict(default="present", choices=["absent", "present"]),
            #
            log_driver = dict(required=False, type='str'),
            log_opts = dict(required=False, type='dict'),
            log_level = dict(required=False, type='str'),
            data_root = dict(required=False, type='str'),
            max_concurrent_downloads = dict(required=False, type="int"),
            max_concurrent_uploads = dict(required=False, type='int'),
            debug = dict(required=False, type="bool", default=False),
            selinux_enabled = dict(required=False, type="bool", default=False),
            experimental = dict(required=False, type="bool", default=False),
            group = dict(required=False, type='str'),
            bridge = dict(required=False, type='str'),
            bip = dict(required=False, type='str'),
            ip = dict(required=False, type='str'),
            fixed_cidr = dict(required=False, type='str'),
            fixed_cidr_v6 = dict(required=False, type='str'),
            default_gateway = dict(required=False, type='str'),
            default_gateway_v6 = dict(required=False, type='str'),
            insecure_registries = dict(required=False, type='list'),
        ),
        supports_check_mode = True,
    )

    dcc = DockerCommonConfig()
    result = dcc.run()

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
