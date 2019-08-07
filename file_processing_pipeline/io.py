"""Provides utilities to load and save data sets.
Mainly thin wrappers around pandas methods."""

import os

import pandas as pd


def load_csv(filepath_or_buffer):
    return pd.read_csv(filepath_or_buffer,
                       header=0,
                       dtype=str,
                       encoding='utf-8')


def load_excel(io, sheet_name):
    return pd.read_excel(io, sheet_name)


def __ensure_dir_exists(file_name):
    dir_name = os.path.dirname(file_name)
    os.makedirs(dir_name, exist_ok=True)


def save_parquet(df, fname):
    __ensure_dir_exists(fname)
    df.to_parquet(fname)


def save_csv(df, path_or_buf):
    __ensure_dir_exists(path_or_buf)
    df.to_csv(path_or_buf,
              index=False,
              header=True,
              encoding='utf8')
