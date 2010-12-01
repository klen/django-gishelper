from django.core.management.base import CommandError

from gishelper.management.commands import GisCommand


class Command( GisCommand ):
    help = "Load geo data in application"
    args = '<appname>'

    def gishandle( self, model_name, filepath, *args, **options ):
        from django.db.models import get_app

        app_name = args[0]
        app = get_app(app_name)

        try:
            model = getattr(app, model_name)
        except AttributeError:
            raise CommandError("Model '%s' not found in %s.models" % ( app_name, model_name ))

        try:
            mapping = getattr(app, "%s_mapping" % options['model'].lower())
        except AttributeError:
            raise CommandError("Mapping '%s_mapping' not found in %s.models" % ( app_name, model_name ))

        options = dict( encoding=options['encoding'], source_srs=options['srid'] )
        load(model, filepath, mapping, options)


def load( model, filepath, mapping, options ):
    from django.contrib.gis.utils import LayerMapping
    lm = LayerMapping(model, filepath, mapping, **options)
    lm.save(strict=True, progress=True, step=1000)
