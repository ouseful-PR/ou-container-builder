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

    content:          # Content to distribute with the container
    sources:          # Additional sources to fetch packages from
    packages:         # Additional packages to install
    scripts:          # Scripts to run during the install process
    jupyter_notebook: # Configuration options for the Jupyter notebook
    web_apps:         # Configuration options for web applications running in the container
    packs:            # Pre-set configuration packs to include
    tutorial_server:  # Configuration options for the tutorial-server pack
    hacks:            # Pre-set installation hacks

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

Specifies that the container runs one or more web application. How the web applications are run needs to be configured
through the `Web Applications`_ setting.

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
      pip:     # Additional packages to install vai the pip package manager

Apt
+++

The apt configuration setting supports a list of package names that are then installed via ``apt-get install -y``

.. sourcecode:: yaml

    packages:
      apt:
        - pkg-name  # The name of the package to install

Pip
+++

The pip configuration setting supports a list of package names that are then install via ``pip install --no-cache-dir``

.. sourcecode:: yaml

    packages:
      pip:
        - pkg-name  # The name of the package to install (can be any valid pip package name)

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

Jupyter Notebook
----------------

The Jupyter Notebook settings allow you to specify the default URL to load when the notebook is started:

.. sourcecode:: yaml

    jupyter_notebook:
      default_url:     # The default URL to load when the notebook is started

Web Applications
----------------

The OU Container Builder supports building containers that run one or more web applications. These can either be run
next to the Jupyter notebook (setting ``type: jupyter-notebook``) or as one or more stand-alone web applications
(setting ``type: web-app``). In both cases the web applications are configured using the following structure:

.. sourcecode:: yaml

    web_apps:
      - path:     # The URL path that the web application is hosted at.
        cmdline:  # The command line used to start the web application.
        port:     # The port the web application is listening on.
        default:  # Whether this web application should be the default to load.
        timeout:  # How long to wait for the web application to start up.

* ``path``: The URL path that the web application is hosted at. This **cannot** be ``/`` and must also not be a path
  used by anything else such as ``/lab`` or ``/tree``.
* ``cmdline``: The command line to run. Each part of the command is provided as a list under this key. Two substitution
  values are available:

  * ``{port}`` is replaced with the random port the Jupyter proxy has selected for the web application.
  * ``{base_url}`` is replaced with the full path the application is hosted at. This will differ whether the container
    is run directly via Docker or via JupyterHub and this setting handles the distinction.

* ``port`` [optional]: The port the web application listens on. If unspecified, this defaults to 0, which means the
  Jupyter proxy will pick a random port (see above for substitution values for that random port).
* ``default`` [optional]: Whether this web application is the default to run in the container.
* ``timeout`` [optional]: How long to wait for the application to start, before giving up.

For multiple web applications simply repeat the configuration block.

Pre-set Configuration Packs
---------------------------

The OU Container Builder provides pre-configured packs that simplify the setup of common scenarios. Currently the
OU Container Builder only comes with a single pack:

.. sourcecode:: yaml

    packs:
      - tutorial-server  # Enable the Tutorial Server.

Tutorial Server
+++++++++++++++

The Tutorial Server is a simply web-server that provides access to static or dynamic content. The settings here are
used to generate the configuration used by the `Tutorial Server <https://github.com/mmh352/tutorial-server>`_:

.. sourcecode:: yaml

    tutorial_server:
      parts:
        - name:       # The name of this part.
          type:       # The type of part this is.
          path:       # The path on the filesystem where the files are stored.
      default:        # The default part to load.

* ``name``: The name of the part. This is used to generate the URL, thus all values must be valid within a URL.
* ``type``: The following values are supported for the type of part

  * ``tutorial``: Static web content that is served as is.
  * ``workspace``: Direct file access, supports GET and PUT requests to fetch the file content and update the file content.

* ``path``: The path on the filesystem where the files accessed via this part are stored. The path is processed relative to
  the user's home directory.

Pre-set Hacks
-------------

The OU Container Builder uses a minimal Debian-based base image (~100MB), to keep the final image size small. In general
this is not a problem, but some packages make assumptions about how things have been set up in a more common base image.
You should not enable any of these hacks unless you know that your setup fails because they are not enabled:

.. sourcecode:: yaml

    hacks:
      - missing-man1  # The /usr/share/man/man1 file is missing

* ``missing-man1``: Create the directory ``/usr/share/man/man1``. Some packages assume that this directory exists. Setting
  this hack creates the directory during the build process. For packages where this is a known problem, this hack is
  automatically activated.
