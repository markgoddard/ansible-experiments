# Roles - handlers and vars on include and import

TL;DR including/importing role with handlers along with setting vars will create
separate handler instances if there was any include along the path to role
with handler.

Run the demo with:
```
ansible-playbook -i inventory site.yml
```

Including/importing a role includes/imports it along with its handlers (this is
expected).
As long as one does not use role with vars then all handler instances are
treated as one.

However, when **importing** a role **with vars** from a role that has been
**included**, triggers a quirky Ansible behaviour, where **each instance of
handler acts separately** (**dynamic behaviour is induced**).

Same when simply including a role with vars ('tis expected -
dynamic behaviour).

Moreover, this quirk does **not** happen when roles are imported instead of
included along the path to the role with handler ('tis expected -
static behaviour).

Finally, this does **not** happen when vars are set further away from
the role with handler (e.g. if one moved vars from roles to play in demo;
'tis expected - no vars may apply to handler).

Running demo, one gets `Some handler` run thrice instead of once.

This was the root cause of
[LP#1864810 - kolla-ansible - bug - haproxy restarted multiple times during
deploy](https://bugs.launchpad.net/kolla-ansible/+bug/1864810)
