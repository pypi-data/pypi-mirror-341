import pyarrow as pa
import pyarrow.dataset as pads
import adlfs
import pyarrow as pa
import pyarrow.parquet as pq
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from tqdm import tqdm
import gc
import pandas as pd
import pyarrow.fs as pa_fs
import datetime
import polars as pl
import os
from pathlib import Path


class PandasBatcher:
    ## Read info
    read_path = None
    read_account_name = None
    read_storage_options = None
    read_abfs = None
    read_credential = None
    read_schema = None

    ## Batch info
    batch_size = None
    max_file_size = 700 * 1024 * 1024
    dataset = None
    current_batch = None    
    file_index = 0
    writer = None
    current_size = 0
    processing_function = None
    total_rows = 0
    total_fragments = 0
    columns = None

    ## Write info
    write_path = None
    write_account_name = None
    write_storage_options = None
    write_abfs = None
    write_credential = None
    write_schema = None


    def __init__(self, path,batch_size, account_name=None, storage_options=None,  columns=None, platform='azure', credentials=None, schema=None):
        self.read_path = path
        self.batch_size = batch_size
        self.columns = columns
        self.read_schema = schema

        if platform == 'azure':
            self.read_account_name = account_name
            self.read_abfs = self._set_azure_fs(storage_options, account_name)

            
        if platform == 'gcs':
            expiration = credentials.expiry if credentials.expiry else datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            self.read_abfs = pa_fs.GcsFileSystem(access_token=credentials.token, credential_token_expiration=expiration)

        if platform in ['azure', 'gcs']:

            if isinstance(self.read_path, str):
                self.read_path = self.read_path.replace("abfs://", "").replace('gcs://', '')
                self.dataset = pads.dataset(self.read_path, format='parquet', filesystem=self.read_abfs)

            elif isinstance(self.read_path, list):
                dss = []
                for path in self.read_path:
                    path = path.replace("abfs://", "").replace('gcs://', '')
                    dss.append(pads.dataset(path, format='parquet', filesystem=self.read_abfs))
                self.dataset = pads.dataset(dss)
        elif platform == 'local':
            self.dataset = pads.dataset(self.read_path, format='parquet')

          
            
    def get_dataset(self):
        return self.dataset

    def _open_new_writer(self, file_path):
        self.writer = pq.ParquetWriter(file_path, self.write_schema, filesystem=self.write_abfs, use_compliant_nested_type=True)

    def _close_writer(self):
        self.writer.close()
        self.writer = None


    def _write_batches_pandas(self, platform):
        self.total_fragments = len(list(self.dataset.get_fragments()))
        for fragment in tqdm(self.dataset.get_fragments(), total=self.total_fragments, desc=f"Processing dataset for {self.read_path}"):   
            scanner = fragment.scanner(columns=self.columns, batch_size=self.batch_size)
            for batch in scanner.to_batches():
                batch = self.processing_function(batch.to_pandas())
                if not self.write_schema:
                    self.write_schema = pa.Schema.from_pandas(batch)
                self.current_size += batch.memory_usage(index=True).sum()
                if self.writer is None:
                    if platform in ['azure', 'gcs']:
                        file_path = f"abfs://{self.write_path}/part.{self.file_index}.parquet"
                        if platform == 'gcs':
                            file_path = file_path.replace('abfs://', '')
                        self._open_new_writer(file_path)
                        self.file_index += 1
                    elif platform == 'local':
                        file_path = f"{self.write_path}/part.{self.file_index}.parquet"
                        Path(self.write_path).mkdir(parents=True, exist_ok=True)
                        self._open_new_writer(file_path)
                        self.file_index += 1
                elif self.current_size > self.max_file_size:
                    if platform in ['azure', 'gcs']:
                        self._close_writer()
                        file_path = f"abfs://{self.write_path}/part.{self.file_index}.parquet"
                        if platform == 'gcs':
                            file_path = file_path.replace('abfs://', '')
                        self._open_new_writer(file_path)
                        self.file_index += 1
                        self.current_size = 0
                    elif platform == 'local':
                        self._close_writer()
                        file_path = f"{self.write_path}/part.{self.file_index}.parquet"
                        Path(self.write_path).mkdir(parents=True, exist_ok=True)
                        self._open_new_writer(file_path)
                        self.file_index += 1
                        self.current_size = 0
                batch = pa.RecordBatch.from_pandas(batch, preserve_index=True, schema=self.write_schema)
                self.writer.write_batch(batch)
        print(f"Done writing to {self.write_path}")
        self._close_writer()

    def _write_batches_polars(self, platform):
        self.total_fragments = len(list(self.dataset.get_fragments()))
        for fragment in tqdm(self.dataset.get_fragments(), total=self.total_fragments, desc=f"Processing dataset for {self.read_path}"):   
            scanner = fragment.scanner(columns=self.columns, batch_size=self.batch_size)
            for batch in scanner.to_batches():
                batch = pl.from_arrow(batch)
                batch = self.processing_function(batch)
                if not self.write_schema:
                    self.write_schema = pa.Schema.from_pandas(batch)
                self.current_size += batch.estimated_size()
                if self.writer is None:
                    file_path = f"abfs://{self.write_path}/part.{self.file_index}.parquet"
                    if platform == 'gcs':
                        file_path = file_path.replace('abfs://', '')
                    self._open_new_writer(file_path)
                    self.file_index += 1
                elif self.current_size > self.max_file_size:
                    self._close_writer()
                    file_path = f"abfs://{self.write_path}/part.{self.file_index}.parquet"
                    if platform == 'gcs':
                        file_path = file_path.replace('abfs://', '')
                    self._open_new_writer(file_path)
                    self.file_index += 1
                    self.current_size = 0
                batch = batch.to_pandas()
                batch = pa.RecordBatch.from_pandas(batch, preserve_index=True, schema=self.write_schema)
                self.writer.write_batch(batch)
        print(f"Done writing to {self.write_path}")
        self._close_writer()
        
    def _clear_memory(self):
        gc.collect()
        pool = pa.default_memory_pool()
        pool.release_unused()
        gc.collect()

    def _set_azure_fs(self, storage_options, account_name):
            if "credential" in storage_options:
                credential = DefaultAzureCredential()
                access_token = credential.get_token("https://storage.azure.com/.default")
                return adlfs.AzureBlobFileSystem(account_name=account_name, token=access_token.token)
            else:
                credential = ClientSecretCredential(
                    client_id=storage_options['client_id'],
                    client_secret=storage_options['client_secret'],
                    tenant_id=storage_options['tenant_id']
                )
                return adlfs.AzureBlobFileSystem(account_name=account_name, credential=credential)
                

    def process_data(self, path, processing_function, account_name=None, storage_options=None, max_file_size=700 * 1024 * 1024, platform = 'azure', credentials=None, schema=None, tool='pandas'):
        self.processing_function = processing_function
        self.write_path = path.replace('abfs://', '').replace('gcs://', '')
        self.write_schema = schema
        if platform == 'azure':
            self.write_account_name = account_name
            self.write_abfs = self._set_azure_fs(storage_options, account_name)
            # Make sure to empty the folder from parquet files
            all_files = self.write_abfs.glob(f"{path}*")
            parquet_files = [file for file in all_files if file.endswith('.parquet')]
            for file in parquet_files:
                self.write_abfs.rm(file)
            
        if platform == 'gcs':
            expiration = credentials.expiry if credentials.expiry else datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            self.write_abfs = pa_fs.GcsFileSystem(access_token=credentials.token, credential_token_expiration=expiration)
            try:
                file_info_list = self.write_abfs.get_file_info(pa.fs.FileSelector(path, recursive=False))
                parquet_files = [file_info.path for file_info in file_info_list if file_info.path.endswith(".parquet")]
                for file_path in parquet_files:
                    self.write_abfs.delete_file(file_path)
            except Exception as e:
                print(e)
        if platform == 'local':
            # Make sure to empty the folder from parquet files
            try:
                all_files = os.listdir(self.write_path)
            except FileNotFoundError:
                all_files = []
            parquet_files = [file for file in all_files if file.endswith('.parquet')]
            for file in parquet_files:
                os.remove(file)
        # Make sure to empty the folder from parquet files
        self.max_file_size = max_file_size
        if tool == 'pandas':
            self._write_batches_pandas(platform)
        elif tool == 'polars': 
            self._write_batches_polars(platform)




    def get_first_batch(self):
        return next(self.dataset.get_fragments()).head(self.batch_size, self.columns).to_pandas()
    
    def count(self, filterxp=None):
        return self.dataset.count_rows(filter=filterxp)
    def filter(self, expression):
        filtered_ds = self.dataset.filter(expression)
        print(f"Found {filtered_ds.count_rows()} rows")
        return filtered_ds.head(self.batch_size, self.columns).to_pandas()
    def __del__(self):
        self._clear_memory()