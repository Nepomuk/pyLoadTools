# pyLoad Scripts

This repository contains some scripts I wrote to enhance my pyLoads functionality. They work independently from pyLoad (a download manager) as they are individual scripts which are executed at a certain event.

### pyLoad's script directory
pyLoad loads scripts from directories in

        ~/.pyload/scripts/

In there you'll find the following folders:

        after_reconnect
        all_dls_finished
        all_dls_processed
        before_reconnect
        download_finished
        download_preparing
        package_finished
        unrar_finished

Their functions should be self-explanatory - scripts put in there will be executed at the corresponding event. I use symlinks in there which point to the scripts from this repository, e.g.

        ln -s removeSiteTag.py ~/.pyload/scripts/<event folder>


## Remove Site Tag

**File: `removeSiteTag.py`**

This script removes a site tag from a filename, based on a list of regular expression patterns. It searches in paths given by arguments or from default settings. Run the script with the `-h` option to see some description.

The tags to search for are defined in the header of the script. Make sure to label the group which character should be kept by indicating `(?P<keep>/some_expression/)`.
