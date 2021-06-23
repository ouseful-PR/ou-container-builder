Startup Scripts
===============

Startup scripts are run each time the container is started up, after distributing any content, but before any
:doc:`system services <../services>` are started. Startup scripts are configured as follows:

.. sourcecode:: yaml

    scripts:
      startup:
        - cmd:  # The command to run

* ``cmd``: The command to run. The file to execute must have been placed in the system using the
  :doc:`content settings <../content>` and made executable using a :doc:`build script <build>`.
