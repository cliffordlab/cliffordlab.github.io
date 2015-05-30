Sepsis Regression Calculator
================

This page is a logistic regression calculator to determine risk of sepsis in the pre-hospital setting.

By Carmen Polito, Erik Reinertsen, and Gari Clifford<br>

Version 0.1 last updated 10/27/2014<br>

===

Source from: http://statpages.org/logistic.html

Fields:

+ Name
+ Patient ID
+ Time + Date
+ Caregiver / ED / ambulance ID (optional)
+ Age: Dropdown box with 4 possibilities (default is nothing): unknown, <40, 40-59, or >59; force user to pick one of the ages - or if age is unknown prompt to ask, if
no comprehensible answer then guess and add a 'guess' check box.

+ Nursing home (yes or no)
+ EMD complaint category == 'sick person' (yes or no)
+ Tactile temp (hot or not hot)
+ SBP in mmHg: ask for retake if <40; if >=110, pop up
message saying 'are you sure - this is only for patients SBP < 110 mmHg'

+ O2 sat (check to make sure it is between 60 and
100 - if they select >100 throw error, if < 60 ask them to retake it)

===

To do list:

+ Hack web page to produce severity index from sepsis input parameters
+ Push probability back to web page for user to see
+ Add decision support (i.e. give instructions to escalate)
+ Pull system time
+ Save ALL info to file (in folder synced through box).
http://stackoverflow.com/questions/5349921/local-javascript-write-to-local-file
