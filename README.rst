Properconfig
------------

Full-blown configuration. Configure your application, in order of precedence, from:

* command-line
* configuration file passed to the command-line
* environment variables
* local configuration file
* global configuration file

Use a single API similar to the one of ``argparse` instead of a couple of
different ones that have nothing in common (``argparse``, ``configparser``, ``os``).
Returns a dictionary object containing the full configuration.


Usage
=====

.. code-block:: python
    
    from properconfig import create_config_parser
    parser = create_config_parser(
        name="myapp",
        environ=True, # looks up all env vars prefixed with MYAPP_
        global_conf=True, # looks up ??/.myapprc
        local_conf=True # looks up ~/.myapprc
    )
    parser \
        .enable_environ(prefix="MYAPP_")
        .enable_global_conf()
        .enable_local_conf()

    parser.add_argument("-v", "--verbose", type=bool)
    # looks up the following:
    # 1. -v, --verbose
    # 2. section [default] key 'verbose' in local file
    # 3. environment variable MYAPP_VERBOSE

    stuff = parser.add_argument_group("stuff")
    stuff.add_argument("--db_url")
    # looks up the following:
    # 1. --db-url
    # 2. section [stuff] key 'db-url'
    # 3. environment variable MYAPP_STUFF_DB_URL




FIXME
=====

1. Where to find local/global files for Linux and Windows?
2. Add concept of configuration validation
3. Configuration based configuration? argparse verbose coding sucks
4. How to represent wild ArgumentParser.add_argument options with INI files and ENV Vars?
5. Add debug information to the parser to show which option comes from which parser (cli, env var, INI)

Material
========
* http://stackoverflow.com/questions/11077223/what-order-of-reading-configuration-values
* http://blog.vwelch.com/2011/04/combining-configparser-and-argparse.html
* https://pypi.python.org/pypi/ConfArgParse
* https://speakerdeck.com/pyconslides/transforming-code-into-beautiful-idiomatic-python-by-raymond-hettinger-1 slide 20
* https://pypi.python.org/pypi/configparser/3.5.0b2
* http://pythonhosted.org/configglue/
* http://stackoverflow.com/questions/335695/lists-in-configparser
* http://stackoverflow.com/questions/6133517/parse-config-file-environment-and-command-line-arguments-to-get-a-single-coll


Map argument parser to INI and env vars
=======================================

1. When verbose option is present (e.g. -v and --verbose), the verbose is used to define env vars and INI file key
2. Specific argparse actions:

    #. 'count'
        parser.add_argument('-v', action='count')
        # env var and INI must be boolean (=1) or int

    #. 'store_const'
        # env var must exist
        # INI must exist

    #. 'store_true'
        # env var and INI must exist

    #. 'store_false'
        # env var and INI must not exist

    #. 'append'
        # env var and ini ??

3. Specific argparse nargs:

    #. 'nargs'
        # INI::
        
            [hello]
            barlist =
                item1
                item2

        # env var::
        
            KEY=value1:value2:...

Append and nargs
^^^^^^^^^^^^^^^^

* append is ``cmd --option 1 --option 2``
* nargs is ``cmd --option 1 2``
* both produce ``option = [1,2]``
* they can be combined ``cmd --option 1 2 3 --option 3 4`` to give ``option = [[1,2,3], [3,4]]``
* for conf files and env variables, all are implemented using

    # INI::

        [hello]
        barlist =
            item1
            item2

    # env var::

        KEY=value1:value2:...


* if we have both append and nargs, INI files and env vars do not change. ``cmd --option 1 2 3 --option 4 5`` can be

        # INI::

            [hello]
            option =
                1
                2
                3
                4
                5

        # env var::

            KEY=1:2:3:4:5


* since the above is ambiguous, support for both append and nargs is not available for INI and env vars


Implementation
==============

1. Override argument parser piece of code that reads the value, and add fallbacks to environ and INI files
    Flow:
    Try to read value from cli->env->files, then fallback to required checks and setting of defaults
2. Create seperate argument parsers for each input method, parse args in all of them and combine results.
3. Use custom impl. for env vars and INI files. Use set_defaults to stop arg. parser from complaining for missing arguments


TODO
====

1. append action
2. nargs
3. subparsers
