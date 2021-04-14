Configuration File
==================

The OU Container Builder uses a YAML configuration file to define which components are included in the final Docker
container. By default the Builder expects this file to be called ``config.yaml``, but this can be overridden on the
command-line. The available settings are split into required settings and optional settings.

The required settings are

.. sourcecode:: yaml

    module:  # Module metadata
    type:    # Container type

The optional settings are

.. sourcecode:: yaml

    content:  # Content to distribute with the container

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
determine which of the container types to generate. Currently only a single type ``jupyter-notebook`` is supported.
However, to ensure that the build process will work without changes when further types are added, the type has to be
specified now.

.. sourcecode:: yaml

    type: jupyter-notebook

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
