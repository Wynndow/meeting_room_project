[![Build Status](https://travis-ci.org/Wynndow/meeting_room_project.svg?branch=master)](https://travis-ci.org/Wynndow/meeting_room_project)
[![Coverage Status](https://coveralls.io/repos/github/Wynndow/meeting_room_project/badge.svg?branch=master)](https://coveralls.io/github/Wynndow/meeting_room_project?branch=master)
# Meeting Rooms 20% Project

A web app to allow easy viewing of the free/busy status of the GDS meeting rooms within Aviation House. It uses the Google calendar API to retrieve the status of all meeting rooms on the 3rd, 6th and 7th floors and displays them in an easy to read manor. The status of rooms can be filtered by floor as well as date.

It also sends email reminders once a day to all staff who have any room bookings the following day. The reminders are to prompt people to unbook rooms if they no longer require them.

## Screenshot

<img width="1440" alt="screen shot 2016-11-11 at 13 23 43" src="https://cloud.githubusercontent.com/assets/13836290/20216431/725aba44-a812-11e6-991a-68db9cf8fec7.png">

## Live example

- [meeting-rooms.cloudapps.digital](https://meeting-rooms.cloudapps.digital)

## Technical documentation

This is a Python/Flask application that utilises Google API's to fetch resource and calendar information and present it to a client in an easy to view manor.

The email reminders are currently being sent via AWS SES.

### Running the application

Clone the app and install requirements, then launch the app with `make run_app`

You will need to provide the following env variables:

* `FLASK_CONFIG` - To set the environment for the app. See the config file for options.
* `MR_ADMIN_EMAIL` - The email address of the admin account responsible for sending email reminders.
* `MR_AUTH_TOKEN` - The authorization token used by the POST route that triggers the sending of email reminders.
* `MR_AWS_SMTP_PASSWORD` - The password for the AWS account being used.
* `MR_AWS_SMTP_USERNAME` - The username for the AWS account being used.
* `MR_CLIENT_SECRET_JSON` - The client secret file for the Google Service Account being used.
* `MR_DELEGATED_ACCOUNT` - The delegated account for creating credentials with the correct authorization.
* `MR_EMAIL_PORT` - The port for the email server being used.
* `MR_MAIL_SERVER` - The email server being used.
* `MR_TEST_EMAIL_ADDRESS` = The test email address supplied by AWS.

### Running the test suite

`make test`

## Licence

[MIT License](LICENCE)
