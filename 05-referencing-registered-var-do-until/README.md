# Referencing registered variables in do-until loops

Q: Can I reference a registered variable in a do-until loop?

A: Yes. However, referencing via an intermediate task variable fails until Ansible 2.8.

2.7:
```
ansible-playbook site.yml
 [WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'


 PLAY [localhost] *******************************************************************************************************************************************************************************************

 TASK [command] *********************************************************************************************************************************************************************************************
 changed: [localhost]

 TASK [command] *********************************************************************************************************************************************************************************************
 fatal: [localhost]: FAILED! => {"msg": "The field 'vars' has an invalid value, which includes an undefined variable. The error was: 'result2' is undefined\n\nThe error appears to have been in '/home/mark/src/ansible-experiments/05-referencing-registered-var/site.yml': line 11, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n    # Does not work\n    - command: echo hi\n      ^ here\n"}
    to retry, use: --limit @/home/mark/src/ansible-experiments/05-referencing-registered-var/site.retry

    PLAY RECAP *************************************************************************************************************************************************************************************************
    localhost                  : ok=1    changed=1    unreachable=0    failed=1   
```

2.8:
```
ansible-playbook site.yml
 [WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'


 PLAY [localhost] *******************************************************************************************************************************************************************************************

 TASK [command] *********************************************************************************************************************************************************************************************
 changed: [localhost]

 TASK [command] *********************************************************************************************************************************************************************************************
 changed: [localhost]

 PLAY RECAP *************************************************************************************************************************************************************************************************
 localhost                  : ok=2    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

