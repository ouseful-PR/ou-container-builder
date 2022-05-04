OpenRefine
==========

To enable the OpenRefine pack, add it to the top-level ``packs`` key:

.. sourcecode:: yaml

    packs:
      - openrefine          # Install OpenRefine server .

This installs the OpenRefine application and the Java runtime environment required to run it.
The OpenRefine application is installed into the directory ``/var/openrefine/``.
An ``openrefine`` directory is also created in the ``$HOME`` directory to store project files.

To configure the installation use the top-level ``openrefine`` key:

.. sourcecode:: yaml

    openrefine:
      version:  # Version of OpenRefine, as a string; current stable release is: '3.4.1'

* ``version``: The version of OpenRefine o use. The current stable version is ``3.4.1``.

The OpenRefine server can be accessed using the Jupyter Server Proxy in a Jupyter server container.

To configure the Jupyter server container to use a proxied Open Refine server, in the container config file
ensure that the ``jupyter-server-proxy`` package is installed and define an OpenRefine web application:

.. sourcecode::

    packages:
      pip:
        - jupyter-server-proxy

    web_apps:
      - path:          openrefine
        cmdline:       /var/openrefine/refine -i 0.0.0.0 -p {port} -d $HOME/openrefine
