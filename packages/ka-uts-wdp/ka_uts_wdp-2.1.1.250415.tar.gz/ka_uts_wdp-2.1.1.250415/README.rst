##########
ka_uts_wdp
##########

Overview
********

.. start short_desc

**Dictionary 'Utilities'**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_wdp`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_wdp

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_wdp

.. end installation

Package files
*************

Classification
==============

The Files of Package ``ka_uts_wdp`` could be classified into the follwing file types:

#. *Special files*
#. *Dunder modules*
#. *Sub Package*
#. *Data files*

Sub-packages
************

The Package ``ka_uts_wdp`` contains the sub-package ``pmeh``:

Sub-package pmeh
================

The Sub-package ``pmeh`` contains following files:

#. special file: py.typed
#. dunder module: __init__.py
#. modules: wdp.py

Module: wdp.py
--------------

The Module ``wdp.py`` contains the followinga classes:

   +-------------+------+---------------------------------------------+
   |Name         |Type  |Description                                  |
   +=============+======+=============================================+
   |CustomHandler|normal|Custom Handler of PatternMatchingEventHandler|
   +-------------+------+---------------------------------------------+
   |WdP          |static|Watch Dog Processor                          |
   +-------------+------+---------------------------------------------+

Class: CustomHandler
^^^^^^^^^^^^^^^^^^^^

The class ``CustomHandler`` contains the subsequent methods.

Methods
"""""""

  .. Methods-of-class-CustomHandlerlabel:
  .. table:: *Methods of class CustomHandler*

   +-----------+--------+-----------------------------------------------------+
   |Name       |Type    |Description                                          |
   +===========+========+=====================================================+
   |__init__   |instance|Initialise class CustomHandler                       |
   +-----------+--------+-----------------------------------------------------+
   |on_created |instance|Process event 'File refered by file path is created' |
   +-----------+--------+-----------------------------------------------------+
   |on_modified|instance|Process 'File refered by file path is modified' event|
   +-----------+--------+-----------------------------------------------------+

Class WdP
^^^^^^^^^

The static class ``WdP`` contains the subsequent methods.

Methods
"""""""

  .. Methods-of-class-WdP-label:
  .. table:: *Methods-of-class-WdP*

   +----+------+-------------------------------------------------+
   |Name|Type  |Description                                      |
   +====+======+=================================================+
   |pmeh|static|WatchDog Task for pattern matching of files paths|
   +----+------+-------------------------------------------------+

Appendix
********

Package Logging
===============

Description
-----------

The Standard or user specifig logging is carried out by the log.py module of the logging
package ka_uts_log using the configuration files **ka_std_log.yml** or **ka_usr_log.yml**
in the configuration directory **cfg** of the logging package **ka_uts_log**.
The Logging configuration of the logging package could be overriden by yaml files with
the same names in the configuration directory **cfg** of the application packages.

Log message types
-----------------

Logging defines log file path names for the following log message types: .

#. *debug*
#. *info*
#. *warning*
#. *error*
#. *critical*

Application parameter for logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Application-parameter-used-in-log-naming-label:
  .. table:: *Application parameter used in log naming*

   +-----------------+---------------------------+----------+------------+
   |Name             |Decription                 |Values    |Example     |
   +=================+===========================+==========+============+
   |dir_dat          |Application data directory |          |/otev/data  |
   +-----------------+---------------------------+----------+------------+
   |tenant           |Application tenant name    |          |UMH         |
   +-----------------+---------------------------+----------+------------+
   |package          |Application package name   |          |otev_xls_srr|
   +-----------------+---------------------------+----------+------------+
   |cmd              |Application command        |          |evupreg     |
   +-----------------+---------------------------+----------+------------+
   |pid              |Process ID                 |          |æevupreg    |
   +-----------------+---------------------------+----------+------------+
   |log_ts_type      |Timestamp type used in     |ts,       |ts          |
   |                 |logging files|ts, dt       |dt        |            |
   +-----------------+---------------------------+----------+------------+
   |log_sw_single_dir|Enable single log directory|True,     |True        |
   |                 |or multiple log directories|False     |            |
   +-----------------+---------------------------+----------+------------+

Log type and Log directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Single or multiple Application log directories can be used for each message type:

  .. Log-types-and-Log-directories-label:
  .. table:: *Log types and directoriesg*

   +--------------+---------------+
   |Log type      |Log directory  |
   +--------+-----+--------+------+
   |long    |short|multiple|single|
   +========+=====+========+======+
   |debug   |dbqs |dbqs    |logs  |
   +--------+-----+--------+------+
   |info    |infs |infs    |logs  |
   +--------+-----+--------+------+
   |warning |wrns |wrns    |logs  |
   +--------+-----+--------+------+
   |error   |errs |errs    |logs  |
   +--------+-----+--------+------+
   |critical|crts |crts    |logs  |
   +--------+-----+--------+------+

Log files naming
^^^^^^^^^^^^^^^^

Conventions
"""""""""""

  .. Naming-conventions-for-logging-file-paths-label:
  .. table:: *Naming conventions for logging file paths*

   +--------+-------------------------------------------------------+-------------------------+
   |Type    |Directory                                              |File                     |
   +========+=======================================================+=========================+
   |debug   |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |info    |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |warning |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |error   |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |critical|/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+

Examples
""""""""

  .. Naming-examples-for-logging-file-paths-label:
  .. table:: *Naming examples for logging file paths*

   +--------+--------------------------------------------+------------------------+
   |Type    |Directory                                   |File                    |
   +========+============================================+========================+
   |debug   |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|debs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |info    |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|infs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |warning |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|wrns_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |error   |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|errs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |critical|/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|crts_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+

Python Terminology
==================

Python package
--------------

Overview
^^^^^^^^

  .. Python package-label:
  .. table:: *Python package*

   +--------------+-----------------------------------------------------------------+
   |Name          |Definition                                                       |
   +==============+==========+======================================================+
   |Python package|Python packages are directories that contains the special module |
   |              |``__init__.py`` and other modules, packages files or directories.|
   +--------------+-----------------------------------------------------------------+
   |Python        |Python sub-packages are python packages which are contained in   |
   |sub-package   |another pyhon package.                                           |
   +--------------+-----------------------------------------------------------------+

Python package sub-directories
------------------------------

Overview
^^^^^^^^

  .. Python package sub-direcories-label:
  .. table:: *Python package sub-directories*

   +--------------+-----------------------------------------+
   |Name          |Definition                               |
   +==============+==========+==============================+
   |Python package|Python packages sub-directories are      |
   |sub-directory |directories contained in python packages.|
   +--------------+-----------------------------------------+
   |Special Python|Special Python package sub-directories   |
   |package       |are python package sub-directories with  |
   |sub-directory |with a special meaning                   |
   +--------------+-----------------------------------------+

Special python package sub-directories
--------------------------------------

Overview
^^^^^^^^

  .. Special-python-package-sub-directories-label:
  .. table:: *Special python sun-directories*

   +----+------------------------------------------+
   |Name|Description                               |
   +====+==========================================+
   |data|Directory for package data files.         |
   +----+------------------------------------------+
   |cfg |Directory for package configuration files.|
   +----+------------------------------------------+

Python package files
--------------------

Overview
^^^^^^^^

  .. Python-package-files-label:
  .. table:: *Python package files*

   +--------------+--------------------------------------------------------------------+
   |Name          |Definition                                                          |
   +==============+==========+=========================================================+
   |Python        |Python packages are files within a python package.                  |
   |package files |                                                                    |
   +--------------+--------------------------------------------------------------------+
   |Special python|Special python package files are package files which are not modules|
   |package files |and used as python marker files like ``__init__.py``                |
   +--------------+--------------------------------------------------------------------+
   |Python package|Python modules are files with suffix ``.py``; they could be empty or|
   |module        |contain python code; other modules can be imported into a module.   |
   +--------------+--------------------------------------------------------------------+
   |Special python|Special python modules like ``__init__.py`` or ``main.py`` are      |
   |package module|python modules with special names and functionality.                |
   +--------------+--------------------------------------------------------------------+

Special python package files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Overview
°°°°°°°°

  .. Special-python-package-files-label:
  .. table:: *Special python package files*

   +--------+--------+---------------------------------------------------------------+
   |Name    |Type    |Description                                                    |
   +========+========+===============================================================+
   |py.typed|Type    |The ``py.typed`` file is a marker file used in Python packages |
   |        |checking|to indicate that the package supports type checking. This is a |
   |        |marker  |part of the PEP 561 standard, which provides a standardized way|
   |        |file    |to package and distribute type information in Python.          |
   +--------+--------+---------------------------------------------------------------+

Special python package modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Overview
°°°°°°°°

  .. Special-Python-package-modules-label:
  .. table:: *Special Python package modules*

   +--------------+-----------+-----------------------------------------------------------------+
   |Name          |Type       |Description                                                      |
   +==============+===========+=================================================================+
   |__init__.py   |Package    |The dunder (double underscore) module ``__init__.py`` is used to |
   |              |directory  |execute initialisation code or mark the directory it contains as |
   |              |marker     |a package. The Module enforces explicit imports and thus clear   |
   |              |file       |namespace use and call them with the dot notation.               |
   +--------------+-----------+-----------------------------------------------------------------+
   |__main__.py   |entry point|The dunder module ``__main__.py`` serves as an entry point for   |
   |              |for the    |the package. The module is executed when the package is called by|
   |              |package    |the interpreter with the command **python -m <package name>**.   |
   +--------------+-----------+-----------------------------------------------------------------+
   |__version__.py|Version    |The dunder module ``__version__.py`` consist of assignment       |
   |              |file       |statements used in Versioning.                                   |
   +--------------+-----------+-----------------------------------------------------------------+

Python elements
---------------

Overview
°°°°°°°°

  .. Python elements-label:
  .. table:: *Python elements*

   +-------------+--------------------------------------------------------------+
   |Python method|Python methods are python functions defined in python modules.|
   +-------------+--------------------------------------------------------------+
   |Special      |Special python methods are python functions with special names|
   |python method|and functionalities.                                          |
   +-------------+--------------------------------------------------------------+
   |Python class |Python classes are defined in python modules.                 |
   +-------------+--------------------------------------------------------------+
   |Python class |Python class methods are python methods defined python        |
   |method       |classes.                                                      |
   +-------------+--------------------------------------------------------------+

Special python methods
^^^^^^^^^^^^^^^^^^^^^^

Overview
°°°°°°°°

  .. Special-python-methods-label:
  .. table:: *Special python methods*

   +--------+------------+----------------------------------------------------------+
   |Name    |Type        |Description                                               |
   +========+============+==========================================================+
   |__init__|class object|The special method ``__init__`` is called when an instance|
   |        |constructor |(object) of a class is created; instance attributes can be|
   |        |method      |defined and initalized in the method.                     |
   +--------+------------+----------------------------------------------------------+

Table of Contents
=================

.. contents:: **Table of Content**
