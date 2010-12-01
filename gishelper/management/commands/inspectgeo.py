from gishelper.management.commands import GisCommand


class Command( GisCommand ):
    help = "Create model and mapping for shape file."

    def gishandle( self, model_name, filepath, *args, **options ):
        from django.contrib.gis.utils import ogrinspect, mapping

        print ogrinspect( filepath, model_name, srid=options['srid'], blank=True )
        print "\n\n%s_mapping = %s" % ( model_name.lower(), mapping( filepath ))
