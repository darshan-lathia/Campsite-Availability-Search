camping.py is original ( I had tomake a small change for my version of python)

camping_wrapper.py is a wrapper I wrong to print results as I want  

camping_notification is a wrapper over camping_wrapper.py to run it continuously with chosen frequency. It will say no changes detected of new line is not added or removed in results. If it sees a change it will print the change and regular result. It also has filter what results we want. Pri/reg/ignore or all. 


CAMPING_WRAPPER.PY OUTPUT 

(camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_wrapper.py --start-date 2025-01-21 --end-date 2025-02-05 --parks 234015 --show-campsite-info --nights 1
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
  2025-01-31 (Fri) -> 2025-02-01 (Sat) --> 73 site(s) available
  2025-02-01 (Sat) -> 2025-02-02 (Sun) --> 73 site(s) available
  2025-01-24 (Fri) -> 2025-01-25 (Sat) --> 35 site(s) available
  2025-01-25 (Sat) -> 2025-01-26 (Sun) --> 35 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
  2025-01-23 (Thu) -> 2025-01-24 (Fri) --> 94 site(s) available
  2025-01-26 (Sun) -> 2025-01-27 (Mon) --> 102 site(s) available
  2025-01-30 (Thu) -> 2025-01-31 (Fri) --> 107 site(s) available
  2025-02-02 (Sun) -> 2025-02-03 (Mon) --> 116 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*
  2025-01-21 (Tue) -> 2025-01-22 (Wed) --> 98 site(s) available
  2025-01-22 (Wed) -> 2025-01-23 (Thu) --> 105 site(s) available
  2025-01-27 (Mon) -> 2025-01-28 (Tue) --> 119 site(s) available
  2025-01-28 (Tue) -> 2025-01-29 (Wed) --> 118 site(s) available
  2025-01-29 (Wed) -> 2025-01-30 (Thu) --> 121 site(s) available
  2025-02-03 (Mon) -> 2025-02-04 (Tue) --> 117 site(s) available
  2025-02-04 (Tue) -> 2025-02-05 (Wed) --> 120 site(s) available
(camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_wrapper.py --start-date 2025-01-21 --end-date 2025-02-05 --parks 234015 --show-campsite-info --nights 2
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
  2025-01-31 (Fri) -> 2025-02-02 (Sun) --> 73 site(s) available
  2025-01-24 (Fri) -> 2025-01-26 (Sun) --> 35 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
  2025-01-30 (Thu) -> 2025-02-01 (Sat) --> 69 site(s) available
  2025-02-01 (Sat) -> 2025-02-03 (Mon) --> 71 site(s) available
  2025-01-23 (Thu) -> 2025-01-25 (Sat) --> 34 site(s) available
  2025-01-25 (Sat) -> 2025-01-27 (Mon) --> 32 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*
  2025-01-21 (Tue) -> 2025-01-23 (Thu) --> 94 site(s) available
  2025-01-22 (Wed) -> 2025-01-24 (Fri) --> 90 site(s) available
  2025-01-26 (Sun) -> 2025-01-28 (Tue) --> 101 site(s) available
  2025-01-27 (Mon) -> 2025-01-29 (Wed) --> 115 site(s) available
  2025-01-28 (Tue) -> 2025-01-30 (Thu) --> 116 site(s) available
  2025-01-29 (Wed) -> 2025-01-31 (Fri) --> 105 site(s) available
  2025-02-02 (Sun) -> 2025-02-04 (Tue) --> 109 site(s) available
  2025-02-03 (Mon) -> 2025-02-05 (Wed) --> 114 site(s) available
(camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_wrapper.py --start-date 2025-01-21 --end-date 2025-02-05 --parks 234015 --show-campsite-info --nights 3
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
  2025-01-30 (Thu) -> 2025-02-02 (Sun) --> 69 site(s) available
  2025-01-31 (Fri) -> 2025-02-03 (Mon) --> 71 site(s) available
  2025-01-23 (Thu) -> 2025-01-26 (Sun) --> 34 site(s) available
  2025-01-24 (Fri) -> 2025-01-27 (Mon) --> 32 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*
  2025-01-21 (Tue) -> 2025-01-24 (Fri) --> 80 site(s) available
  2025-01-26 (Sun) -> 2025-01-29 (Wed) --> 100 site(s) available
  2025-01-27 (Mon) -> 2025-01-30 (Thu) --> 114 site(s) available
  2025-01-28 (Tue) -> 2025-01-31 (Fri) --> 100 site(s) available
  2025-01-29 (Wed) -> 2025-02-01 (Sat) --> 69 site(s) available
  2025-02-01 (Sat) -> 2025-02-04 (Tue) --> 69 site(s) available
  2025-02-02 (Sun) -> 2025-02-05 (Wed) --> 107 site(s) available
  2025-01-22 (Wed) -> 2025-01-25 (Sat) --> 33 site(s) available
  2025-01-25 (Sat) -> 2025-01-28 (Tue) --> 32 site(s) available
(camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_wrapper.py --start-date 2025-01-21 --end-date 2025-02-05 --parks 234015 --show-campsite-info --nights 4
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
  2025-01-30 (Thu) -> 2025-02-03 (Mon) --> 67 site(s) available
  2025-01-23 (Thu) -> 2025-01-27 (Mon) --> 31 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*
  2025-01-26 (Sun) -> 2025-01-30 (Thu) --> 99 site(s) available
  2025-01-27 (Mon) -> 2025-01-31 (Fri) --> 99 site(s) available
  2025-01-28 (Tue) -> 2025-02-01 (Sat) --> 67 site(s) available
  2025-01-29 (Wed) -> 2025-02-02 (Sun) --> 69 site(s) available
  2025-01-31 (Fri) -> 2025-02-04 (Tue) --> 69 site(s) available
  2025-02-01 (Sat) -> 2025-02-05 (Wed) --> 68 site(s) available
  2025-01-21 (Tue) -> 2025-01-25 (Sat) --> 31 site(s) available
  2025-01-22 (Wed) -> 2025-01-26 (Sun) --> 33 site(s) available
  2025-01-24 (Fri) -> 2025-01-28 (Tue) --> 32 site(s) available
  2025-01-25 (Sat) -> 2025-01-29 (Wed) --> 32 site(s) available
(camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_wrapper.py --start-date 2025-01-21 --end-date 2025-02-05 --parks 234015 --show-campsite-info --nights 5
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
  2025-01-26 (Sun) -> 2025-01-31 (Fri) --> 90 site(s) available
  2025-01-27 (Mon) -> 2025-02-01 (Sat) --> 66 site(s) available
  2025-01-28 (Tue) -> 2025-02-02 (Sun) --> 67 site(s) available
  2025-01-29 (Wed) -> 2025-02-03 (Mon) --> 67 site(s) available
  2025-01-30 (Thu) -> 2025-02-04 (Tue) --> 65 site(s) available
  2025-01-31 (Fri) -> 2025-02-05 (Wed) --> 68 site(s) available
  2025-01-21 (Tue) -> 2025-01-26 (Sun) --> 31 site(s) available
  2025-01-22 (Wed) -> 2025-01-27 (Mon) --> 31 site(s) available
  2025-01-23 (Thu) -> 2025-01-28 (Tue) --> 31 site(s) available
  2025-01-24 (Fri) -> 2025-01-29 (Wed) --> 32 site(s) available
  2025-01-25 (Sat) -> 2025-01-30 (Thu) --> 31 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*


CAMPING_NOTIFICATION.PY OUTPUTS


[4:03 PM, 1/16/2025] Darshan Lathia: (camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_notification.py --start-date 2025-01-16 --end-date 2025-01-20 --parks 234015 --nights 1 --frequency 1
Starting camping notifications with frequency: 1 minute(s)

[2025-01-16 18:56:56.317418] Checking campsite availability...

=== Changes Detected ===
🟢 New availability:   2025-01-16 (Thu) -> 2025-01-17 (Fri) --> 99 site(s) available

=== Full Results for Reference ===
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
  2025-01-16 (Thu) -> 2025-01-17 (Fri) --> 99 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*


[2025-01-16 18:57:57.609574] Checking campsite availability...

No changes detected.
[4:03 PM, 1/16/2025] Darshan Lathia: (camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_notification.py --start-date 2025-01-16 --end-date 2025-01-20 --parks 234015 --nights 1 --frequency 1 --filters {priority,regular}
Starting camping notifications with frequency: 1 minute(s)
Filtering results: priority, regular

[2025-01-16 19:02:19.778984] Checking campsite availability...

=== Changes Detected ===
🟢 New availability:   2025-01-16 (Thu) -> 2025-01-17 (Fri) --> 99 site(s) available

=== Full Results for Reference ===
🏕 🏕 PINNACLES CAMPGROUND
  *Priority Results:*
🏕 🏕 PINNACLES CAMPGROUND
  *Regular Results:*
  2025-01-16 (Thu) -> 2025-01-17 (Fri) --> 99 site(s) available
🏕 🏕 PINNACLES CAMPGROUND
  *Ignored Results:*



[2025-01-16 19:03:20.692419] Checking campsite availability...

No changes detected.
[4:03 PM, 1/16/2025] Darshan Lathia: (camping_reservation) ~/Documents/recreation-gov-campsite-checker$ python camping_notification.py --start-date 2025-01-16 --end-date 2025-01-20 --parks 234015 --nights 1 --frequency 1 --filters priority
Starting camping notifications with frequency: 1 minute(s)
Filtering results: priority

[2025-01-16 19:01:43.591783] Checking campsite availability...

No changes detected.















darshan@Darshans-MacBook-Air Camping_Reservation_python_script % pyenv virtualenv 3.12.2 camping_reservation_env
darshan@Darshans-MacBook-Air Camping_Reservation_python_script % pyenv activate camping_reservation_env
(camping_reservation_env) darshan@Darshans-MacBook-Air Camping_Reservation_python_script % ls
LICENSE.md                      camping.py                      camping_wrapper.py              fake_twitter_credentials.json   requirements.txt                utils
README.md                       camping_notification.py         clients                         notifier.py                     setup.py
README_own_words.md             camping_reservation             enums                           other                           tests
(camping_reservation_env) darshan@Darshans-MacBook-Air Camping_Reservation_python_script % pwd
/Users/darshan/Projects/Camping_Reservation/Camping_Reservation_python_script



To deactivate the environment:

pyenv deactivate
To delete an environment:

pyenv uninstall camping_reservation_env




To automatically activate a virtual environment when you cd into a project:

Inside your project folder (~/Projects/Personal/my-python-project), run:
pyenv local camping_reservation_env
Now, every time you enter this folder, pyenv will activate my-python-env automatically.









