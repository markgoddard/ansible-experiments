# Fact caching

Q: How can I use fact caching to improve performance of Ansible?

Fact caching is described
[here](http://docs.ansible.com/ansible/playbooks_variables.html#fact-caching).

In this example we have the following in `ansible.cfg`:

```
[defaults]
fact_caching = jsonfile
fact_caching_connection = ./facts
fact_caching_timeout = 120
```

The `site.yml` playbook simply has two simple plays which display the
`ansible_hostname` fact:

```
---
# Don't specify gather_facts.
- hosts: localhost
  tasks:
    - debug:
        var: ansible_hostname

# Do specify gather_facts.
- hosts: localhost
  gather_facts: yes
  tasks:
    - debug:
        var: ansible_hostname
```

## Implicit mode

First, we will test the default gathering mode, `implicit`.

```
time ansible-playbook site.yml 

 PLAY [localhost] ****************************************************

 TASK [Gathering Facts] **********************************************
 ok: [localhost]

 PLAY [localhost] ****************************************************

 TASK [Gathering Facts] **********************************************
 ok: [localhost]

 PLAY RECAP **********************************************************
 localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


 real   0m3.093s
 user   0m2.204s
 sys    0m0.468s
 ```

We can see that each play gathers facts. A JSON file is created containing the
facts - `facts/localhost` - but it is only being written to, not read.


## Explicit mode

Next, we will try the `explicit` mode.

```
rm -f facts/localhost # clear cache
export ANSIBLE_GATHERING=explicit
time ansible-playbook site.yml
PLAY [localhost] *****************************************************

TASK [debug] *********************************************************
ok: [localhost] => {
        "ansible_hostname": "VARIABLE IS NOT DEFINED!"
}

PLAY [localhost] *****************************************************

TASK [Gathering Facts] ***********************************************
ok: [localhost]

TASK [debug] *********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY RECAP ***********************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

real    0m2.481s
user    0m1.900s
sys 0m0.328s
```

Here we see that without setting `gather_facts` to `true`, facts are not
gathered in the first play.

If we run the play a second time, the first play is able to use the fact cache,
but the second play still gathers facts as this was explicitly requested in the
play. Runtime is similar.

```
export ANSIBLE_GATHERING=explicit
time ansible-playbook site.yml
PLAY [localhost] ******************************************************

TASK [debug] **********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY [localhost] ******************************************************

TASK [Gathering Facts] ************************************************
ok: [localhost]

TASK [debug] **********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY RECAP ************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


real    0m2.239s
user    0m1.816s
sys 0m0.260s
```

## Smart

Finally, we will try `smart` mode.

```
rm -f facts/localhost # clear cache
export ANSIBLE_GATHERING=smart
time ansible-playbook site.yml
PLAY [localhost] ******************************************************

TASK [Gathering Facts] ************************************************
ok: [localhost]

TASK [debug] **********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY [localhost] ******************************************************

TASK [debug] **********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY RECAP ************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


real    0m1.786s
user    0m1.196s
sys 0m0.404s
```

Here we see that facts are gathered in the first play, similarly to implicit
mode. In the second play, even with an explicit `gather_facts` on the play,
facts are not gathered and the cache is used. Runtime is reliably lower than in
earlier runs, even compared with the explicit mode which also only gathered
facts once.

Let's try again with a populated cache:

```
export ANSIBLE_GATHERING=smart
time ansible-playbook site.yml
PLAY [localhost] ******************************************************

TASK [debug] **********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY [localhost] ******************************************************

TASK [debug] **********************************************************
ok: [localhost] => {
        "ansible_hostname": "mark-xps15"
}

PLAY RECAP ************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


real    0m0.631s
user    0m0.528s
sys 0m0.100s
```

Wow, quite an improvement. We can see that facts were not gathered, and the
cache was used for each play.
