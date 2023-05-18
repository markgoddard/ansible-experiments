# Handler include loops

Trying to reproduce an Ansible bug seen in ansible-core 2.14.

## 1

Does the "conditional handler include loop" pattern for serialising multiple tasks still work?

```
ansible-playbook -i inventory handler-include-loop.yml
```

Works as expected - handlers execute serially for each host.

## 2

Michal's theory:

1. Notify two handlers "bootstrap" and "restart"
2. order of handlers is that we do 3 handlers of "bootstrap", then two handlers of "restart",  and then last handler of "bootstrap"
3. Somehow the last handler of "bootstrap" takes play_hosts of "restart" handler :wink:

```
ansible-playbook -i inventory multiple-handlers.yml
```

Works as expected - final handler executes only on first host.
