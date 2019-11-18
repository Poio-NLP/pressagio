Welcome to pressagio's documentation!
=====================================

Pressagio is a library that predicts text based on n-gram models. For example,
you can send a string and the library will return the most likely word
completions for the last token in the string.

Example Usage
-------------

The repository contains two example scripts  in the folder :code:`example` to
demonstrate how to build a language model and use the model for prediction.
You can check the code of those two scripts how to use pressagio in your own
projects. Here is how to use the two scripts to predict the next word in a
phrase.

First, you have to build a languange model. We will use the script
`example/text2ngram.py <https://github.com/Poio-NLP/pressagio/blob/master/example/text2ngram.py>`_
to add 1-, 2- and 3-grams of a given text to a sqlite database. For
demonstration purposes we will use a simple text file that comes with
pressagio's tests. You have to run the script three times to create a table
for each of the n-grams:

.. code:: bash

    $ python example/text2ngram.py -n 1 -o test.sqlite tests/test_data/der_linksdenker.txt
    $ python example/text2ngram.py -n 2 -o test.sqlite tests/test_data/der_linksdenker.txt
    $ python example/text2ngram.py -n 3 -o test.sqlite tests/test_data/der_linksdenker.txt

This will create  a file :code:`test.sqlite` in the current directory. We can now
use this database to get a prediction for a phrase. We will use the script
`example/predict.py <https://github.com/Poio-NLP/pressagio/blob/master/example/predict.py>`_
which uses the configuration file
`example/example_profile.ini <https://github.com/Poio-NLP/pressagio/blob/master/example/example_profile.ini>`_.
Note that you will always need a configuration file if you want to use the
built-in predictor. To get a prediction call:

.. code:: bash

    $ python example/predict.py
    ['warm', 'der', 'und', 'die', 'nicht']

The script will just output a list of predictions.

Running the tests
-----------------

.. code:: bash

    $ python -m unittest discover


API documentation
=================

.. toctree::
   :maxdepth: 2

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

