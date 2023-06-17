import numpy as np

from model.PostProc.CA_CFAR_1D import ca_cfar_1d
from model.PostProc.FFT_3D import angle_of_arrival_2d


def detected_object(
        chirp: list,
        frame: list,
        guard_cell: int,
        training_cell: int,
        p_fa: float,
        data_type: bool,
        tx: int,
        rx: int,
        freq_slope: float,
        sample_rate: int,
        adc_sample_rate: int
):

    cfar = ca_cfar_1d(
        chirp=chirp,
        guard_cell=guard_cell,
        training_cell=training_cell,
        p_fa=p_fa,
        adc_sample_rate=adc_sample_rate,
        freq_slope=freq_slope,
        sample_rate=sample_rate,
        data_type=data_type
    )

    angles = angle_of_arrival_2d(
        tx=tx,
        rx=rx,
        frame=frame,
        freq_slope=freq_slope,
        sample_rate=sample_rate,
        adc_sample_rate=adc_sample_rate,
        data_type=data_type
    )

    success_obj = {}
    res = []
    detected_obj = []
    if len(cfar[3]) > 0:
        for element in cfar[3]:
            degrees = angles[0][len(angles[0]) - element[2] - 1]
            if element[2] not in success_obj:
                angle = max(degrees)
                ind = np.unravel_index(np.argmax(degrees, axis=None), degrees.shape)[0]
                success_obj[element[2]] = [[element[0], angle, ind]]

            else:
                for obj in success_obj[element[2]]:
                    degrees = np.delete(degrees, obj[2])

                angle = max(degrees)
                ind = np.unravel_index(np.argmax(degrees, axis=None), degrees.shape)[0]
                success_obj[element[2]] = [[element[0], angle, ind]]

            detected_obj = []
            for key, value in success_obj.items():
                half_deg = round(len(angles[0][0]) / 2)

                for elem in value:
                    pos = elem[2] - half_deg
                    if pos <= 0:
                        angle = (abs(pos) + 1) * angles[5]
                        detected_obj.append([elem[0], angle])
                    else:
                        angle = -pos * angles[5]
                        detected_obj.append([elem[0], angle])

        for elem in detected_obj:
            a = elem[0] * np.sin(np.deg2rad(elem[1]))
            b = elem[0] * np.cos(np.deg2rad(elem[1]))
            res.append([a, b])

        return [detected_obj, res]
