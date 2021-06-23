Required Configuration Settings
===============================

To create a minimal container via the OU Container Builder only requires specifying the module metadata and container
type.

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

The OU Container Builder is able to generate multiple types of containers. This configuration setting is used to
determine which of the container types to generate. Currently it supports the types ``jupyter-notebook`` and
``web-app``.

.. sourcecode:: yaml

    type: jupyter-notebook

Specifies that the container runs a Jupyter Notebook. :doc:`See here <container_type/jupyter_notebook>` for details
on the configuration settings for this container type.

.. sourcecode:: yaml

    type: web-app

Specifies that the container runs one or more web application. :doc:`See here <container_type/web_app>` for details
on the configuration settings for this container type.
