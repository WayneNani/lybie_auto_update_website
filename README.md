## Lybie's Auto-Update Script

This is a little update utility for [places-of-unity.com](places-of-unity.com) in order to make it
less complex to maintain essential parts of the website (such as Current Location and the Places
that have been added).

The infrastructure behind this is as follows:<br>
An Oracle Database instance with an Oracle APEX Application on top (I just love this tool so I had to 
use it :P) can be accessed to change any data provided by the website (again this can be the location,...).
If someone updated data this person would run the python script provided in this repo to update the 
[GIT-Repository of the Website itself](https://github.com/WayneNani/lybie-places-of-unity) and publish
the freshly created Website to the Server that hosts it.

Done!

...At least that is how it **should** work.