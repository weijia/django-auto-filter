=============================
django-auto-filter
=============================

.. image:: https://badge.fury.io/py/django-auto-filter.png
    :target: https://badge.fury.io/py/django-auto-filter

.. image:: https://travis-ci.org/weijia/django-auto-filter.png?branch=master
    :target: https://travis-ci.org/weijia/django-auto-filter

"An automatically generated filter page for django application"

Documentation
-------------

The full documentation is at https://django-auto-filter.readthedocs.org.

Quickstart
----------

Install django-auto-filter::

    pip install django-auto-filter

Then use it in a project

urls.py::

    from django.conf.urls import patterns, url
    from django_auto_filter.views_django_auto_filter import DjangoAutoFilter
    from django.contrib.auth.models import User

    urlpatterns = patterns('',
                           url(r'', DjangoAutoFilter.as_view(model_class=User)),
                           )

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
