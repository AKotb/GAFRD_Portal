import os

from gafrd_portal_app.model_tools import TSModel


class ExecuteModel:

    @staticmethod
    def run(data_inputs_path, data_outputs_path):

        # Define all main inputs to tools as Inputs (In), where n from 1 to 16
        # --------------------------------------------------------------------
        model_info_files = {
            "data_inputs": "data_inputs.csv",
            "data_outputs": "data_outputs.csv",
            "reclassify_list": "reclassify_list.csv",
            "weight_list": "weight_list.csv",
        }
        for k in model_info_files.keys():
            model_info_files[k] = os.path.join(data_inputs_path, "model_info_files", model_info_files[k])

        # Define all main inputs to tools as Inputs (In), where n from 1 to 16
        data_inputs = {}

        f = open(model_info_files["data_inputs"], "r")
        for line in f.readlines()[1:]:
            lineSplit = line.rstrip("\n").split(",")
            data_inputs["I{}".format(lineSplit[0])] = "{}\\{}.{}".format(data_inputs_path, lineSplit[1], lineSplit[2])
        f.close()

        # Define all outputs from tools as Tool Output (TOn), where n from 1 to 30
        data_outputs = {}

        f = open(model_info_files["data_outputs"], "r")
        for line in f.readlines()[1:]:
            lineSplit = line.rstrip("\n").split(",")
            data_outputs["TO{}".format(lineSplit[0])] = "{}\\{}.{}".format(data_outputs_path, lineSplit[1],
                                                                           lineSplit[2])

        # Define all reclassify lists used in tools as Rn,
        # where n in [14, 15, 16, 17, 19, 20, 22, 23, 24, 25, 27, 30]
        reclassify_list = {}

        f = open(model_info_files["reclassify_list"], "r")
        for line in f.readlines()[1:]:
            lineSplit = line.rstrip("\n").rstrip(",").split(",")
            entries = int((len(lineSplit) - 1) / 3)
            reclassify_list["R{}".format(lineSplit[0])] = [
                [float(lineSplit[3 * x + 1]), float(lineSplit[3 * x + 2]), float(lineSplit[3 * x + 3])]
                for x in range(entries)]

        # Define all weight lists used in tools of additive raster calculator as Wn, where n in [18, 21, 26, 28]
        weight_list = {}

        f = open(model_info_files["weight_list"], "r")
        for line in f.readlines()[1:]:
            lineSplit = line.rstrip("\n").rstrip(",").split(",")
            weight_list["W{}".format(lineSplit[0])] = [float(x) for x in lineSplit[1:] if len(x.strip(" ")) > 0]
        # --------------------------------------------------------------------

        print("Run Tools 1, 2, & 3")
        TSModel.vector_to_raster(data_inputs["I12"], data_outputs["TO1"])
        TSModel.is_null(data_outputs["TO1"], data_outputs["TO2"])
        TSModel.clip_raster(data_outputs["TO2"], data_inputs["I16"], data_outputs["TO3"])

        print("Run Tools 4, 5, & 6")
        TSModel.vector_to_raster(data_inputs["I13"], data_outputs["TO4"])
        TSModel.is_null(data_outputs["TO4"], data_outputs["TO5"])
        TSModel.clip_raster(data_outputs["TO5"], data_inputs["I16"], data_outputs["TO6"])

        print("Run Tools 7, 8, & 9")
        TSModel.vector_to_raster(data_inputs["I14"], data_outputs["TO7"])
        TSModel.is_null(data_outputs["TO7"], data_outputs["TO8"])
        TSModel.clip_raster(data_outputs["TO8"], data_inputs["I16"], data_outputs["TO9"])

        print("Run Tools 10, 11, & 12")
        TSModel.vector_to_raster(data_inputs["I15"], data_outputs["TO10"])
        TSModel.is_null(data_outputs["TO10"], data_outputs["TO11"])
        TSModel.clip_raster(data_outputs["TO11"], data_inputs["I16"], data_outputs["TO12"])

        print("Run Tool 13")
        TSModel.raster_calc_mul(
            [data_outputs["TO3"], data_outputs["TO6"], data_outputs["TO9"], data_outputs["TO12"]],
            data_outputs["TO13"])

        print("Run Tools 14, 15, 16, & 17")
        TSModel.raster_reclassify(data_inputs["I2"], reclassify_list["R14"], data_outputs["TO14"])
        TSModel.raster_reclassify(data_inputs["I3"], reclassify_list["R15"], data_outputs["TO15"])
        TSModel.raster_reclassify(data_inputs["I4"], reclassify_list["R16"], data_outputs["TO16"])
        TSModel.raster_reclassify(data_inputs["I5"], reclassify_list["R17"], data_outputs["TO17"])

        print("Run Tool 18")
        TSModel.raster_calc_add(
            [data_outputs["TO14"], data_outputs["TO15"], data_outputs["TO16"], data_outputs["TO17"]],
            weight_list["W18"],
            data_outputs["TO18"])

        print("Run Tools 19 & 20")
        TSModel.raster_reclassify(data_inputs["I6"], reclassify_list["R19"], data_outputs["TO19"])
        TSModel.raster_reclassify(data_inputs["I7"], reclassify_list["R20"], data_outputs["TO20"])

        print("Run Tool 21")
        TSModel.raster_calc_add([data_outputs["TO19"], data_outputs["TO20"]],
                                weight_list["W21"],
                                data_outputs["TO21"])

        print("Run Tools 22, 23, 24, & 25")
        TSModel.raster_reclassify(data_inputs["I8"], reclassify_list["R22"], data_outputs["TO22"])
        TSModel.raster_reclassify(data_inputs["I9"], reclassify_list["R23"], data_outputs["TO23"])
        TSModel.raster_reclassify(data_inputs["I10"], reclassify_list["R24"], data_outputs["TO24"])
        TSModel.raster_reclassify(data_inputs["I11"], reclassify_list["R25"], data_outputs["TO25"])

        print("Run Tool 26")
        TSModel.raster_calc_add(
            [data_outputs["TO22"], data_outputs["TO23"], data_outputs["TO24"], data_outputs["TO25"]],
            weight_list["W26"],
            data_outputs["TO26"])

        print("Run Tool 27")
        TSModel.raster_reclassify(data_inputs["I1"], reclassify_list["R27"], data_outputs["TO27"])

        print("Run Tool 28")
        TSModel.raster_calc_add(
            [data_outputs["TO18"], data_outputs["TO21"], data_outputs["TO26"], data_outputs["TO27"]],
            weight_list["W28"],
            data_outputs["TO28"])

        print("Run Tool 29")
        TSModel.raster_calc_mul([data_outputs["TO13"], data_outputs["TO28"]],
                                data_outputs["TO29"])

        print("Run Tool 30")
        TSModel.raster_reclassify(data_outputs["TO29"], reclassify_list["R30"], data_outputs["TO30"])

        print("Model Run is finished.")
