from django.contrib.gis.gdal.datasource import DataSource
from django.contrib.gis.gdal.error import OGRIndexError
from django.contrib.gis.gdal.feature import Feature
from django.contrib.gis.gdal.layer import Layer
from django.contrib.gis.gdal.prototypes import ds as capi
from django.contrib.gis.utils import LayerMapping


class FilteredLayer( Layer ):
    def __init__(self, layer_ptr, ds, filter_map=None):
        super( FilteredLayer, self ).__init__( layer_ptr, ds )
        self.filter_map = filter_map or dict()

    def __iter__(self):
        capi.reset_reading(self._ptr)
        for i in xrange(self.num_feat):
            feat = Feature(capi.get_next_feature(self._ptr), self._ldefn)
            if not self.__filter(feat):
                continue
            yield feat

    def __getitem__(self, index):
        if isinstance(index, (int, long)):
            if index < 0:
                raise OGRIndexError('Negative indices are not allowed on OGR Layers.')
            return self._make_feature(index)
        elif isinstance(index, slice):
            start, stop, stride = index.indices(self.num_feat)
            result = []
            for fid in xrange(start, stop, stride):
                feat = self._make_feature(fid)
                if not self.__filter(feat):
                    continue
                result.append(feat)
            return result
        else:
            raise TypeError('Integers and slices may only be used when indexing OGR Layers.')

    def __filter( self, feat ):
        result = True
        for key, value in self.filter_map.items():
            ogr_name, action = key.split('__')
            test = feat[ogr_name].value
            if action == 'equal':
                result = test == value
            elif action == 'in':
                result = test in value
            elif action == 'lte':
                result = test <= value
            elif action == 'gte':
                result = test >= value
        return result


class FilteredDataSource( DataSource ):

    def __init__( self, ds_input, filter_map=None, **kwargs ):
        self.filter_map = filter_map or dict()
        super( FilteredDataSource, self ).__init__( ds_input, **kwargs )

    def __getitem__(self, index):
        if isinstance(index, basestring):
            l = capi.get_layer_by_name(self.ptr, index)
            if not l:
                raise OGRIndexError('invalid OGR Layer name given: "%s"' % index)
        elif isinstance(index, int):
            if index < 0 or index >= self.layer_count:
                raise OGRIndexError('index out of range')
            l = capi.get_layer(self._ptr, index)
        else:
            raise TypeError('Invalid index type: %s' % type(index))
        return FilteredLayer(l, self, filter_map=self.filter_map)


class GisMapping( LayerMapping ):
    def __init__( self, model, data, mapping, filter_map, **kwargs ):
        if isinstance(data, basestring):
            data = FilteredDataSource(data, filter_map)
        super( GisMapping, self ).__init__( model, data, mapping, **kwargs )
