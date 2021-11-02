# Fatal errors

How can we control whether errors are fatal?

We have `any_errors_fatal` and `max_fail_percentage`. Is it possible to
template these parameters?

`any_errors_fatal` cannot be templated:

```
ansible-playbook -i inventory any-errors-fatal.yml
PLAY [any_errors_fatal cannot be templated] **************************************

TASK [Fail one host] *************************************************************
fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
skipping: [h3]
skipping: [h1]

NO MORE HOSTS LEFT ***************************************************************

PLAY RECAP ***********************************************************************
h1                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
h3                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

`max_fail_percentage` can be templated:

```
ansible-playbook -i inventory max-fail-percentage.yml 
PLAY [max_fail_percentage can be templated] **************************************

TASK [Fail one host] *************************************************************
fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
skipping: [h3]
skipping: [h1]

TASK [Nobody gets here] **********************************************************
ok: [h3] => {
    "msg": "Hello world!"
}
ok: [h1] => {
    "msg": "Hello world!"
}

PLAY RECAP ***********************************************************************
h1                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
h3                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
```
