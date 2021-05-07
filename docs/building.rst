Building Containers
===================

To run the OU Container Builder use the following command in the same directory as your ``ContainerConfig.yaml`` file:

.. sourcecode:: console

    $ ou-container-builder

The ``ou-container-builder`` supports a range of command-line switches to configure the output:

* ``-b``, ``--build``: Automatically build the Docker image [Default behaviour].
* ``-c``, ``--context``: The context directory that contains the ``ContainerConfig.yaml`` [Default: .].
* ``--clean``: Clean all temporary files generated for the Docker build [Default behaviour].
* ``--help``: Show all available command-line switches.
* ``-nb``, ``--no-build``: Generate the Dockerfile, but do not build it. This implies ``--no-clean``.
* ``--no-clean``: Do not clean the temporary files generated for the Docker build.
* ``--tag {TAG}``: Tag the resulting Docker image. The full tag that is passed to Docker is ``mmh352/CODE-PRESENTATION:TAG``,
  where ``CODE`` and ``PRESENTATION`` are taken from the ``ContainerConfig.yaml``.

.. note::

    The Docker image tag currently has a hard-coded account part. This will in future be updated to use the OU Docker repository.
