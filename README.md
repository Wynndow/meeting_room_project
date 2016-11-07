# Meeting Rooms 20% Project

A web app to allow easy viewing of the free/busy status of the GDS meeting rooms within Aviation House. It uses the Google calendar API to retrieve the status of all meeting rooms on the 3rd, 6th and 7th floors and displays them in an easy to read manor. The status of rooms can be filtered by floor as well as date.

It also sends email reminders once a day to all staff who have any room bookings the following day. The reminders are to prompt people to unbook rooms if they no longer require them.

## Screenshot

<img width="1440" alt="meeting_room_screenshot" src="https://cloud.githubusercontent.com/assets/13836290/18210815/4f720d0a-7132-11e6-9a56-1b531ca5d403.png">

## Live example

- [meeting-rooms.cloudapps.digital](https://meeting-rooms.cloudapps.digital)

## Technical documentation

This is a Python/Flask application that utilises Google API's to fetch resource and calendar information and present it to a client in an easy to view manor.

The email reminders are currently being sent via AWS SES.

### Running the application

Clone the app and install requirements, then launch the app with `make run_app`

You will need to provide the following env variables:

`FLASK_CONFIG` - To set the environment for the app. See the config file for options.
`MR_ADMIN_EMAIL` - The email address of the admin account responsible for sending email reminders.
`MR_AWS_SMTP_PASSWORD` - The password for the AWS account being used.
`MR_AWS_SMTP_USERNAME` - The username for the AWS account being used.
`MR_CLIENT_SECRET_JSON` - The client secret file for the accessing Google APIs.
`MR_DELEGATED_ACCOUNT` - The delegated account for creating credentials with the correct authorization.
`MR_EMAIL_PORT` - The port for the email server being used.
`MR_MAIL_SERVER` - The email server being used.
`MR_TEST_EMAIL_ADDRESS` = The test email address supplied by AWS.

### Running the test suite

`make test`

## Licence

[MIT License](LICENCE)
