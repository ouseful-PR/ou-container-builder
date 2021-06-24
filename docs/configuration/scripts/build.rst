Build Scripts
=============

Build scripts are run at container image build time and configured as follows:

.. sourcecode:: yaml

    scripts:
      build:
        - commands:     # Inline definition of the script

* ``inline``: Specifies an inline script. Inline scripts are defined in the ``ContainerConfig.yaml``. They can either
  be specified as a list of commands:

  .. sourcecode:: yaml

      scripts:
        build:
          - commands:
            - touch /etc/notes.txt
            - rm /etc/notes.txt

  or as a block of commands:

  .. sourcecode:: yaml

      scripts:
      build:
        - commands: |
            touch /etc/notes.txt
            rm /etc/notes.txt

  When run at build time the commands are combined using ``&&`` and executed in a single ``RUN`` statement.
