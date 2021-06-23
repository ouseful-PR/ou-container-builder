Tutorial Server
===============

The `Tutorial Server <https://github.com/mmh352/tutorial-server>`_ is a simple web-server that provides access to
static or dynamic content. To enable the Tutorial Server pack, add it to the top-level ``packs`` key:

.. sourcecode:: yaml

    packs:
      - tutorial-server          # Enable the Tutorial Server

The following settings are used to generate the configuration used by the Tutorial Server:

.. sourcecode:: yaml

    tutorial_server:
      parts:
        - name:       # The name of this part.
          type:       # The type of part this is.
          path:       # The path on the filesystem where the files are stored.
      default:        # The default part to load.
      php-cgi:        # Active the PHP CGI support

* ``parts``: Configures the different parts of the content served by the Tutorial Server. Consists of a list, where
  each entry must have the following three keys:

  * ``name``: The name of the part. This is used to generate the URL, thus all values must be valid within a URL.
  * ``type``: The following values are supported for the type of part

    * ``tutorial``: Static web content that is served as is.
    * ``workspace``: Direct file access, supports GET and PUT requests to fetch the file content and update the file
      content.
    * ``live``: Read-only access to the files. If they are PHP files and ``php-cgi`` is set to ``true``, then they will
      automatically be run via ``php-cgi``

  * ``path``: The path on the filesystem where the files accessed via this part are stored. The path is processed
    relative to the user's home directory.

* ``default``: The ``name`` of the default part to load
* ``php-cgi``: Set to ``true`` in order to enable running PHP scripts via ``php-cgi``
