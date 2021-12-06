import os
from gafrd_portal_app import model_tools as mt


data_inputs_path = r'D:\NARSS\GAFRD_Portal\Model\Ahmed_Kotb\Ahmed_Kotb\Data'
data_outputs_path = r'D:\NARSS\GAFRD_Portal\Model\Ahmed_Kotb\Ahmed_Kotb\Data\output'

# Define all main inputs to tools as Inputs (In), where n from 1 to 16
data_inputs = {
    "I1": "clip_Temprature.tif",
    "I2": "clip_DistanceToWaterBody.tif",
    "I3": "clip_PerennialRiverDensity.tif",
    "I4": "clip_DistanceToRiver.tif",
    "I5": "clip_rainfallAnn.tif",
    "I6": "clip_RoadDensity.tif",
    "I7": "clip_DistanceToRoad.tif",
    "I8": "clip_SOM.tif",
    "I9": "clip_claypercent.tif",
    "I10": "clip_soilpH.tif",
    "I11": "clip_Slope.tif",
    "I12": "RoadsBuffer.shp",
    "I13": "WaterBodies.shp",
    "I14": "protectedareas.shp",
    "I15": "Perennialrivers5mBuffer.shp",
    "I16": "LimpopoBoundary.shp",
}

for k in data_inputs.keys():
    data_inputs[k] = os.path.join(data_inputs_path, data_inputs[k])

# Define all outputs from tools as Tool Output (TOn), where n from 1 to 30
data_outputs = {
    "TO1": "RoadsBufferRaster.tif",
    "TO2": "RoadsBufferRasterIsNull.tif",
    "TO3": "RoadsBufferRestriction.tif",
    "TO4": "WaterBodiesRaster.tif",
    "TO5": "WaterBodiesRasterIsNull.tif",
    "TO6": "WaterBodiesRestriction.tif",
    "TO7": "protectedareasRaster.tif",
    "TO8": "protectedareasRasterIsNull.tif",
    "TO9": "protectedareasRestriction.tif",
    "TO10": "Perennialrivers5mBufferRaster.tif",
    "TO11": "Perennialrivers5mBufferRasterIsNull.tif",
    "TO12": "Perennialrivers5mBufferRestriction.tif",
    "TO13": "FinalRestrictionModel.tif",
    "TO14": "DistanceToWaterBodyReclassify.tif",
    "TO15": "PerennialRiverDensityReclassify.tif",
    "TO16": "DistanceToRiverReclassify.tif",
    "TO17": "rainfallAnnReclassify.tif",
    "TO18": "WaterAvailabilitySubModel.tif",
    "TO19": "RoadDensityReclassify.tif",
    "TO20": "DistanceToRoadReclassify.tif",
    "TO21": "SocioEconomic.tif",
    "TO22": "SOMReclassify.tif",
    "TO23": "claypercentReclassify.tif",
    "TO24": "soilpHReclassify.tif",
    "TO25": "SlopeReclassify.tif",
    "TO26": "SoilSubModel.tif",
    "TO27": "TempratureReclassify.tif",
    "TO28": "FinalSuitabilityModel.tif",
    "TO29": "FinalSuitabilityMapModel.tif",
    "TO30": "FinalSuitabilityMapModelReclassify.tif"
}

for k in data_outputs.keys():
    data_outputs[k] = os.path.join(data_outputs_path, data_outputs[k])

# Define all reclassify lists used in tools as Rn,
# where n in [14, 15, 16, 17, 19, 20, 22, 23, 24, 25, 27, 30]
reclassify_list = {
    "R14": [(0, 1000, 4), (1000, 2500, 3), (2500, 3500, 2), (3500, 100000, 1)],
    "R15": [(0, 0.02, 1), (0.02, 0.2, 2), (0.2, 0.35, 3), (0.35, 1, 4)],
    "R16": [(0, 20, 1), (20, 1000, 4), (1000, 2500, 3), (2500, 3500, 2), (3500, 100000, 1)],
    "R17": [(0, 200, 1), (200, 300, 1), (300, 700, 2), (700, 1000, 3), (1000, 3000, 4)],
    "R19": [(0, 0.04, 1), (0.04, 0.2, 2), (0.2, 0.35, 3), (0.35, 1, 4)],
    "R20": [(0, 5000, 4), (5000, 10000, 3), (10000, 15000, 2), (15000, 100000, 1)],
    "R22": [(0, 1, 1), (1, 1.5, 2), (1.5, 2.5, 4), (2.5, 18, 3), (18, 100, 1)],
    "R23": [(0, 20, 1), (20, 40, 2), (40, 60, 3), (60, 100, 4)],
    "R24": [(1, 4, 1), (4, 5.5, 2), (5.5, 6.5, 3), (6.5, 8.5, 4)],
    "R25": [(0, 3, 1), (3, 6, 3), (0.999, 1, 4), (6, 9, 2), (9, 242.17, 1)],
    "R27": [(0, 18, 1), (18, 22, 2), (22, 25, 3), (25, 36, 4), (36, 50, 1)],
    "R30": [(0, 18, 1), (18, 22, 2), (22, 25, 3), (25, 36, 4), (36, 50, 1)]
}

