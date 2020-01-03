# Async tasks

How do async tasks work in Ansible?

With poll > 0, tasks are polled, so we can avoid connection timeouts. We are
still subject to the number of forks, so tasks will be executed in batches.
```
With poll == 0, tasks are kicked off concurrently for all hosts. The result can
be collected in a separate task via async_status.

See `site.yml` for an example:


ansible-playbook site.yml -i inventory
```

Add some `-v`s to see what's going on.

https://docs.ansible.com/ansible/latest/user_guide/playbooks_async.html
