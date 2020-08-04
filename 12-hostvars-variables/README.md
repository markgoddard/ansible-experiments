# Hostvars variables

Which variables are accessible via the magic `hostvars` variable?

See
[docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)
for types of variables and precedence.

To run:

`ansible-playbook site.yml -e extra_var=ev -i inventory/hosts`

Accessible?

Yes:
* facts
* extra variables
* playbook host/group variables
* inventory host/group variables
* `set_fact` variables

No:
* play variables
* task variables
* role default variables
* role variables
* role parameters
