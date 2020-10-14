<h1>Qwickly Auto Attendance Script</h1>
<h5>As the semester goes on professors leave the attendance open for people to 
check in as they tune into the class but don't often remind students. This
makes sure you don't forget.</h5>

<h2>Config.json</h2>
<h5>It's required that you fill out a json file for the class you want to check
in automatically for. I did not add support for multiple classes yet but I plan on
on doing so when I make sure that this works first.</h5>

<h6>JSON Format</h6>
<blockquote>
{
<br>
  "username": "", //tuh sign-in goes here
  <br>
  <br>
  "password": "", //password goes here
  <br>
  <br>
  "class": "", //the url to your class goes here(ex. https://templeu.instructure.com/courses/84394)
  <br>
  <br>
  "webdriver": "", //Chrome web driver for the app to pilot a browser https://chromedriver.chromium.org/downloads
  <br>
  <br>
  "userProfile": " " //If you have 2FA you'll need your personal chrome browser's profile path
  <br>
}

</blockquote>

<h2>Usage</h2>
<h4>Make sure to use pyinstaller for your respective OS and to install selenium, it's the only library you'll need to install. Also make sure that the config file is in the same directory as the program.</h4>
<h5>Windows</h5>
After creating an executable with pyinstaller you can use Window's built in task scheduler to run this script when you have
classes
<h5>Linux</h5>
Use the cron command to schedule tasks
<blockquote>a b c d e /directory/command output</blockquote>
<ul>
<li>The first five fields a (min) b (hour) c (day) d (month) e (day of the week) specify the time/date and recurrence of the job.</li>
<li>In the second section, the /directory/command specifies the location and script you want to run.</li>
<li>The final segment output is optional. It defines how the system notifies the user of the job completion.</li>
</ul>

Example of running a script every 10 minutes

<blockquote>*/10 * * * * /usr/bin/python script.py</blockquote>

<h5>MacOS</h5>

MacOS has a scheduler similar to Windows called Automator that pairs up with iCal

<h2>Limitations</h2>
<h5>Check-ins that require pins cannot be automated</h5>
