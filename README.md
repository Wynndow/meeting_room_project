[![Build Status](https://travis-ci.org/Wynndow/meeting_room_project.svg?branch=master)](https://travis-ci.org/Wynndow/meeting_room_project)
[![Coverage Status](https://coveralls.io/repos/github/Wynndow/meeting_room_project/badge.svg?branch=master)](https://coveralls.io/github/Wynndow/meeting_room_project?branch=master)
# Meeting Rooms 20% Project

A web app to allow easy viewing of the free/busy status of the GDS meeting rooms within Aviation House. It uses the Google calendar API to retrieve the status of all meeting rooms on the 3rd, 6th and 7th floors and displays them in an easy to read manor. The status of rooms can be filtered by floor as well as date.

It also sends email reminders once a day to all staff who have any room bookings the following day. The reminders are to prompt people to unbook rooms if they no longer require them.

## Screenshot

<img width="1440" alt="screen shot 2016-11-18 at 14 22 51" src="https://cloud.githubusercontent.com/assets/13836290/20433213/9477032a-ad9a-11e6-9694-9739343103a7.png">


## Live example

- [meeting-rooms.cloudapps.digital](https://meeting-rooms.cloudapps.digital)

## Technical documentation

This is a Python/Flask application that utilises Google API's to fetch resource and calendar information and present it to a client in an easy to view manor.

The email reminders are currently being sent via AWS SES.

### Running the application

0. Clone the app
0. `$ cd meeting_room_project`
0. Install requirements with `$ pip install -r requirements.txt`
0. Launch the app with `$ make run_app`

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

## Sending reminder emails

The scheduling of sending reminder emails is handled in a separate app, which can be found here: [https://github.com/Wynndow/meeting_room_project_cron](https://github.com/Wynndow/meeting_room_project_cron).
It sends a POST request to this app at a specified time which triggers the email sending. The POST route is protected with an token to prevent unintended sending.

### Running the test suite

0. Install requirements for testing `$ pip install -r requirements_for_test.txt`
0. Run the tests with `$ make test`

## Licence

[MIT License](LICENCE)
