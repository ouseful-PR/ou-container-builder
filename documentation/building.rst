Building Containers
===================

To run the OU Container Builder use the following command in the same directory as your ``ContainerConfig.yaml`` file:

.. sourcecode:: console

    $ ou-container-builder

To retain a copy of the build files (``Dockerfile``, other generated files), add the ``--no-clean `` switch.

For a dry run (don't build the image), use ```--no-build`.

To name and tag the generated image, use the ``--tag IMAGENAME`` switch.

To see a full list of supported command-line parameters, use the following command:

.. sourcecode:: console

    $ ou-container-builder --help
