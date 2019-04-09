This is code for gluing the output of 'motion' into the MIoT framework, allowing you to use cameras as motion-sensors.

"motion" is a software package designed to process streaming video, throwing most of it away, unless motion is detected.
It supports a wide variety of cameras.  When motion is detected in the video stream, it records still frame images as well
as video for as long as there's more motion detected, and for a configurable timeout after motion stops.
I've only been looking at the "motion" package for a few days, but it seems feature-complete and pretty easy to use.

(although I have some questions.)
