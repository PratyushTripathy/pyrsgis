# pyrsgis/utils

# safely import gdal (support old version)
try:
    import gdal
except:
    from osgeo import gdal

"""
Create data type dictionaries to call later
"""
datatype_dict_str_num = {
    'byte': gdal.GDT_Byte,
    'cfloat32': gdal.GDT_CFloat32,
    'cfloat64': gdal.GDT_CFloat64,
    'cint16': gdal.GDT_CInt16,
    'cint32': gdal.GDT_CInt32,
    'float': gdal.GDT_Float32,
    'float32': gdal.GDT_Float32,
    'float64': gdal.GDT_Float64,
    'int': gdal.GDT_Int16,
    'int16': gdal.GDT_Int16,
    'int32': gdal.GDT_Int32,
    'uint8': gdal.GDT_Byte,
    'uint16': gdal.GDT_UInt16,
    'uint32': gdal.GDT_UInt32
}

datatype_dict_num_str = {
    gdal.GDT_Byte: 'byte',
    gdal.GDT_CFloat32: 'cfloat32',
    gdal.GDT_CFloat64: 'cfloat64',
    gdal.GDT_CInt16: 'cint16',
    gdal.GDT_CInt32: 'cint32',
    gdal.GDT_Float32: 'float',
    gdal.GDT_Float64: 'float64',
    gdal.GDT_Int16: 'int',
    gdal.GDT_Int32: 'int32',
    gdal.GDT_UInt16: 'uint16',
    gdal.GDT_UInt32: 'uint32'
}


