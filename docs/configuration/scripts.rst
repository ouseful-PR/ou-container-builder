Scripts
=======

The OU Container Builder supports running arbitrary scripts during build time and at container startup and shutdown.
These are configured under the top-level ``scripts`` key:

.. sourcecode:: yaml

    scripts:
      build:     # Scripts run during the build process
      startup:   # Scripts run at container startup
      shutdown:  # Scripts run at container shutdown

Build scripts are run from the Dockerfile using ``RUN`` commands. Startup and shutdown scripts are run when the
container is started and stopped.

Each script is configured using the following settings:

.. sourcecode:: yaml

    - commands:  # Commands to run in this script

* ``commands``: The commands to run for this script. This can either be provided using a list of commands:

  .. sourcecode:: yaml

      - commands:
        - touch /etc/notes.txt
        - rm /etc/notes.txt

  or as a block of commands:

  .. sourcecode:: yaml

      - commands: |
          touch /etc/notes.txt
          rm /etc/notes.txt


.. note:

    Startup scripts are run **before** any :doc:`services <services>` are started.

    Shutdown scripts are run **after** any :doc:`services <services>` are stopped.
