from django.conf import settings

GIS_APPS = settings.GISHELPER_GIS_APPS or list()
GIS_DB = 'default'
GIS_MODELS = ('SpatialRefSys','GeometryColumns')

for db_name, db_params in settings.DATABASES.items():
    if db_params['ENGINE'].startswith('django.contrib.gis.db.backends'):
        GIS_DB = db_name
        break

class GisRouter( object ):
    """ Router for geo databases.
    """

    def db_for_read( self, model, **hints ):
        """ Read geo models only from geo db.
        """
        return self.__get_db_for_model( model )

    def db_for_write( self, model, **hints ):
        """ Write geo models only geo db.
        """
        return self.__get_db_for_model( model )

    def allow_syncdb( self, db, model ):
        """ Sync geo db only geo models.
        """
        if db == GIS_DB:
            return self.__check_geo_model(model)
        elif self.__check_geo_model(model):
            return False
        return None

    def __get_db_for_model( self, model ):
        """ Route geo db.
        """
        if self.__check_geo_model(model):
            return GIS_DB
        return None

    @staticmethod
    def __check_geo_model( model ):
        return model._meta.app_label in GIS_APPS or model._meta.object_name in GIS_MODELS
