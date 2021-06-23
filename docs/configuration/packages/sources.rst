Additional APT Sources
======================

To add additional APT sources use the top-level ``sources`` key:

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

Multiple sources can be added by repeating creating more list items with the same three keys.

.. note::

    The sources are, obviously, added before the package installation, thus all packages provided by the new sources
    are available when installing :doc:`additional packages <packages>`.
