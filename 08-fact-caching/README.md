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

## Smart mode and the setup module

The `setup` module can be used to explicitly gather facts via a task. We'll use
the `setup.yml` playbook to test how this interacts with `smart` mode:

```
---
# Specify gather_facts=no, then gather via setup module.
- hosts: localhost
  gather_facts: no
  tasks:
    - setup:
```

Try running this with smart mode:

```
export ANSIBLE_GATHERING=smart
time ansible-playbook setup.yml
PLAY [localhost] ******************************************************

TASK [setup] **********************************************************
ok: [localhost]

PLAY RECAP ************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


real    0m2.532s
user    0m1.396s
sys 0m0.244s
```

We can see that the setup task ran. If we run the same commands again, the
runtime does not significantly reduce, and we see that the task executes again.
This suggests that the `setup` module will always run, regardless of the state
of the cache.

## Conditional gathering with the setup module

We may want to skip the setup module if we have facts in the cache. How can we
do this? There is a variable called `module_setup` which gets set to `true`
when facts exist for a host.  See `conditional-setup.yml` for an example of how
to do this.

We might ask whether `module_setup` respects the expiry of the cache. We can
test this using the `conditional-setup.yml` playbook, with a low cache expiry.
Run it once to populate the cache:

```
export ANSIBLE_GATHERING=smart
export ANSIBLE_CACHE_PLUGIN_TIMEOUT=10
time ansible-playbook conditional-setup.yml
PLAY [localhost] ***********************************************************

TASK [setup] ***************************************************************
ok: [localhost]

PLAY RECAP *****************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


real	0m2.569s
user	0m2.091s
sys	0m0.458s
```

Then again, to check that the cache is used:

```
export ANSIBLE_GATHERING=smart
export ANSIBLE_CACHE_PLUGIN_TIMEOUT=10
time ansible-playbook conditional-setup.yml
PLAY [localhost] ***********************************************************

TASK [setup] ***************************************************************
skipping: [localhost]

PLAY RECAP *****************************************************************
localhost                  : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0


real	0m1.332s
user	0m1.223s
sys	0m0.118s
```

Then wait for the cache to expire, and run once more:

```
sleep 10
export ANSIBLE_GATHERING=smart
export ANSIBLE_CACHE_PLUGIN_TIMEOUT=10
time ansible-playbook conditional-setup.yml
PLAY [localhost] ***********************************************************

TASK [setup] ***************************************************************
ok: [localhost]

PLAY RECAP *****************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


real	0m2.491s
user	0m1.974s
sys	0m0.499s
```

We see that the cache is deemed invalid, and facts are gathered again, as we
might expect.

Other conditions we might use with the setup module:

* `gather_subset` tells us which fact subsets exist
* if there is a specific fact we are interested in, we can check if it is
  defined

## Gotchas

* Fact gathering honours the `become` attribute on a play, and this affects
  things like `ansible_user_uid`. The `smart` mode will not collect facts when
  they exist in the cache, even if they were collected with a different value
  of `become`.

## Open Questions

* How does caching interact with `gather_subset`?
