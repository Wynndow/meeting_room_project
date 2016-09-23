# Meeting Rooms 20% Project

One paragraph description and purpose.
A web app to allow easy viewing of the free/busy status of the GDS meeting rooms within Aviation House. It uses the Google calendar API to retrieve the status of all meeting rooms on the 3rd, 6th and 7th floors and displays them in an easy to read manor. The status of rooms can be filtered by floor as well as date.

Future iterations will (hopefully) assist in freeing up room space by reminding people who have booked a room to cancel it if they no longer need it.

## Screenshot

<img width="1440" alt="meeting_room_screenshot" src="https://cloud.githubusercontent.com/assets/13836290/18210815/4f720d0a-7132-11e6-9a56-1b531ca5d403.png">

## Live example

- [/meeting-room-project-d.eu-west-1.elasticbeanstalk.com/](http://meeting-room-project-d.eu-west-1.elasticbeanstalk.com/)

## Technical documentation

This is a Python/Flask application that utilises Google API's to fetch resource and calendar information and present it to a client in an easy to view manor.

### Running the application

Clone the app and install requirements, then launch the app with `make run_app`

Documentation for where the app will appear (default port, vhost, URL etc).

### Running the test suite

`make test`

## Licence

[MIT License](LICENCE)
