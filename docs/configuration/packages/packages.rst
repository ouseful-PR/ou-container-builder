Additional Packages
===================

Additional packages can be installed by specifying them under the top-level ``packages`` key. The OU Container Builder
supports installing additional packages via ``apt`` and ``pip``:

.. sourcecode:: yaml

    packages:
      apt:     # Additional packages to install via the apt package manager
      pip:     # Additional packages to install vai the pip package manager

Apt
---

The apt configuration setting supports a list of package names that are then installed via ``apt-get install -y``

.. sourcecode:: yaml

    packages:
      apt:
        - pkg-name  # The name of the package to install

Pip
---

The pip configuration setting supports a list of package names that are then install via ``pip install --no-cache-dir``

.. sourcecode:: yaml

    packages:
      pip:
        - pkg-name  # The name of the package to install (can be any valid pip package requirement)

.. warning::

    The pip installer does not ensure that any system packages required by a pip package are automatically installed.
    These system package dependencies **must** be explicitly listed under the ``apt`` key.
