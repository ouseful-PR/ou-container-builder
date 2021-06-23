Scripts
=======

The OU Container Builder supports running arbitrary scripts during build time and at container startup. These are
configured under the top-level ``scripts`` key:

.. sourcecode:: yaml

    scripts:
      build:    # Scripts run during the build process
      startup:  # Scripts run at container startup

.. toctree::
    :maxdepth: 2
    :titlesonly:

    build
    startup
