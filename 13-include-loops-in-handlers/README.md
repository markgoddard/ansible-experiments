# Looped task includes in handlers

In a regular task, we can use a conditional looped include to perform a set of
tasks serially for each host:

```
- name: include when loop item is inventory_hostname
  include_tasks: include.yml
  when: inventory_hostname == item
  loop: "{{ groups['x'] }}"
```

See `include-loop.yml` for a complete example. The included task in this case
displays the name of the host. If we run this multiple times we see that the
order of the includes is consistent between runs:

```
ansible-playbook -i inv include-loop.yml
```

Next, we can try this pattern from within a handler, as in
`handler-include-loop.yml`. Again, the order seems consistent.

```
ansible-playbook -i inv handler-include-loop.yml
```

In `handler-include-loop2.yml`, we use a `command` task to notify the handler,
   rather than the `debug` task used previously. In this case, the order
   becomes inconsistent. It seems that the task completion becoming
   asynchronous causes the order of the handler host list to become ordered
   differently from the main host list.

```
ansible-playbook -i inv handler-include-loop2.yml
```
