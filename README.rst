..   -*- mode: rst -*-

django-gishelper
#################

**Gishelper** is python django application with useful commands for django.gis module.

.. contents::

Requirements
-------------

- python >= 2.5
- pip >= 0.8


Installation
------------

**Gishelper** should be installed using pip: ::

    pip install git+git://github.com/klen/django-gishelper.git


Setup
------

- Add gishelper to INSTALLED_APPS ::

  INSTALLED_APPS += ( 'gishelper', )

- Add gishelper router to DATABASE_ROUTERS ::

  DATABASE_ROUTERS = [ 'gishelper.router.GisRouter', ]

- Add GISHELPER_GIS_APPS with your gis app labels to settings ::

  GISHELPER_GIS_APPS =  ( 'my_gis_app', )


Usage
------

- Inspect shape maps and show django gis model structure and mapping ::

    ./manage.py inspectgeo -f FILEPATH -m MODEL_NAME -s SRID -u USE_DB_ALIAS

- Load data in postgis (mapping and filter) command parse from app.models::

    ./manage.py loadgeo APP_NAME -f FILEPATH -m MODEL -s SRID -u USE_DB_ALIAS

'loadgeo' can filtrate source, define in models file dict '<lower_model_name>_filter' where keys OGR_NAME of features and condition. 

Example: ::

    poi_filter = dict(AMENITY__in = ( city, town ))


Note
-----

You need to setup geodjango_ as described in geodjango documentation


.. _geodjango: http://docs.djangoproject.com/en/dev/ref/contrib/gis/