# Define all weight lists used in tools of additive raster calculator as Wn, where n in [18, 21, 26, 28]
weight_list = {
    "W18": (0.09, 0.455, 0.273, 0.182),
    "W21": (0.143, 0.238),
    "W26": (0.15, 0.503, 0.096, 0.251),
    "W28": (0.391, 0.087, 0.262, 0.217)
}

print("Run Tools 1, 2, & 3")
mt.vector_to_raster(data_inputs["I12"], data_outputs["TO1"])
mt.is_null(data_outputs["TO1"], data_outputs["TO2"])
mt.clip_raster(data_outputs["TO2"], data_inputs["I16"], data_outputs["TO3"])

print("Run Tools 4, 5, & 6")
mt.vector_to_raster(data_inputs["I13"], data_outputs["TO4"])
mt.is_null(data_outputs["TO4"], data_outputs["TO5"])
mt.clip_raster(data_outputs["TO5"], data_inputs["I16"], data_outputs["TO6"])

print("Run Tools 7, 8, & 9")
mt.vector_to_raster(data_inputs["I14"], data_outputs["TO7"])
mt.is_null(data_outputs["TO7"], data_outputs["TO8"])
mt.clip_raster(data_outputs["TO8"], data_inputs["I16"], data_outputs["TO9"])

print("Run Tools 10, 11, & 12")
mt.vector_to_raster(data_inputs["I15"], data_outputs["TO10"])
mt.is_null(data_outputs["TO10"], data_outputs["TO11"])
mt.clip_raster(data_outputs["TO11"], data_inputs["I16"], data_outputs["TO12"])

print("Run Tool 13")
mt.raster_calc_mul([data_outputs["TO3"], data_outputs["TO6"], data_outputs["TO9"], data_outputs["TO12"]],
                   data_outputs["TO13"])

print("Run Tools 14, 15, 16, & 17")
mt.raster_reclassify(data_inputs["I2"], reclassify_list["R14"], data_outputs["TO14"])
mt.raster_reclassify(data_inputs["I3"], reclassify_list["R15"], data_outputs["TO15"])
mt.raster_reclassify(data_inputs["I4"], reclassify_list["R16"], data_outputs["TO16"])
mt.raster_reclassify(data_inputs["I5"], reclassify_list["R17"], data_outputs["TO17"])

print("Run Tool 18")
mt.raster_calc_add([data_outputs["TO14"], data_outputs["TO15"], data_outputs["TO16"], data_outputs["TO17"]],
                   weight_list["W18"],
                   data_outputs["TO18"])

print("Run Tools 19 & 20")
mt.raster_reclassify(data_inputs["I6"], reclassify_list["R19"], data_outputs["TO19"])
mt.raster_reclassify(data_inputs["I7"], reclassify_list["R20"], data_outputs["TO20"])

print("Run Tool 21")
mt.raster_calc_add([data_outputs["TO19"], data_outputs["TO20"]],
                   weight_list["W21"],
                   data_outputs["TO21"])

print("Run Tools 22, 23, 24, & 25")
mt.raster_reclassify(data_inputs["I8"], reclassify_list["R22"], data_outputs["TO22"])
mt.raster_reclassify(data_inputs["I9"], reclassify_list["R23"], data_outputs["TO23"])
mt.raster_reclassify(data_inputs["I10"], reclassify_list["R24"], data_outputs["TO24"])
mt.raster_reclassify(data_inputs["I11"], reclassify_list["R25"], data_outputs["TO25"])

print("Run Tool 26")
mt.raster_calc_add([data_outputs["TO22"], data_outputs["TO23"], data_outputs["TO24"], data_outputs["TO25"]],
                   weight_list["W26"],
                   data_outputs["TO26"])

print("Run Tool 27")
mt.raster_reclassify(data_inputs["I1"], reclassify_list["R27"], data_outputs["TO27"])

print("Run Tool 28")
mt.raster_calc_add([data_outputs["TO18"], data_outputs["TO21"], data_outputs["TO26"], data_outputs["TO27"]],
                   weight_list["W28"],
                   data_outputs["TO28"])

print("Run Tool 29")
mt.raster_calc_mul([data_outputs["TO13"], data_outputs["TO28"]],
                   data_outputs["TO29"])

print("Run Tool 30")
mt.raster_reclassify(data_outputs["TO29"], reclassify_list["R30"], data_outputs["TO30"])

print("Model Run is finished.")

