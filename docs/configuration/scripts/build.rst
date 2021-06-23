Build Scripts
=============

Build scripts are run at container image build time and configured as follows:

.. sourcecode:: yaml

    scripts:
      build:
        - inline:     # Inline definition of the script
          - command1  # First command to run
          - command2  # Second command to run

* ``inline``: Specifies an inline script. Inline scripts are defined in the ``ContainerConfig.yaml`` as a list of
  commands. When run at build time the commands are combined using ``&&`` and executed in a single ``RUN`` statement.
