# Drexel Course Availability Checker

We all dread registration day at Drexel. Almost always our chosen schedule gets ruined because some class gets filled up and its difficult to find a replacement class. Everything is too stressful.

But to relieve some of your stress, this program will let you escape the whole process of refreshing Drexel Term Master Schedule every hour to find an available seat for the class you want. As soon as an open seat shows up for your class, the program will send you an email so you can quickly go ahead and register before someone else takes your place!

## Installation

Go to [this](https://myaccount.google.com/lesssecureapps) link and enable access for less secure apps. If you don't feel comfortable enabling this, I suggest you make a new Google account for this program.

Next, open up CONFIG_DEV.txt and fill in the appropiate fields.
* Sender Email should be the Google account you used to enable access for less secure apps.
* Sender Password is self explanitory.
* Recepient Email can be any email you want. This email will receive the updates.
* Send update email can be set to however many hours after which you'd like to receive updates about your course. Can be set to zero to receive no updates. Note that you will get an email update as soon as a seat opens up regardless of what configuration you set.
* Check for course availability field checks the Drexel Term Master every x amount of seconds to see if a spot opened up. 

Now rename the CONFIG_DEV.txt file to CONFIG.txt.

Next, install the dependencies using the following commands:
```
pip install requests
pip install bs4
pip install ssl

```
## Usage

In the working directory, open up a terminal and type:
```
python main.py
```
And follow the prompts.

## To-do

* Find a way to log-in to one.drexel.edu and check the class status in real time instead of relying on the Term Master website which gets updated every few hours.
* Add error messages for incorrect email/password.
* Avoid enabling access for "less secure apps" somehow. 

## Contributing

1. Fork it! Click the Fork button on the top right corner.
1. Clone it to your local computer using `git clone <copied-url>`
1. Create your feature branch: `git checkout -b my-new-feature`
1. Commit your changes: `git commit -am 'Add some feature'`
1. Push to the branch: `git push origin my-new-feature`
1. Submit a pull request :D

Feel free to add more issues if you want a feature added!
