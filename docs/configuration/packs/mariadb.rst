MariaDB
=======

To enable the MariaDB pack, add it to the top-level ``packs`` key:

.. sourcecode:: yaml

    packs:
      - mariadb          # Enable a MariaDB database.

This installs a full MariaDB installation, with the database files stored inside the user's home directory in the
mariadb directory. This ensures that the database persists across container launches.

To configure the installation use the top-level ``mariadb`` key:

.. sourcecode:: yaml

    mariadb:
      database:  # Database name
      username:  # Database access username
      password:  # Database access password

* ``database``: The name of the database to create in the MariaDB installation. The database will be created when
  the container starts, if it does not already exist.
* ``username``: The name of the user to use to access the database. The user is created when the container starts and
  has all privileges on the ``database``.
* ``password``: The password used for authenticating

The database is only accessible via socket or the standard MySQL port (3306) on localhost, thus there is no security
risk created by the same password being shared across all containers that use the image.
