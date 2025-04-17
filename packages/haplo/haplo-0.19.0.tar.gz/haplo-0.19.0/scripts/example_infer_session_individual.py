from pathlib import Path

import numpy as np
import torch
from bokeh.io import show
from bokeh.plotting import figure

from haplo.export_onnx import WrappedModel
from haplo.models import Cura
from haplo.nicer_dataset import NicerDataset, split_dataset_into_count_datasets
from haplo.nicer_transform import PrecomputedNormalizeParameters, PrecomputedNormalizePhaseAmplitudes, \
    PrecomputedUnnormalizePhaseAmplitudes


def example_infer_session():
    model = Cura()
    model = WrappedModel(model)  # The DDP module requires an extra wrapping. This emulates that.
    saved_model_path = Path('/Users/golmschenk/Downloads/lowest_50m_validation_model.pt')
    model.load_state_dict(torch.load(str(saved_model_path), map_location=torch.device('cpu')))
    model.eval()
    normalize = PrecomputedNormalizeParameters()
    unnormalize = PrecomputedUnnormalizePhaseAmplitudes()
    parameters = np.array([7.557257540694740E-002, 0.123674255335847, -0.494945657705134,
                           2.16487304204509, 2.45025873920033, 0.338851445495323,
                           -0.126617284613881, -9.594016785496662E-002, 1.76792362926050,
                           5.41682185280249, 4.27309470936332], dtype=np.float32)
    normalized_parameters = normalize(parameters)
    input_array = np.expand_dims(normalized_parameters, axis=0)
    with torch.no_grad():
        input_tensor = torch.tensor(input_array)
        output_tensor = model(input_tensor)
        output_array = output_tensor.numpy()
    normalized_phase_amplitudes = np.squeeze(output_array, axis=0)
    phase_amplitudes = unnormalize(normalized_phase_amplitudes)
    print(phase_amplitudes)
    for phase_amplitude in phase_amplitudes:
        print(f'{phase_amplitude}, ', end='')
    pass


if __name__ == '__main__':
    example_infer_session()
