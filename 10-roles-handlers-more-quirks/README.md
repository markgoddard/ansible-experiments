# Roles - handlers - more quirks

TL;DR using `roles` at the play level and then including role (directly or not)
will make it run its handlers (if triggered) twice instead of once. But
importing this role again in play will reset this behaviour to the expected
one.

Run the demo with:
```
ansible-playbook -i inventory site.yml
```

Running demo, one gets `Some handler` run twice in play A (`roles` and
`include_role`) but once in plays B (`import` resets) and C (no `roles`).

Note **same applies also to indirect include/import** as seen in plays D and E.
This can be confusing.

The quirk is best described by looking at the playbook's contents and the
accompanying comments.

Note this is a different case than experiment 09 which involved role vars.
