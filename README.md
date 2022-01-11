# Teams Bot
A Bot that attends your teams meetings and notifies you when it joins/leaves the meeting.
## Configuration
* Insert your email id ,password in the variables `email_id,password` provided in the beginning of the script
* Insert the subject names(as in the time table) in the `Positions` dictionary.The positions
should be according to the positions the meetings appear in the teams dashboard of your profile.
* To receive realtime notifications,go to Discord>Create Server>Go to Server Settings >Create Webhook>Copy url
and assign it to the variable `webhook` in the script.
## TimeTable
* The timetable provided should be in csv file format.
* The time provided should be in 24 hour format.
* The timetable format should be same as provided.
* Leave cells empty if any.
