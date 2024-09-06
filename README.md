# UMBC Peoplesoft Autoenroll
Automatically enroll into a class that's full once a spot has been opened up.

This is used for enrolling into a class at UMBC if it is full (or not) and is best used once the waitlist period is over (and class has started for the semester after 5 days.)

Note: The script will check the site every 5 minutes to see if there are any available seats opened. If you would like to change this, edit the `refresh_timer` value in `config.json`. Try not to get rate-limited if you set the timer too low.

How to use:
1. Enter you UMBC credentials into `config.json`
2. Grab the URL to the class that you would like to enroll into by clicking on the "Share" button on the UMBC Peoplesoft website and grabbing the URL to enter it into `config.json`
3. Run `pip install -r requirements.txt` to install Selenium
4. Run the `autoenroll.py` script with `python ./autoenroll.py`
5. Don't forget to accept the Duo Push 2FA authorization notification
6. Sit back and let it run

Last updated: September 5th, 2024
