Configuration File
==================

The OU Container Builder uses a YAML configuration file to define which components are included in the final Docker
container. By default the Builder expects this file to be called ``ContainerConfig.yaml``, but this can be overridden
on the command-line. The available settings are split into required settings and optional settings.

The required settings are

.. sourcecode:: yaml

    module:  # Module metadata
    type:    # Container type

The optional settings are

.. sourcecode:: yaml

    content:   # Content to distribute with the container
    sources:   # Additional sources to fetch packages from
    packages:  # Additional packages to install
    scripts:   # Scripts to run during the install process
    web_app:   # Configuration options for the nested web application

Module metadata
---------------

The module meta-data is used to create the internal directory structure within which the container files are made
available to the user. This ensures that when the user runs containers for multiple modules, they do not overwrite
each other's files. The module metadata consists of two values:

.. sourcecode:: yaml

    module:
      code:          # The module code
      presentation:  # The module presentation

Container type
--------------

The OU Container Builder will be able to generate multiple types of containers. This configuration setting is used to
determine which of the container types to generate. It supports the types ``jupyter-notebook`` and ``web-app``.

.. sourcecode:: yaml

    type: jupyter-notebook

Specifies that the container runs a Jupyter Notebook.

.. sourcecode:: yaml

    type: web-app

Specifies that the container runs a web application. How the web application is run needs to be configured through
the `Nested Web Application`_ setting.

Content to distribute
---------------------

The OU Container Builder supports distributing module content to the user. When the container is started, then this
content is automatically copied into the module's directory within the user's home directory and thus made available
to them. The configuration uses the following structure:

.. sourcecode:: yaml

    content:
      - source:     # The source directory or file to copy into the container
        target:     # The target directory or file to copy to in the container
        overwrite:  # Whether newer files should overwrite older files

* ``source``: The path to the source directory or file to copy into the container. This is relative to the location of
  the configuration file.
* ``target``: The name of the directory or file in the container. Only a single directory or filename is supported, no
  paths.
* ``overwrite``: As some content should always be kept up-to-date, while other content is there as a starting point and
  can be modified by the user, after which it should not be updated anymore, the distribution functionality has
  multiple overwrite modes:

  * *always*: Content with this setting will always be overwritten with the content distributed with the container.
  * *never*: Content with this setting will never be overwritten with the content distributed with the container.
  * *if-unchanged*: Content with this setting will be overwritten, but only if the user has not modified it.

The user can always delete part or all of the content in their home directory and in that case when the container
starts the next time, the deleted content will automatically be replaced with the latest content.

.. note::

    If you remove content that had previously been distributed to users, this content will **not** be removed
    automatically from the user's home directory.


Sources
-------

The OU Container Builder supports adding additional software sources to the system before installing packages.
Currently it only supports additional sources for the apt package manager.

.. sourcecode:: yaml

    sources:
      apt:    # Additional sources for the apt package manager

Apt
+++

The apt configuration setting supports a list of additional package repositories that can be installed:

.. sourcecode:: yaml

    sources:
      apt:
        - name:  # Name of the repository
          key:   # The URL to fetch the repository's signing key from
          deb:   # The "deb" line to set as the repository's source

* ``name``: The name of the repository. Is used to generate the filenames that the ``key`` and ``deb`` entries are
  stored in.
* ``key``: The URL from which to fetch the repository's signing key. This will be stored in a file called
  ``/etc/apt/trusted.gpg.d/{name}.gpg``.
* ``deb``: The entry of the repository's source file. This specifies where the packages for this additional repository
  are fetched from. This value will be stored in a file called ``/etc/apt/sources.list.d/{name}.list``.

Packages
--------

The OU Container Builder supports specifying additional packages to install. Currently it only supports additional
packages for the apt package manager.

.. sourcecode:: yaml

    packages:
      apt:     # Additional packages to install via the apt package manager

Apt
+++

The apt configuration setting supports a list of package names that are then installed via ``apt-get install -y``

.. sourcecode:: yaml

    packages:
      apt:
        - pkg-name  # The name of the package to install

Scripts
-------

The OU Container Builder supports running arbitrary scripts during the container building process. These are run after
all packages have been installed via the supported package managers.

.. sourcecode:: yaml

    scripts:
      - inline:  # Inline definition of the script

* ``inline``: Specifies an inline script. Multiple inline scripts are possible in a single ``ContainerConfig.yaml``.

Inline Scripts
++++++++++++++

Inline scripts are defined directly within the ``ContainerConfig.yaml`` file:

.. sourcecode:: yaml

    scripts:
      - inline:
        - command

Any number of ``command`` entries are allowed and each one is run as specified here.

Nested Web Application
----------------------

The OU Container Builder supports building containers that run a web application via the ``type: web-app`` setting.
For these the following required, additional settings must be specified:

.. sourcecode:: yaml

    web_app:
      cmdline:  # The commandline used to start the nested web application

* ``cmdline``: The commandline to execute to start the nested web application. By default the wrapper that ensures the
  web application is made compatible with JupyterHub runs the web application on a random port. You can pass this port
  to the web application via the ``{port}`` substitution variable.

The web application also supports the following optional settings:

.. sourcecode:: yaml

    web_app:
      port:     # Fixed port for the nested web application

* ``port``: If the port of the web application cannot be changed, then you can use this to specify that the wrapper
  will always expect the nested web application to be listening on this port.
