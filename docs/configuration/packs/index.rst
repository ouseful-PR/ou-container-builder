Configuration Packs
===================

The OU Container Builder provides pre-configured packs that simplify the setup of common scenarios. Packs are always
configured via the top-level ``packs`` key:

.. sourcecode:: yaml

    packs:
      - tutorial-server  # Enable the Tutorial Server.
      - mariadb          # Enable a MariaDB database.

Currently the following two packs are provided:

.. toctree::
    :maxdepth: 2
    :titlesonly:

    mariadb
    tutorial_server
