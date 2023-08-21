# No hosts remaining callback

When do we receive the `v2_playbook_on_no_hosts_remaining` callback?

This example includes a callback plugin that prints "NO HOSTS REMAINING!" to
the stdout when the callback is received.

The test inventory includes 3 hosts, and the test.yml playbook includes one
that that fails the first host, and second debug task.

```
ansible-playbook -i inventory test.yml
```

Testing with ansible-core 2.15.3, the callback is not received.

Now, try the same playbook with `any_errors_fatal: true`:

```
ansible-playbook -i inventory test_any_errors_fatal.yml
```

This time the callback fires.

And again with `max_fail_percentage: 0`:

```
ansible-playbook -i inventory test_max_fail_percentage_0.yml
```

Again, the callback fires, but this time it fires twice!

And finally with `max_fail_percentage: 100`:

```
ansible-playbook -i inventory test_max_fail_percentage_100.yml
```

This time the callback does not fire.
