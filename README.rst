liapi
=====

install
-------
.. code-block:: bash

   git clone git@github.com:dincamihai/liwrapper.git
   cd liwrapper
   virtualenv sandbox
   . sandbox/bin/activate
   pip install -r requirements-dev.txt

run tests
---------
.. code-block:: bash

   py.test

use
---
.. code-block:: bash

   LOAD_IMPACT_TOKEN=<token> ./script tests/sample.jmx

task management
---------------

TODO
````
- convert wrapper to package with exacutable script
- establish how data extracted from jmx translates to configuration params

    +----------------+--------------+
    | xml attribute  | config param |
    +================+==============+
    | test_plan_name | name         |
    +----------------+--------------+
    | domain         | url [param]  |
    +----------------+--------------+
- validate jmx with xml schema
- check if there are unhandled exceptions in script
- validate json extractor configuration and handle errors

DONE
````
- improve extractor to allow accept flexible json extraction instructions
- script creates config (not just scenario)
- handle data extraction errors
- handle scenario creation errors 400 and 401 as an example and use raise_for_status to handle the rest
- handle configuration creation errors using raise_for_status
- create separate extractor python package and use it
