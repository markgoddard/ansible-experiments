# Error handling

How does ansible handle errors?

## When will ansible-playbook exit non-zero?

* If all hosts targeted to the current play are marked as failed or
  unreachable, even if there are other hosts in the inventory.

  ```
  ansible-playbook -i inventory play-stops-if-all-hosts-fail.yml
  PLAY [Fail all hosts in a play] *************************************************

  TASK [Fail all hosts in a play] *************************************************
  fatal: [h1]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  
  PLAY RECAP **********************************************************************
  h1                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

  echo $?
  2
  ```

* If any hosts are marked as failed or unreachable at the end of a top-level
  playbook (specified as a CLI argument).

  ```
  ansible-playbook -i inventory some-hosts-fail.yml nobody-gets-here.yml
  PLAY [Fail some hosts in a play] ************************************************

  TASK [Fail some hosts in a play] ************************************************
  fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  skipping: [h3]
  skipping: [h1]
  
  PLAY RECAP **********************************************************************
  h1                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h3                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  2
  ```

* If any hosts are marked as failed or unreachable in a play or task marked
  with `any_errors_fatal=true`

  ```
  ansible-playbook -i inventory any-errors-fatal.yml
  PLAY [Fail some hosts in a play (fatal)] ****************************************

  TASK [Fail some hosts in a play (fatal)] ****************************************
  fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  skipping: [h3]
  skipping: [h1]
  
  NO MORE HOSTS LEFT **************************************************************
  
  PLAY RECAP **********************************************************************
  h1                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h3                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  2
  ```

* If the number of hosts marked as failed or unreachable in a play exceeds the
  `max_fail_percentage`

  ```
  ansible-playbook -i inventory max-fail-percentage.yml
  PLAY [Fail some hosts in a play (max_fail_percentage=0)] **********************

  TASK [Fail some hosts in a play (max_fail_percentage=0)] **********************
  fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  skipping: [h3]
  skipping: [h1]
  
  NO MORE HOSTS LEFT ************************************************************
  
  NO MORE HOSTS LEFT ************************************************************
  
  PLAY RECAP ********************************************************************
  h1                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h3                         : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  2
  ```

## When will ansible-playbook not exit?

* If all hosts targeted to a play are marked as failed or unreachable before
  the play starts

  ```
  ansible-playbook -i inventory play-matches-only-failed-hosts.yml
  PLAY [Fail one host] **********************************************************

  TASK [Fail one host] **********************************************************
  skipping: [h3]
  skipping: [h2]
  fatal: [h1]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  
  PLAY [All hosts matching this play have previously failed] ********************
  
  PLAY [This play continues regardless] *****************************************
  
  TASK [Remaining hosts continue] ***********************************************
  ok: [h2] => {
      "msg": "Hello world!"
  }
  ok: [h3] => {
      "msg": "Hello world!"
  }
  
  PLAY RECAP ********************************************************************
  h1                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h2                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h3                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  2
  ```

* If any hosts are not marked as failed or unreachable at the end of a play
  that is not the last (including statically imported playbooks)

  ```
  ansible-playbook -i inventory mid-playbook-failures-continue.yml
  PLAY [Fail one host] **********************************************************

  TASK [Fail one host] **********************************************************
  fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  skipping: [h3]
  skipping: [h1]
  
  PLAY [Remaining hosts continue] ***********************************************
  
  TASK [Remaining hosts continue] ***********************************************
  ok: [h3] => {
      "msg": "Hello world!"
  }
  ok: [h1] => {
      "msg": "Hello world!"
  }
  
  PLAY RECAP ********************************************************************
  h1                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h3                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  ```

* If any hosts targeted to a play are marked as failed or unreachable before
  the play starts, and the play is marked with `any_errors_fatal=true`

  ```
  ansible-playbook -i inventory play-matches-only-failed-hosts-with-any-errors-fatal.yml
  PLAY [Fail one host] **********************************************************

  TASK [Fail one host] **********************************************************
  fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  skipping: [h3]
  skipping: [h1]
  
  PLAY [Play with any_errors_fatal ignores previous failures] *******************
  
  TASK [Remaining hosts continue] ***********************************************
  ok: [h3] => {
      "msg": "Hello world!"
  }
  ok: [h1] => {
      "msg": "Hello world!"
  }
  
  PLAY RECAP ********************************************************************
  h1                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h3                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  2
  ```

* If the number of hosts targeted to a play and marked as failed or unreachable
  before the play starts exceeds the `max_fail_percentage`

  ```
  ansible-playbook -i inventory play-matches-only-failed-hosts-with-max-fail-percentage.yml
  PLAY [Fail one host] **********************************************************

  TASK [Fail one host] **********************************************************
  fatal: [h2]: FAILED! => {"changed": false, "msg": "Failed as requested from task"}
  skipping: [h3]
  skipping: [h1]
  
  PLAY [Play with max_fail_percentage=0 ignores previous failures] **************
  
  TASK [Remaining hosts continue] ***********************************************
  ok: [h3] => {
      "msg": "Hello world!"
  }
  ok: [h1] => {
      "msg": "Hello world!"
  }
  
  PLAY RECAP ********************************************************************
  h1                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
  h2                         : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
  h3                         : ok=1    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

  echo $?
  ```
