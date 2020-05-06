# Concurrent known hosts update

Q: Does the `known_hosts` module fail to atomically update the known hosts file
when iterating on many nodes?

A: Yes.

```
$ ansible-playbook site.yml
[...]

TASK [fail] ********************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "msg": "Found 93 keys, expected 96"}
```

Q: Does it work when `known_hosts` is called with `serial: 1`?

A: Yes.

```
$ ansible-playbook site.yml -e ansible_serial=1
[...]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "msg": "Found the expected number of keys"
}
```
