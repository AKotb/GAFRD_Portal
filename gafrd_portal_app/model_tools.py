from osgeo import ogr, osr
from osgeo import gdal
import numpy as np
from PIL import Image
import os


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

        # print(target_ds, [1], source_layer.name)

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
        print('inside is null: ndv = ', ndv)
        if ndv is None:
            ndv = 10000
            # print('\tinside is null: ndv becomes 10000')
        # else:
        # print('NDV is equals: ', ndv)
        band_arr = band.ReadAsArray()
        # print('inside is null: \n\tinput unique values = ', np.unique(band_arr))
        # band_arr[band_arr == ndv] = 1.0
        # band_arr[band_arr != ndv] = 0.0
        band_arr = 0.0001 * band_arr

        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(out_raster, band_arr.shape[1], band_arr.shape[0], 1, gdal.GDT_UInt16)
        outdata.SetGeoTransform(ds.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr)
        outdata.GetRasterBand(1).SetNoDataValue(ndv)  ##if you want these values transparent
        # print('inside is null: \n\toutput unique values = ', np.unique(band_arr))
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
        # cols, rows = temp.RasterXSize, temp.RasterYSize
        # print('inside clip: out clipped: \n{} \ndims: cols = {}, rows = {}'.format(out_clipped_ras, cols, rows))

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
        # print('inside rasCalcMul: \n\t NDV1 = ', ndv1)
        band_arr1 = band1.ReadAsArray()
        b1 = np.where(band_arr1 == 10000.0)
        band_arr1[band_arr1 == ndv1] = nan_value
        transform = ds1.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols1 = ds1.RasterXSize
        rows1 = ds1.RasterYSize
        '''print('{}\ntransform: {}\n\tpixel width: {}, pixel height: {}\n\tcols: {}, rows: {}'.format(input_list[0],
                                                                                                    transform,
                                                                                                    pixelWidth,
                                                                                                    pixelHeight, cols1,
                                                                                                    rows1))'''

        input2 = input_list[1]
        ds2 = gdal.Open(input2)
        band2 = ds2.GetRasterBand(1)
        ndv2 = band2.GetNoDataValue()
        # print('inside rasCalcMul: \n\t NDV2 = ', ndv2)
        band_arr2 = band2.ReadAsArray()
        b2 = np.where(band_arr2 == 10000.0)
        band_arr2[band_arr2 == ndv2] = nan_value
        transform = ds2.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols2 = ds2.RasterXSize
        rows2 = ds2.RasterYSize
        '''print('{}\ntransform: {}\n\tpixel width: {}, pixel height: {}\n\tcols: {}, rows: {}'.format(input_list[1],
                                                                                                    transform,
                                                                                                    pixelWidth,
                                                                                                    pixelHeight, cols2,
                                                                                                    rows2))'''

        if nParams == 2:
            min_cols = min([cols1, cols2])
            min_rows = min([rows1, rows2])

            band_arr1 = band_arr1[:min_rows, :min_cols]
            band_arr2 = band_arr2[:min_rows, :min_cols]
            b1 = np.where(band_arr1 == 10000.0)
            b2 = np.where(band_arr2 == 10000.0)
            band_arr_all = 1.0 * band_arr1 * band_arr2
            # band_arr_all = 0.5 * (band_arr1 + band_arr2)

            # print('Again ... ', np.unique(band_arr_all))

            # print('inside raster_calc_mul: \n\tdims of calculated matrix: \n\t', band_arr_all.shape)
            band_arr_all[b1] = nan_value
            band_arr_all[b2] = nan_value

            driver = gdal.GetDriverByName("GTiff")
            outdata = driver.Create(output_raster, band_arr1.shape[1], band_arr1.shape[0], 1, gdal.GDT_Float32)

        else:
            input3 = input_list[2]
            ds3 = gdal.Open(input3)
            band3 = ds3.GetRasterBand(1)
            ndv3 = band3.GetNoDataValue()
            # print('inside rasCalcMul: \n\t NDV3 = ', ndv3)
            band_arr3 = band3.ReadAsArray()
            band_arr3[band_arr3 == ndv3] = nan_value
            cols3 = ds3.RasterXSize
            rows3 = ds3.RasterYSize

            input4 = input_list[3]
            ds4 = gdal.Open(input4)
            band4 = ds4.GetRasterBand(1)
            ndv4 = band4.GetNoDataValue()
            # print('inside rasCalcMul: \n\t NDV4 = ', ndv4)
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
            # band_arr_all = 1.0 * band_arr1 * band_arr2 * band_arr3 * band_arr4
            band_arr_all = 0.25 * (band_arr1 + band_arr2 + band_arr3 + band_arr4)
            # print(np.unique(band_arr_all))
            band_arr_all[np.where(band_arr_all < 1.0)] = 0
            band_arr_all[np.where(band_arr_all == 1.0)] = 1
            band_arr_all[np.where(band_arr_all > 1.0)] = 10000
            # print('Again ... ', np.unique(band_arr_all))

            # print('inside raster_calc_mul: \n\tdims of calculated matrix: \n\t', band_arr_all.shape)
            band_arr_all[band_arr_all == nan_value] = ndv1
            driver = gdal.GetDriverByName("GTiff")
            outdata = driver.Create(output_raster, band_arr1.shape[1], band_arr1.shape[0], 1, gdal.GDT_UInt16)

        outdata.SetGeoTransform(ds1.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds1.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr_all)

        outdata.GetRasterBand(1).SetNoDataValue(ndv1)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None
        # print(output_raster)
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
        # print('band 1: ', np.unique(band_arr1))
        b1 = np.where(band_arr1 == 10000.0)
        # print(b1)
        # band_arr1[band_arr1 == ndv1] = nan_value
        transform = ds1.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols1 = ds1.RasterXSize
        rows1 = ds1.RasterYSize
        '''print('{}\ntransform 1: {}\n\tpixel width 1: {}, pixel height 1: {}\n\tcols 1: {}, rows 1: {}'.format(
            input_list[0], transform, pixelWidth,
            pixelHeight, cols1, rows1))'''

        input2 = input_list[1]
        weight2 = weight_list[1]
        ds2 = gdal.Open(input2)
        band2 = ds2.GetRasterBand(1)
        ndv2 = band2.GetNoDataValue()
        band_arr2 = band2.ReadAsArray()
        # print('band 2: ', np.unique(band_arr2))
        b2 = np.where(band_arr2 == 10000.0)
        # print(b2)
        # band_arr2[band_arr2 == ndv2] = nan_value
        transform = ds2.GetGeoTransform()
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        cols2 = ds2.RasterXSize
        rows2 = ds2.RasterYSize
        '''print('{}\ntransform 2: {}\n\tpixel width 2: {}, pixel height 2: {}\n\tcols 2: {}, rows 2: {}'.format(
            input_list[1], transform, pixelWidth,
            pixelHeight, cols2, rows2))'''

        if nParams == 2:
            min_cols = min([cols1, cols2])
            min_rows = min([rows1, rows2])

            band_arr1 = band_arr1[:min_rows, :min_cols]
            band_arr2 = band_arr2[:min_rows, :min_cols]

            band_arr_all = (weight1 * band_arr1) + (weight2 * band_arr2)
            # print("Unique Values inside rasCalcAdd: ", np.unique(band_arr_all))
            band_arr_all[b1] = 10000
            band_arr_all[b2] = 10000
            # print("Again: Unique Values inside rasCalcAdd: ", np.unique(band_arr_all))
            # band_arr_all[band_arr_all == nan_value] = ndv1
        else:
            input3 = input_list[2]
            weight3 = weight_list[2]
            ds3 = gdal.Open(input3)
            band3 = ds3.GetRasterBand(1)
            ndv3 = band3.GetNoDataValue()
            band_arr3 = band3.ReadAsArray()
            # print('band 3: ', np.unique(band_arr3))
            b3 = np.where(band_arr3 == 10000.0)
            # print(b3)
            # band_arr3[band_arr3 == ndv3] = nan_value

            input4 = input_list[3]
            weight4 = weight_list[3]
            ds4 = gdal.Open(input4)
            band4 = ds4.GetRasterBand(1)
            ndv4 = band4.GetNoDataValue()
            band_arr4 = band4.ReadAsArray()
            # print('band 4: ', np.unique(band_arr4))
            b4 = np.where(band_arr4 == 10000.0)
            # print(b4)
            # band_arr4[band_arr4 == ndv4] = nan_value

            band_arr_all = (weight1 * band_arr1) + (weight2 * band_arr2) + (weight3 * band_arr3) + (weight4 * band_arr4)
            # print("Unique Values inside rasCalcAdd: ", np.unique(band_arr_all))
            band_arr_all[b1] = 10000
            band_arr_all[b2] = 10000
            band_arr_all[b3] = 10000
            band_arr_all[b4] = 10000
            # print("Again: Unique Values inside rasCalcAdd: ", np.unique(band_arr_all))
            # band_arr_all[band_arr_all == nan_value] = ndv1

        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(output_raster, band_arr1.shape[1], band_arr1.shape[0], 1, gdal.GDT_Float32)
        outdata.SetGeoTransform(ds1.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds1.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr_all)

        outdata.GetRasterBand(1).SetNoDataValue(nan_value)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None
        # print(output_raster)
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

        # print('Good Tool ...')

        ds = gdal.Open(input_raster)
        band = ds.GetRasterBand(1)
        ndv = band.GetNoDataValue()
        # print('ndv: ', ndv)
        if ndv == None:
            # print('There is no data value')
            ndv = nan_value
        band_arr = band.ReadAsArray()

        # print('Starting reclassify pixels ...')
        for entry in reclassify_list:
            band_arr[np.where((entry[0] <= band_arr) & (band_arr <= entry[1]))] = entry[2]

        band_arr[np.where((ndv <= band_arr) & (band_arr <= ndv))] = nan_value

        # print('End of reclassify.')

        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(output_raster, band_arr.shape[1], band_arr.shape[0], 1, gdal.GDT_UInt16)
        outdata.SetGeoTransform(ds.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(ds.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(band_arr)
        outdata.GetRasterBand(1).SetNoDataValue(ndv)

        outdata.GetRasterBand(1).SetNoDataValue(nan_value)  ##if you want these values transparent
        outdata.FlushCache()  ##saves to disk!!
        outdata = None
        # print(output_raster)
        ds = None

    @staticmethod
    def clip_using_polygon(in_ras, in_clipper, area_clipped_dir, area_clipped_name):
        """
        Clip model ouput raster using list of coordinates come from request.

        :param in_ras: Raster tif file.
        :param in_clipper: List of coordinates.
        :param area_clipped_dir: A fullpath for clipped area tif file.
        :param out_clipped_ras: A filename for clipped area - shp for boundary and tif for data.
        """

        nan_value = -3.4028230607370965e+38  # 2**16 - 1
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

        OutTile = gdal.Warp("{}/{}.tif".format(area_clipped_dir, area_clipped_name),
                            in_ras, cutlineDSName="{}/{}.shp".format(area_clipped_dir, area_clipped_name),
                            cropToCutline=True, dstNodata=nan_value)
        OutTile = None

        temp = gdal.Open("{}/{}.tif".format(area_clipped_dir, area_clipped_name))
        cols, rows = temp.RasterXSize, temp.RasterYSize
        print('inside clip: out clipped: \n{} \ndims: cols = {}, rows = {}'.format(area_clipped_name, cols, rows))
        band = temp.GetRasterBand(1)
        bmin, bmax = band.ComputeRasterMinMax(1)
        print(bmin, bmax)
        band_arr = band.ReadAsArray()
        print(nan_value)
        print(band_arr.shape)
        print(np.min(band_arr), np.max(band_arr))
        # scale ascending
        scaled = 255 * (band_arr - bmin) / (bmax - bmin)
        #print(np.min(scaled), np.max(scaled))
        scaled[np.where(scaled > 255)] = 255
        scaled[np.where(scaled < 0)] = 0
        scaled = scaled.astype(int)
        #print(np.min(scaled), np.max(scaled))
        scaled2 = 255 - scaled
        #print(np.min(scaled2), np.max(scaled2))
        #print(scaled[25, 57], scaled2[25, 57])
        scaled3 = 0 * scaled
        scaled4 = 255 + scaled3
        scaled4[np.where(band_arr == nan_value)] = 0
        img = scaled

        img = np.zeros((scaled.shape[0], scaled.shape[1], 4), dtype=np.uint8)
        img[:, :, 0] = scaled
        img[:, :, 1] = scaled2
        img[:, :, 2] = scaled3
        img[:, :, 3] = scaled4
        print(scaled2.shape, img.shape)
        imgFile = Image.fromarray(img)
        imgFile.save("{}/{}.png".format(area_clipped_dir, area_clipped_name))

        imgLeg = np.zeros([100, 257 - 1, 3], dtype=np.uint8)
        for n in range(257 - 1):
            imgLeg[:, n] = [255 - n, n, 0]
        imgLegFile = Image.fromarray(imgLeg)
        imgLegFile.save("{}/{}-legend.jpg".format(area_clipped_dir, area_clipped_name))

        txtInfo = open("{}/{}-info.txt".format(area_clipped_dir, area_clipped_name), "w+")
        txtInfo.write("name:{}\n".format(area_clipped_name))
        txtInfo.write("minValue:{}\n".format(bmin))
        txtInfo.write("maxValue:{}\n".format(bmax))
        txtInfo.write("bottom:{}\n".format(boundingBox[0]))
        txtInfo.write("top:{}\n".format(boundingBox[1]))
        txtInfo.write("left:{}\n".format(boundingBox[2]))
        txtInfo.write("right:{}\n".format(boundingBox[3]))




