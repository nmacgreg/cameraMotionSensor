This is code for gluing the output of 'motion' into the MIoT framework, allowing you to use cameras as motion-sensors.

"motion" is a software package designed to process streaming video, throwing most of it away, unless motion is detected.
It supports a wide variety of cameras.  When motion is detected in the video stream, it records still frame images as well
as video for as long as there's more motion detected, and for a configurable timeout after motion stops.
I've only been looking at the "motion" package for a few days, but it seems feature-complete and pretty easy to use.

There's a glaring problem with this code.  It's quite inefficient.  All it does is awaken ever 3 seconds, and check
for the existence of a file which is created or deleted by "motion".  And this only works because "motion" has 
configuration allowing it to run commands at the start & end of a motion event, which I used to touch or delete
the file.  This makes it easy to test this code.   However, I'd rather have "motion" run a curl command to PUT 
directly against this Thing's API... but I can't figure out how!  If anybody knows how, I'd appreciate some help.

$ pip install webthing
(or maybe) 
$ pip install webthing --user
(or maybe) 
$ sudo pip install webthing


Maybe look at some examples: 
[nmacgreg@its004nm2 dev]$ git clone git@github.com:mozilla-iot/webthing-python.git


Guide to creating webthings: https://hacks.mozilla.org/2018/05/creating-web-things-with-python-node-js-and-java/
