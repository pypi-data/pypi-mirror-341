import numpy as np
from pathlib import Path

from haplo.nicer_dataset import NicerDataset, split_dataset_into_count_datasets
from haplo.nicer_transform import PrecomputedNormalizeParameters, PrecomputedNormalizePhaseAmplitudes


def example_infer_session():
    print('0')
    full_dataset_path = Path('data/640m_parameters_and_phase_amplitudes.db')
    full_train_dataset = NicerDataset.new(
        dataset_path=full_dataset_path,
        # parameters_transform=PrecomputedNormalizeParameters(),
        # phase_amplitudes_transform=PrecomputedNormalizePhaseAmplitudes(),
        length=200_000,
    )
    test_dataset, validation_dataset, train_dataset, _ = split_dataset_into_count_datasets(
        full_train_dataset, [100_000, 10, 10])
    print('1')

    parameters_list = []
    test_phase_amplitudes_list = []
    for test_parameters, test_phase_amplitudes in test_dataset:
        parameters_list.append(test_parameters)
        test_phase_amplitudes_list.append(test_phase_amplitudes)
        if len(parameters_list) % 1000 == 0:
            print(len(parameters_list))
    parameters_array = np.stack(parameters_list, axis=0, dtype=np.float32)
    phase_amplitudes_array = np.stack(test_phase_amplitudes_list, axis=0, dtype=np.float32)
    np.save(Path('test_parameters.npy'), parameters_array)
    np.save(Path('test_phase_amplitudes.npy'), phase_amplitudes_array)

if __name__ == '__main__':
    example_infer_session()
