import os.path
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

class GisCommand( BaseCommand ):
    option_list = BaseCommand.option_list + (
        make_option( '-f', '--file', default=None, dest='file', help='Shape file path.' ),
        make_option( '-m', '--model', default=None, dest='model', help='Model name' ),
        make_option( '-e', '--encoding', default='utf-8', dest='encoding', help='Source encoding' ),
        make_option( '-s', '--srid', default='4326', dest='srid', help='Source srid' ),
        make_option( '-u', '--using', default=None, dest='using', help='DB_ALIAS' ),
    )

    def handle( self, *args, **options ):
        try:
            model_name = options['model']
            filepath = options['file']
            assert filepath and model_name
        except ( AssertionError, KeyError ):
            raise CommandError('Usage error. Not required options: --model or --file.')

        if not os.path.exists( filepath ):
            raise CommandError( "File '%s' not exists." % filepath)

        self.gishandle( self, model_name, filepath, *args, **options )

    def gishandle( self, model_name, filepath, *args, **options ):
        raise NotImplementedError()

