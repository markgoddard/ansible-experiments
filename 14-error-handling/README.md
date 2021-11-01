# Error handling

How does ansible handle errors?

## When will ansible-playbook exit non-zero?

* If all hosts targeted to the current play are marked as failed or
  unreachable, even if there are other hosts in the inventory.

  ```
  ansible-playbook -i inventory play-stops-if-all-hosts-fail.yml
  echo $?
  ```

* If any hosts are marked as failed or unreachable at the end of a top-level
  playbook (specified as a CLI argument).

  ```
  ansible-playbook -i inventory some-hosts-fail.yml nobody-gets-here.yml
  echo $?
  ```

* If any hosts are marked as failed or unreachable in a play or task marked
  with `any_errors_fatal=true`

  ```
  ansible-playbook -i inventory any-errors-fatal.yml
  echo $?
  ```

* If the number of hosts marked as failed or unreachable in a play exceeds the
  `max_fail_percentage`

  ```
  ansible-playbook -i inventory max-fail-percentage.yml
  echo $?
  ```

## When will ansible-playbook not exit?

* If all hosts targeted to a play are marked as failed or unreachable before
  the play starts

  ```
  ansible-playbook -i inventory play-matches-only-failed-hosts.yml
  echo $?
  ```

* If any hosts are not marked as failed or unreachable at the end of a play
  that is not the last (including statically imported playbooks)

  ```
  ansible-playbook -i inventory mid-playbook-failures-continue.yml
  echo $?
  ```

* If any hosts targeted to a play are marked as failed or unreachable before
  the play starts, and the play is marked with `any_errors_fatal=true`

  ```
  ansible-playbook -i inventory play-matches-only-failed-hosts-with-any-errors-fatal.yml
  echo $?
  ```

* If the number of hosts targeted to a play and marked as failed or unreachable
  before the play starts exceeds the `max_fail_percentage`

  ```
  ansible-playbook -i inventory play-matches-only-failed-hosts-with-max-fail-percentage.yml
  echo $?
  ```
