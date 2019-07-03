# Multiple Inventories


Q: Does Ansible consume group\_vars from all inventories?

A: Yes, although it does warn if there is no inventory file.

Q: If a variable is defined in both places, which wins?

A: Variables in inventories specified via later `-i` arguments win.

```
ansible-playbook -i inventory/common -i inventory/prod site.yml

 [WARNING]: Unable to parse /home/mark/src/ansible-experiments/01-multiple-inventories/inventory/common as an inventory source

 [WARNING]: Unable to parse /home/mark/src/ansible-experiments/01-multiple-inventories/inventory/common as an inventory source


PLAY [localhost] *******************************************************************************************************************************************************************************************

TASK [display hostvars] ************************************************************************************************************************************************************************************
ok: [localhost] => {
    "hostvars": {
        "localhost": {
			...
            "variable_defined_in_both": "prod",
            "variable_defined_in_common": true, 
            "variable_defined_in_prod": true
        }
    }
}

PLAY RECAP *************************************************************************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0   
```
