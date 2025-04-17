import math
import os
from pathlib import Path

import torch
from haplo.data_paths import move_to_tmp_on_pbs
from haplo.distributed import distributed_logging
from haplo.unwrap_model import unwrap_model
from torch.optim import AdamW
from datetime import timedelta
from haplo.losses import PlusOneBeforeUnnormalizationChiSquaredStatisticMetric, \
    PlusOneChiSquaredStatisticMetric, SumDifferenceSquaredOverMedianExpectedSquaredMetric
from haplo.models import Cura
from haplo.nicer_dataset import NicerDataset, split_dataset_into_count_datasets
from haplo.train_hyperparameter_configuration import TrainHyperparameterConfiguration
from haplo.train_logging_configuration import TrainLoggingConfiguration
from haplo.train_system_configuration import TrainSystemConfiguration
from haplo.train_session import train_session
from haplo.nicer_transform import PrecomputedNormalizeParameters, PrecomputedNormalizePhaseAmplitudes
from haplo.pbs_helper import schedule_self_process_interrupt_signal_before_pbs_end_time
from haplo.train_session import load_latest_state
from torch.distributed import Backend


@distributed_logging
def example_train_session():
    full_dataset_path = Path('data/640m_parameters_and_phase_amplitudes.db')
    full_train_dataset = NicerDataset.new(
        dataset_path=full_dataset_path,
        length=600_000_000,
        parameters_transform=PrecomputedNormalizeParameters(),
        phase_amplitudes_transform=PrecomputedNormalizePhaseAmplitudes(),
        in_memory= True
    )
    test_dataset, validation_dataset, train_dataset, _ = split_dataset_into_count_datasets(
        full_train_dataset, [100_000, 100_000, 500_000])
    model = Cura()

    loss_function = SumDifferenceSquaredOverMedianExpectedSquaredMetric()
    metric_functions = [PlusOneChiSquaredStatisticMetric(), PlusOneBeforeUnnormalizationChiSquaredStatisticMetric(),SumDifferenceSquaredOverMedianExpectedSquaredMetric()]
    hyperparameter_configuration = TrainHyperparameterConfiguration.new(batch_size=1_000, learning_rate=.001)
    system_configuration = TrainSystemConfiguration.new(preprocessing_processes_per_train_process=8,distributed_back_end=Backend.NCCL)
    optimizer = AdamW(params=model.parameters(), lr=hyperparameter_configuration.learning_rate,
                      weight_decay=hyperparameter_configuration.weight_decay,
                      eps=hyperparameter_configuration.optimizer_epsilon)

    #load_latest_state(model=model, optimizer=optimizer, session_directory=Path('sessions/2024_02_20_08_34_17_50m_continue_diff_loss_multinode_in_mem_2pp_retry'))

    run_comments = (f'nccl_test')  # Whatever you want to log in a string.
    additional_log_dictionary = {
        'model_name': type(model).__name__, 'train_dataset_size': len(train_dataset), 'run_comments': run_comments,
        'pbs_job_id': os.environ['PBS_JOBID']
    }
    schedule_self_process_interrupt_signal_before_pbs_end_time(timedelta(minutes=2))
    logging_configuration = TrainLoggingConfiguration.new(
        wandb_project='multinode_runs', wandb_entity='ramjet', additional_log_dictionary=additional_log_dictionary,
        model_save_cycle_frequency=math.ceil(500_000_000 / len(train_dataset))
    )
    train_session(train_dataset=train_dataset, validation_dataset=validation_dataset, model=model,
                  loss_function=loss_function, metric_functions=metric_functions, optimizer=optimizer,
                  hyperparameter_configuration=hyperparameter_configuration, system_configuration=system_configuration,
                  logging_configuration=logging_configuration)


if __name__ == '__main__':
    example_train_session()
