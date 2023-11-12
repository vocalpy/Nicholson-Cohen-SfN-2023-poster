#!/usr/bin/env python
# coding: utf-8
"""Script that generates summary data for loss function experiments"""
from dataclasses import dataclass
import pathlib

import pandas as pd


RESULTS_ROOT = pathlib.Path('results/multiclass/BFSongRepo/')


@dataclass
class ModelMetadata:
    """Class that represents a trained model + metadata"""
    results_dir: str
    window_size: int
    loss: str


MODEL_METADATA_MAP = {
    'TweetyNet': {
        'all-birds': [
            ModelMetadata(
                results_dir='results_231025_222720',
                window_size=2000,
                loss='CE',
            ),
            ModelMetadata(
                results_dir='results_231028_080948',
                window_size=2000,
                loss='CE+TMSE',
            ),
            ModelMetadata(
                results_dir='results_231028_124122',
                window_size=2000,
                loss='CE+gsTMSE',
            ),
        ],
    },
    'ConvTemporalConvNet': {
        'all-birds': [
            ModelMetadata(
                results_dir='results_231025_222812',
                window_size=2000,
                loss='CE'
            ),
            ModelMetadata(
                results_dir='results_231027_162429',
                window_size=2000,
                loss='CE+TMSE',
            ),
            ModelMetadata(
                results_dir='results_231027_162459',
                window_size=2000,
                loss='CE+gsTMSE',
            ),
        ],
    },
}



COLUMNS = [
    'model_name', 'dataset', 'train_dur', 'replicate_num', 'window_size', 'loss',
    'avg_val_acc_epoch', 'avg_val_acc_tfm_epoch',
    'avg_val_levenshtein_epoch', 'avg_val_levenshtein_tfm_epoch',
    'avg_val_loss_epoch',
    'avg_val_character_error_rate_epoch', 'avg_val_character_error_rate_tfm_epoch',
    'avg_val_precision_epoch', 'avg_val_precision_tfm_epoch',
    'avg_val_recall_epoch', 'avg_val_recall_tfm_epoch',
    'avg_val_fscore_epoch', 'avg_val_fscore_tfm_epoch',
]


def df_from_model_metadata_map(model_metadata_map: dict) -> pd.DataFrame:
    results_df = []

    for model_name, dataset_metadata_list_map in model_metadata_map.items():
        for dataset_name, metadata_list in dataset_metadata_list_map.items():
            for metadata in metadata_list:
                csv_path = RESULTS_ROOT / dataset_name / model_name / metadata.results_dir / 'learning_curve.csv'
                df = pd.read_csv(csv_path)
                df['dataset'] = dataset_name
                df['window_size'] = metadata.window_size
                df['loss'] = metadata.loss
                df = df[COLUMNS]
                results_df.append(df)

    results_df = pd.concat(results_df)

    columns = {
        column_old: column_old.replace('avg_val_', '').replace('_epoch', '')
        if column_old.startswith('avg_val') else column_old
        for column_old in results_df.columns
    }
    columns.update(
        {
            'model_name': 'Model',
            'window_size': 'Window Size',
            'train_dur': 'Training set size (s)',
            'loss': 'Loss',
        }
    )
    results_df = results_df.rename(columns=columns)

    results_df['frame_error'] = (1.0 - results_df['acc']) * 100
    results_df['frame_error_tfm'] = (1.0 - results_df['acc_tfm']) * 100
    for metric_name in (
        'character_error_rate',
        'character_error_rate_tfm',
        'precision',
        'precision_tfm',
        'recall',
        'recall_tfm',
        'fscore',
        'fscore_tfm',
    ):
        results_df[metric_name] = results_df[metric_name] * 100

    return results_df


data = df_from_model_metadata_map(MODEL_METADATA_MAP)

data = data.drop(columns='dataset')

id_vars = [
    'Model',
    'Training set size (s)',
    'replicate_num',
    'Loss',
]

value_vars = [
    'character_error_rate',
    'character_error_rate_tfm',
    'precision',
    'precision_tfm',
    'recall',
    'recall_tfm',
    'fscore',
    'fscore_tfm',
    'frame_error',
    'frame_error_tfm'
]

data = data.melt(id_vars=id_vars, value_vars=value_vars)

data['Post-processing'] = data['variable'].apply(lambda x: x.endswith('_tfm'))

var_metric_map = dict(zip((
    'frame_error',
    'frame_error_tfm',
    'character_error_rate',
    'character_error_rate_tfm',
    'precision',
    'precision_tfm',
    'recall',
    'recall_tfm',
    'fscore',
    'fscore_tfm',
),
(
    'Frame Error (%)',
    'Frame Error (%)',
    'Character Error Rate (%)',
    'Character Error Rate (%)',
    'Precision (%)',
    'Precision (%)',
    'Recall (%)',
    'Recall (%)',
    '$F$-score (%)',
    '$F$-score (%)',
)))

data['Metric'] = data['variable'].map(var_metric_map)


data.to_csv('results/summary-data-loss-function-experiments.csv', index=False)
