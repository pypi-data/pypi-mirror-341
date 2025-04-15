##########
ka_uts_com
##########

Overview
********

.. start short_desc

**Communication Utilities**

.. end short_desc

Installation
************

.. start installation

The package ``ka_uts_com`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_com

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_com

.. end installation

Package files
*************

Classification
==============

The Files of Package ``ka_uts_com`` could be classified into the follwing file types:

#. *Special files*
#. *Dunder modules*
#. *Decorator modules*
#. *Package modules*
#. *Data files*

Decorator Modules
*****************

Overview
========

  .. Decorator Modules-label:
  .. table:: *Decorator Modules*

   +------+-----------------+
   |Name  |Decription       |
   +======+=================+
   |dec.py|Decorators module|
   +------+-----------------+

Data Files
**********

Overview
========

  .. Data-Files-label:
  .. table:: *Data Files*

   +-----------+--------------------------------------------+
   |Name       |Description                                 |
   +===========+============================================+
   |log.std.yml|Yaml configuration file for standard logging|
   +-----------+--------------------------------------------+
   |log.usr.yml|Yaml configuration file for user logging    |
   +-----------+--------------------------------------------+

Package Files
*************

Classification
==============

The Modules of Package ``ka_uts_com`` could be classified into the following module types:

#. **Communication Modules**
#. **Base Modules**

Communication Modules
=====================

Overview
--------

  .. Communication Modules-label:
  .. table:: *Communication Modules*

   +--------+-----------------------------+
   |Name    |Decription                   |
   +========+=============================+
   |com.py  |Communication handling module|
   +--------+-----------------------------+
   |timer.py|Timer management module      |
   +--------+-----------------------------+

Communication module com.py
===========================

The Communication Module ``com.py`` contains the single static class ``Com``.

Class Com
---------

The static Class ``Com`` contains the subsequent variables and methods.

Variables
^^^^^^^^^

  .. Variables-of-class-Com-label:
  .. table:: *Variables of class Com*

   +--------+-----------+-------+-----------------------------------+
   |Name    |Type       |Default|Description                        |
   +========+===========+=======+===================================+
   |d_pacmod|TyDic      |{}     |pacmod dictionary                  |
   +--------+-----------+-------+-----------------------------------+
   |pid     |TyInt      |None   |current Process id                 |
   +--------+-----------+-------+-----------------------------------+
   |sw_init |TyBool     |None   |Initialisation switch              |
   +--------+-----------+-------+-----------------------------------+
   |**Timestamp fields**                                            |
   +--------+-----------+-------+-----------------------------------+
   |ts      |TnTimeStamp|None   |Timestamp                          |
   +--------+-----------+-------+-----------------------------------+
   |ts_start|TnDateTime |None   |start timestamp in date time format|
   +--------+-----------+-------+-----------------------------------+
   |ts_end  |TnDateTime |None   |end timestamp in date time format  |
   +--------+-----------+-------+-----------------------------------+
   |ts_etime|TnDateTime |None   |elapse Time                        |
   +--------+-----------+-------+-----------------------------------+
   |d_timer |TyDic      |False  |Timer dictionary                   |
   +--------+-----------+-------+-----------------------------------+
   |**Links to other Classes**                                      |
   +--------+-----------+-------+-----------------------------------+
   |App     |TyAny      |False  |Application class                  |
   +--------+-----------+-------+-----------------------------------+
   |cfg     |TyDic      |None   |Configuration dictionary           |
   +--------+-----------+-------+-----------------------------------+
   |Log     |TyLogger   |False  |Log class                          |
   +--------+-----------+-------+-----------------------------------+
   |Exit    |TyAny      |False  |Exit class                         |
   +--------+-----------+-------+-----------------------------------+

Methods
^^^^^^^

  .. Methods-of-class-Com-label:
  .. table:: *Methods-of-class-Com*

   +---------+-------------------------------------------------------+
   |Name     |Description                                            |
   +=========+=======================================================+
   |init     |Initialise static variables if they are not initialized|
   +---------+-------------------------------------------------------+
   |sh_kwargs|Show keyword arguments                                 |
   +---------+-------------------------------------------------------+

Method init
^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-init-label:
  .. table:: *Parameter-of-method-init*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|keyword arguments|
   +---------+-----+-----------------+

Method sh_kwargs
^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-sh_kwargs-label:
  .. table:: *Parameter of method sh_kwargs*

   +--------+-----+--------------------+
   |Name    |Type |Description         |
   +========+=====+====================+
   |cls     |class|current class       |
   +--------+-----+--------------------+
   |root_cls|class|root lass           |
   +--------+-----+--------------------+
   |d_parms |TyDic|parameter dictionary|
   +--------+-----+--------------------+
   |\*args  |list |arguments array     |
   +--------+-----+--------------------+

Time management Module timer.py
===============================

Classes
-------

The Module ``timer.py`` contains the following classes


  .. Static-classes-of-module-timer.py-label:
  .. table:: *Static classes of module timer.py*

   +---------+------+---------------+
   |Name     |Type  |Description    |
   +=========+======+===============+
   |Timestamp|static|Timestamp class|
   +---------+------+---------------+
   |Timer    |static|Timer class    |
   +---------+------+---------------+


Class Timer
-----------

Methods
^^^^^^^

  .. Methods-of-class-Timer-label:
  .. table:: *Methods of class Timer*

   +----------+------------------------------------+
   |Name      |Description                         |
   +==========+====================================+
   |sh_task_id|Show task id                        |
   +----------+------------------------------------+
   |start     |Start Timer                         |
   +----------+------------------------------------+
   |end       |End Timer and Log Timer info message|
   +----------+------------------------------------+

Method sh_task_id
^^^^^^^^^^^^^^^^^
        
Show task id, which is created by the concatination of the following items if they are defined:
#. package,
#. module,
#. class_name,
#. parms
The items package and module are get from the package-module directory;
The item class_name is the class_id if its a string, otherwise the attribute
__qualname__ is used.
        
Parameter
"""""""""

  .. Parameter-of-method-sh_task_id-label:
  .. table:: *Parameter-of-method-sh_task_id*

   +--------+-----+-----------------+
   |Name    |Type |Description      |
   +========+=====+=================+
   |d_pacmod|TyDic|pacmod dictionary|
   +--------+-----+-----------------+
   |class_id|TyAny|Class Id         |
   +--------+-----+-----------------+
   |parms   |TnAny|Parameters       |
   +--------+-----+-----------------+
   |sep     |TyStr|Separator        |
   +--------+-----+-----------------+

Return Value
""""""""""""

  .. Return-value-of-method-sh_task_id-label:
  .. table:: *Return value of method sh_task_id*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |    |TyStr|Task Id    |
   +----+-----+-----------+

Method start
^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-start-label:
  .. table:: *Parameter of method start*

   +--------+-----+-------------+
   |Name    |Type |Description  |
   +========+=====+=============+
   |cls     |class|current class|
   +--------+-----+-------------+
   |class_id|TyAny|Class Id     |
   +--------+-----+-------------+
   |parms   |TnAny|Parameter    |
   +--------+-----+-------------+
   |sep     |TyStr|Separator    |
   +--------+-----+-------------+

Method: end
^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-end-method-label:
  .. table:: *Parameter of end method*

   +--------+-----+-------------+
   |Name    |Type |Description  |
   +========+=====+=============+
   |cls     |class|current class|
   +--------+-----+-------------+
   |class_id|TyAny|Class Id     |
   +--------+-----+-------------+
   |parms   |TnAny|Parameter    |
   +--------+-----+-------------+
   |sep     |TyStr|Separator    |
   +--------+-----+-------------+

Base Modules
************

Overview
========

  .. Base Modules-label:
  .. table:: *Base Modules*

   +---------+----------------------------+
   |Name     |Decription                  |
   +=========+============================+
   |app\_.py |Application setup module    |
   +---------+----------------------------+
   |cfg\_.py |Configuration setup module  |
   +---------+----------------------------+
   |exit\_.py|Exit Manafement setup module|
   +---------+----------------------------+

Application setup module: app\_.py
==================================

The Module ``app.py`` contains a single static class ``App_``.

Class: App\_
------------

The static class ``App_`` contains the subsequent static variables and methods

Static Variables
^^^^^^^^^^^^^^^^

  .. Static-variables-of-class-App_-label:
  .. table:: *Static Variables of class App_*

   +---------------+-------+-------+---------------------+
   |Name           |Type   |Default|Description          |
   +===============+=======+=======+=====================+
   |sw_init        |TyBool |False  |initialisation switch|
   +---------------+-------+-------+---------------------+
   |httpmod        |TyDic  |None   |http modus           |
   +---------------+-------+-------+---------------------+
   |sw_replace_keys|TnBool |False  |replace keys switch  |
   +---------------+-------+-------+---------------------+
   |keys           |TnArr  |None   |Keys array           |
   +---------------+-------+-------+---------------------+
   |reqs           |TyDic  |None   |Requests dictionary  |
   +---------------+-------+-------+---------------------+
   |app            |TyDic  |None   |Appliction dictionary|
   +---------------+-------+-------+---------------------+

Methods
^^^^^^^

  .. Methods-of-class-App_-label:
  .. table:: *Methods of class App_*

   +----+------+------------------------------------+
   |Name|Type  |Description                         |
   +====+======+====================================+
   |init|class |initialise static variables of class|
   |    |      |if they are not allready initialized|
   +----+------+------------------------------------+
   |sh  |class |show (return) class                 |
   +----+------+------------------------------------+

Method: init
^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-init-label:
  .. table:: *Parameter of method init*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Method: sh
^^^^^^^^^^
        
  .. Parameter-of-method-sh-label:
  .. table:: *Parameter of method sh*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Return Value
""""""""""""

  .. Return-values-of-method-sh-label:
  .. table:: *Return values of method sh*

   +----+--------+-----------+
   |Name|Type    |Description|
   +====+========+===========+
   |log |TyLogger|Logger     |
   +----+--------+-----------+

cfg\_.py
========

The Base module cfg\_.py contains a single static class ``Cfg_``.

Class Cfg\_
-----------

The static class ``Cfg_`` contains the subsequent static variables and methods

Static Variables
^^^^^^^^^^^^^^^^

  .. Static-variables-of-Cfg_-label:
  .. table:: *Static Variables of Cfg_*

   +----+-----+-------+--------------------+
   |Name|Type |Default|Description         |
   +====+=====+=======+====================+
   |cfg |TyDic|None   |Configuration object|
   +----+-----+-------+--------------------+

Methods
^^^^^^^

  .. Methods-of-class-Cfg_-label:
  .. table:: *Methods of class Cfg_*

   +----+------+-----------------------------------+
   |Name|Type  |Description                        |
   +====+======+===================================+
   |sh  |class |read pacmod yaml file into class   |
   |    |      |variable cls.dic and return cls.cfg|
   +----+------+-----------------------------------+

Method: sh
^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-init-label:
  .. table:: *Parameter of method sh*

   +--------+--------+-----------------+
   |Name    |Type    |Description      |
   +========+========+=================+
   |cls     |class   |Current class    |
   +--------+--------+-----------------+
   |log     |TyLogger|Logger           |
   +--------+--------+-----------------+
   |d_pacmod|TyDic   |pacmod dictionary|
   +--------+--------+-----------------+

Return Value
""""""""""""

  .. Return-values-of-method-sh-label:
  .. table:: *Return values of method sh*

   +-------+-----+-----------+
   |Name   |Type |Description|
   +=======+=====+===========+
   |cls.cfg|TyDic|           |
   +-------+-----+-----------+

Base Modul ext\_.py
===================

The Base module exit\_.py contains a single static class ``Ext_``.

class Exit\_
------------

The static Class ``Exit_`` contains the subsequent static variables and methods.

Static Variables
^^^^^^^^^^^^^^^^

  .. Static variables-of-class-Ext_-label:
  .. table:: *Static variables of class Ext_*

   +--------------+------+-------+---------------------+
   |Name          |Type  |Default|Description          |
   +==============+======+=======+=====================+
   |sw_init       |TyBool|False  |initialisation switch|
   +--------------+------+-------+---------------------+
   |sw_critical   |TyBool|False  |critical switch      |
   +--------------+------+-------+---------------------+
   |sw_stop       |TyBool|False  |stop switch          |
   +--------------+------+-------+---------------------+
   |sw_interactive|TyBool|False  |interactive switch   |
   +--------------+------+-------+---------------------+

Methods
^^^^^^^

  .. Methods-of-class-Ext_-label:
  .. table:: *Methods of class Ext_*

   +----+------+------------------------------------+
   |Name|Method|Description                         |
   +====+======+====================================+
   |init|class |initialise static variables of class|
   |    |      |if they are not allready initialized|
   +----+------+------------------------------------+
   |sh  |class |show (return) class                 |
   +----+------+------------------------------------+

Method: init
^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-init-label:
  .. table:: *Parameter of method init*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Method: sh
^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-method-sh-label:
  .. table:: *Parameter of method sh*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Return Value
""""""""""""

  .. Return-values-of-method-sh-label:
  .. table:: *Return values of method sh*

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |cls |class|Current class|
   +----+-----+-------------+

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
