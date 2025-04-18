import os
from osgeo import gdal, ogr
import numpy as np

def create_ndvi_vrt(input_image, nir_band=4, red_band=3, output_vrt="ndvi.vrt"):
    ds = gdal.Open(input_image)
    nir = ds.GetRasterBand(nir_band).ReadAsArray().astype(np.float32)
    red = ds.GetRasterBand(red_band).ReadAsArray().astype(np.float32)
    ndvi = (nir - red) / (nir + red + 1e-9)  # avoid division by zero

    mem_drv = gdal.GetDriverByName("MEM")
    mem_ds = mem_drv.Create("", ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32)
    mem_ds.SetGeoTransform(ds.GetGeoTransform())
    mem_ds.SetProjection(ds.GetProjection())
    mem_ds.GetRasterBand(1).WriteArray(ndvi)

    gdal.GetDriverByName("VRT").CreateCopy(output_vrt, mem_ds)
    ds, mem_ds = None, None
    return output_vrt

def create_threshold_vector(ndvi_vrt, threshold_val, operator_str="<=", output_gpkg="mask.gpkg"):
    ds = gdal.Open(ndvi_vrt)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()

    if operator_str == "<=":
        mask = arr <= threshold_val
    elif operator_str == ">=":
        mask = arr >= threshold_val
    elif operator_str == "<":
        mask = arr < threshold_val
    elif operator_str == ">":
        mask = arr > threshold_val
    elif operator_str == "==":
        mask = arr == threshold_val
    else:
        raise ValueError("Unsupported operator")

    mask = mask.astype(np.uint8)

    mem_ds = gdal.GetDriverByName("MEM").Create("", ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
    mem_ds.SetGeoTransform(ds.GetGeoTransform())
    mem_ds.SetProjection(ds.GetProjection())
    mem_ds.GetRasterBand(1).WriteArray(mask)

    drv = ogr.GetDriverByName("GPKG")
    if os.path.exists(output_gpkg):
        drv.DeleteDataSource(output_gpkg)
    out_ds = drv.CreateDataSource(output_gpkg)
    out_lyr = out_ds.CreateLayer("mask", srs=None)
    out_lyr.CreateField(ogr.FieldDefn("DN", ogr.OFTInteger))

    gdal.Polygonize(mem_ds.GetRasterBand(1), mem_ds.GetRasterBand(1), out_lyr, 0, [])
    ds, mem_ds, out_ds = None, None, None
    return output_gpkg

def main():
    input_tif = "input.tif"
    nir_band_num = 4
    red_band_num = 3
    ndvi_vrt = "ndvi_output.vrt"
    threshold_value = 0.2
    operator_text = "<="
    out_gpkg = "low_veg_mask.gpkg"

    create_ndvi_vrt(input_tif, nir_band_num, red_band_num, ndvi_vrt)
    create_threshold_vector(ndvi_vrt, threshold_value, operator_text, out_gpkg)

if __name__ == "__main__":
    main()