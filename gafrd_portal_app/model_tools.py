import os.path

import numpy as np
from PIL import Image
from osgeo import gdal
from osgeo import ogr, osr
import matplotlib.pyplot as plt
import matplotlib.colors as clr


class TSModel:

    @staticmethod
    def vector_to_raster(in_shp, out_raster, pixel_size=0.001, burn_value=1):
        """
        Vector to Raster process found in tools:
            [1, 4, 7, 10]

        :param in_shp: input shapefile.
        :param out_raster: output raster tif file.
        :param pixel_size: pixel size of output raster (default: 1000 meter).
        :param burn_value: pixel value inside polygon.
        """

        '''
        input_shp = ogr.Open(in_shp)
        shp_layer = input_shp.GetLayer()

        xmin, xmax, ymin, ymax = shp_layer.GetExtent()
        ds = gdal.Rasterize(out_raster, in_shp, xRes=pixel_size, yRes=pixel_size,
                            burnValues=burn_value, outputBounds=[xmin, ymin, xmax, ymax],
                            outputType=gdal.GDT_UInt16)
        ds = None
        '''

        NoData_value = 10000

        # Open the data source and read in the extent
        source_ds = ogr.Open(in_shp)
        source_layer = source_ds.GetLayer()
        x_min, x_max, y_min, y_max = source_layer.GetExtent()
        source_srs = source_layer.GetSpatialRef()

        # Create the destination data source
        x_res = int((x_max - x_min) / pixel_size)
        y_res = int((y_max - y_min) / pixel_size)

        target_ds = gdal.GetDriverByName('GTiff').Create(out_raster, x_res, y_res, 1, gdal.GDT_UInt16)
        target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(NoData_value)

        target_ds.SetProjection(source_srs.ExportToWkt())


        # Rasterize
        # gdal.RasterizeLayer(target_ds,
        #                    [1], source_layer,
        #                    burn_values=[3]) # try to burn a contant value (3)

        # Rasterize
        gdal.RasterizeLayer(target_ds,
                            [1], source_layer, burn_values=[burn_value],
                            options=["ALL_TOUCHED=TRUE"])  # using an attribute from the shapefile

    @staticmethod
    def is_null(in_raster, out_raster):
        """
        Is Null process found in tools:
            [2, 5, 8, 11]

        :param in_raster: input raster tif file.
        :param out_raster: output raster tif file.
        """

        ds = gdal.Open(in_raster)
        band = ds.GetRasterBand(1)
        ndv = band.GetNoDataValue()
        if ndv is None:
            ndv = 10000
        band_arr = band.ReadAsArray()
        band_arr = 0.0001 * band_arr

        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(out_raster, band_arr.shape[1], band_arr.shape[0], 1, gdal.GDT_UInt16)
        outdata.SetGeoTransform(ds.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr)
        outdata.GetRasterBand(1).SetNoDataValue(ndv)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None

    @staticmethod
    def clip_raster(in_ras, in_clipper, out_clipped_ras):
        """
        Clip raster process found in tools:
            [3, 6, 9, 12]

        :param in_ras: Raster tif file.
        :param in_clipper: Vector shapefile containing a polygon.
        :param out_clipped_ras: A clipped raster tif file.
        """

        nan_value = -3.4028230607370965e+38  # 2**16 - 1
        nan_value = 10000

        OutTile = gdal.Warp(out_clipped_ras, in_ras, cutlineDSName=in_clipper, cropToCutline=True, dstNodata=nan_value)
        OutTile = None
        temp = gdal.Open(out_clipped_ras)

    @staticmethod
    def raster_calc_mul(input_list, output_raster):
        """
        Multiplication of rasters Process found in tools:
            Tool 13: Type1: Input1 * Input2 * Input3 * Input4
            Tool 29: Type1: Input1 * Input2

        :param input_list: list containing strings for full path of 4 or 2 raster tif files.
        :param output_raster: contains string for full path of output raster tif file.
        """

        nan_value = -3.4028230607370965e+38  # 2**16 - 1
        nan_value = 10000

        nParams = len(input_list)
        # 4 params for tool 13 and 2 params for tool 29
        if nParams not in [2, 4]:
            print("\nError in first parameter: must be a list consists of 2 or 4 strings.")
            return

        input1 = input_list[0]
        ds1 = gdal.Open(input1)
        band1 = ds1.GetRasterBand(1)
        ndv1 = band1.GetNoDataValue()
        band_arr1 = band1.ReadAsArray()
        b1 = np.where(band_arr1 == 10000.0)
        band_arr1[band_arr1 == ndv1] = nan_value
        transform = ds1.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols1 = ds1.RasterXSize
        rows1 = ds1.RasterYSize
        input2 = input_list[1]
        ds2 = gdal.Open(input2)
        band2 = ds2.GetRasterBand(1)
        ndv2 = band2.GetNoDataValue()
        band_arr2 = band2.ReadAsArray()
        b2 = np.where(band_arr2 == 10000.0)
        band_arr2[band_arr2 == ndv2] = nan_value
        transform = ds2.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols2 = ds2.RasterXSize
        rows2 = ds2.RasterYSize
        if nParams == 2:
            min_cols = min([cols1, cols2])
            min_rows = min([rows1, rows2])

            band_arr1 = band_arr1[:min_rows, :min_cols]
            band_arr2 = band_arr2[:min_rows, :min_cols]
            b1 = np.where(band_arr1 == 10000.0)
            b2 = np.where(band_arr2 == 10000.0)
            band_arr_all = 1.0 * band_arr1 * band_arr2
            band_arr_all[b1] = nan_value
            band_arr_all[b2] = nan_value

            driver = gdal.GetDriverByName("GTiff")
            outdata = driver.Create(output_raster, band_arr1.shape[1], band_arr1.shape[0], 1, gdal.GDT_Float32)

        else:
            input3 = input_list[2]
            ds3 = gdal.Open(input3)
            band3 = ds3.GetRasterBand(1)
            ndv3 = band3.GetNoDataValue()
            band_arr3 = band3.ReadAsArray()
            band_arr3[band_arr3 == ndv3] = nan_value
            cols3 = ds3.RasterXSize
            rows3 = ds3.RasterYSize

            input4 = input_list[3]
            ds4 = gdal.Open(input4)
            band4 = ds4.GetRasterBand(1)
            ndv4 = band4.GetNoDataValue()
            band_arr4 = band4.ReadAsArray()
            band_arr4[band_arr4 == ndv4] = nan_value
            cols4 = ds4.RasterXSize
            rows4 = ds4.RasterYSize

            min_cols = min([cols1, cols2, cols3, cols4])
            min_rows = min([rows1, rows2, rows3, rows4])
            band_arr1 = band_arr1[:min_rows, :min_cols]
            band_arr2 = band_arr2[:min_rows, :min_cols]
            band_arr3 = band_arr3[:min_rows, :min_cols]
            band_arr4 = band_arr4[:min_rows, :min_cols]
            band_arr_all = 0.25 * (band_arr1 + band_arr2 + band_arr3 + band_arr4)
            band_arr_all[np.where(band_arr_all < 1.0)] = 0
            band_arr_all[np.where(band_arr_all == 1.0)] = 1
            band_arr_all[np.where(band_arr_all > 1.0)] = 10000

            band_arr_all[band_arr_all == nan_value] = ndv1
            driver = gdal.GetDriverByName("GTiff")
            outdata = driver.Create(output_raster, band_arr1.shape[1], band_arr1.shape[0], 1, gdal.GDT_UInt16)

        outdata.SetGeoTransform(ds1.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds1.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr_all)

        outdata.GetRasterBand(1).SetNoDataValue(ndv1)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None
        ds1 = None
        ds2 = None
        ds3 = None
        ds4 = None

    @staticmethod
    def raster_calc_add(input_list, weight_list, output_raster):
        """
            Addition of rasters Process found in tools:
                Tool 18: \n\t(Input1 * 0.09) + (Input2 * 0.455) + (Input3 * 0.273) + (Input4 * 0.182)\n
                Tool 21: \n\t(Input1 * 0.143) + (Input2 * 0.238)\n
                Tool 26: \n\t(Input1 * 0.15) + (Input2 * 0.503) + (Input3 * 0.096) + (Input4 * 0.251)\n
                Tool 28: \n\t(Input1 * 0.391) + (Input2 * 0.087) + (Input3 * 0.262) + (Input4 * 0.217)\n

            :param input_list: list containing strings for full path of 4 or 2 raster tif files.
            :param weight_list: list containing float values for weight of equation.
            :param output_raster: contains string for full path of output raster tif file.
            """

        # nan_value = -3.4028230607370965e+38  # 2**16 - 1
        nan_value = 10000

        nParams = len(input_list)
        nWeights = len(weight_list)
        if nParams != nWeights:
            print("\nError in first & Second parameters: Two lists must be the same length.")
            return

        # 4 params for tool 18, 26, 28 and 2 params for tool 21
        if nParams not in [2, 4]:
            print("\nError in first parameter: must be a list consists of 2 or 4 strings.")
            return

        input1 = input_list[0]
        weight1 = weight_list[0]
        ds1 = gdal.Open(input1)
        band1 = ds1.GetRasterBand(1)
        ndv1 = band1.GetNoDataValue()
        band_arr1 = band1.ReadAsArray()
        b1 = np.where(band_arr1 == 10000.0)
        transform = ds1.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols1 = ds1.RasterXSize
        rows1 = ds1.RasterYSize

        input2 = input_list[1]
        weight2 = weight_list[1]
        ds2 = gdal.Open(input2)
        band2 = ds2.GetRasterBand(1)
        ndv2 = band2.GetNoDataValue()
        band_arr2 = band2.ReadAsArray()
        b2 = np.where(band_arr2 == 10000.0)
        transform = ds2.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols2 = ds2.RasterXSize
        rows2 = ds2.RasterYSize

        if nParams == 2:
            min_cols = min([cols1, cols2])
            min_rows = min([rows1, rows2])

            band_arr1 = band_arr1[:min_rows, :min_cols]
            band_arr2 = band_arr2[:min_rows, :min_cols]

            band_arr_all = (weight1 * band_arr1) + (weight2 * band_arr2)
            band_arr_all[b1] = 10000
            band_arr_all[b2] = 10000
        else:
            input3 = input_list[2]
            weight3 = weight_list[2]
            ds3 = gdal.Open(input3)
            band3 = ds3.GetRasterBand(1)
            ndv3 = band3.GetNoDataValue()
            band_arr3 = band3.ReadAsArray()
            b3 = np.where(band_arr3 == 10000.0)

            input4 = input_list[3]
            weight4 = weight_list[3]
            ds4 = gdal.Open(input4)
            band4 = ds4.GetRasterBand(1)
            ndv4 = band4.GetNoDataValue()
            band_arr4 = band4.ReadAsArray()
            b4 = np.where(band_arr4 == 10000.0)

            band_arr_all = (weight1 * band_arr1) + (weight2 * band_arr2) + (weight3 * band_arr3) + (weight4 * band_arr4)
            band_arr_all[b1] = 10000
            band_arr_all[b2] = 10000
            band_arr_all[b3] = 10000
            band_arr_all[b4] = 10000

        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(output_raster, band_arr1.shape[1], band_arr1.shape[0], 1, gdal.GDT_Float32)
        outdata.SetGeoTransform(ds1.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds1.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr_all)

        outdata.GetRasterBand(1).SetNoDataValue(nan_value)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None
        ds1 = None
        ds2 = None
        ds3 = None
        ds4 = None

    @staticmethod
    def raster_reclassify(input_raster, reclassify_list, output_raster):
        """
        Reclassify process found in tools:
            [14, 15, 16, 17, 19, 20, 22, 23, 24, 25, 27, 30]

        Tool14 : \n\t[(0, 1000, 4), (1000, 2500, 3), (2500, 3500, 2), (3500, 100000, 1)]\n
        Tool15": \n\t[(0, 0.02, 1), (0.02, 0.2, 2), (0.2, 0.35, 3), (0.35, 1, 4)]\n
        Tool16": \n\t[(0, 20, 1), (20, 1000, 4), (1000, 2500, 3), (2500, 3500, 2), (3500, 100000, 1)]\n
        Tool17": \n\t[(0, 200, 1), (200, 300, 1), (300, 700, 2), (700, 1000, 3), (1000, 3000, 4)]\n
        Tool19": \n\t[(0, 0.04, 1), (0.04, 0.2, 2), (0.2, 0.35, 3), (0.35, 1, 4)]\n
        Tool20": \n\t[(0, 5000, 4), (5000, 10000, 3), (10000, 15000, 2), (15000, 100000, 1)]\n
        Tool22": \n\t[(0, 1, 1), (1, 1.5, 2), (1.5, 2.5, 4), (2.5, 18, 3), (18, 100, 1)]\n
        Tool23": \n\t[(0, 20, 1), (20, 40, 2), (40, 60, 3), (60, 100, 4)]\n
        Tool24": \n\t[(1, 4, 1), (4, 5.5, 2), (5.5, 6.5, 3), (6.5, 8.5, 4)]\n
        Tool25": \n\t[(0, 3, 1), (3, 6, 3), (0.999, 1, 4), (6, 9, 2), (9, 242.17, 1)]\n
        Tool27": \n\t[(0, 18, 1), (18, 22, 2), (22, 25, 3), (25, 36, 4), (36, 50, 1)]\n
        Tool30": \n\t[(0, 18, 1), (18, 22, 2), (22, 25, 3), (25, 36, 4), (36, 50, 1)]\n

        :param input_raster: contains string for full path of input raster tif file.
        :param reclassify_list: contains a list of tuple, each tuple has 3 values(start, end, target).
        :param output_raster: contains string for full path of output raster tif file.
        """

        nan_value = -3.4028230607370965e+38  # 2**16 - 1
        nan_value = 10000

        t = {len(x) for x in reclassify_list}
        # print(t)
        if len(t) != 1:
            print("Tool must contains tuples of 3 values (start, end, target)")
            return -1
        elif len(t) == 1 and list(t)[0] != 3:
            print("All tuples of Tool must be 3 values (start, end, target)")
            return

        ds = gdal.Open(input_raster)
        band = ds.GetRasterBand(1)
        ndv = band.GetNoDataValue()
        if ndv == None:
            ndv = nan_value
        band_arr = band.ReadAsArray()

        for entry in reclassify_list:
            band_arr[np.where((entry[0] <= band_arr) & (band_arr <= entry[1]))] = entry[2]

        band_arr[np.where((ndv <= band_arr) & (band_arr <= ndv))] = nan_value

        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(output_raster, band_arr.shape[1], band_arr.shape[0], 1, gdal.GDT_UInt16)
        outdata.SetGeoTransform(ds.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr)
        outdata.GetRasterBand(1).SetNoDataValue(ndv)

        outdata.GetRasterBand(1).SetNoDataValue(nan_value)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None
        ds = None

    @staticmethod
    def get_cr(fullPath):
        cr_list = ['red', 'yellow', 'cyan', 'blue']
        img = Image.open(fullPath)
        img = np.array(img)
        data_pixels = img[img != 10000.0]

        data_mean = data_pixels.mean()
        data_min = data_pixels.min()
        data_max = data_pixels.max()
        print(f"mean: {data_mean}, min: {data_min}, max: {data_max}")
        img[img == 10000.0] = np.nan

        cmap = clr.LinearSegmentedColormap.from_list('custom', cr_list, N=256)

        plt.imsave(fullPath.replace('.tif', '.png'), img, cmap=cmap, vmin=data_min, vmax=data_max)

        gradient = np.linspace(0, 1, 256)
        for g in range(5):
            gradient = np.vstack((gradient, gradient))

        plt.imsave(fullPath.replace('.tif', '_legend.jpg'), gradient, cmap=cmap)

        return [data_min, data_max, data_mean]

    @staticmethod
    def clip_using_polygon(in_ras_list, out_dir, in_clipper, area_clipped_dir, area_clipped_name):
        """
        Clip model ouput raster using list of coordinates come from request.

        :param in_ras: Raster tif file.
        :param in_clipper: List of coordinates.
        :param area_clipped_dir: A fullpath for clipped area tif file.
        :param out_clipped_ras: A filename for clipped area - shp for boundary and tif for data.
        """
        print("area_clipped_name:\n", area_clipped_name)
        nan_value = 10000

        # set up the shapefile driver
        driver = ogr.GetDriverByName("ESRI Shapefile")

        # create the data source
        data_source = driver.CreateDataSource(area_clipped_dir)

        # create the spatial reference, WGS84
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

        # create the layer
        layer = data_source.CreateLayer(area_clipped_name, srs, ogr.wkbPolygon)

        ring = ogr.Geometry(ogr.wkbLinearRing)
        # add first point as last point where Points of LinearRing must form a closed linestring
        in_clipper.append(in_clipper[0])
        for lat, lon in in_clipper:
            ring.AddPoint(lon, lat)

        # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(poly)
        boundingBox = feature.GetGeometryRef().GetEnvelope()
        # Create the feature in the layer (shapefile)
        layer.CreateFeature(feature)
        # Dereference the feature
        feature = None

        # Save and close the data source
        data_source = None
        out_params = ""
        for i in in_ras_list:
            in_ras = os.path.join(out_dir, i)
            out_ras = "{}/{}_{}".format(area_clipped_dir, area_clipped_name, i)

            OutTile = gdal.Warp(out_ras,
                                in_ras, cutlineDSName="{}/{}.shp".format(area_clipped_dir, area_clipped_name),
                                cropToCutline=True, dstNodata=nan_value)
            OutTile = None
            cur_params = TSModel.get_cr(out_ras)
            out_params += i[:-4] + "," + ",".join([str(x) for x in cur_params]) + ","

        print("get_cr out_params: ", out_params)
        return out_params[:-1]


if __name__ == '__main__':
    img_path = "C:/Users/ahmed.kotb/PycharmProjects/GAFRD_Portal/gafrd_portal_app/static/model_results/FinalSuitabilityModel.tif"
    TSModel.get_cr(img_path)

