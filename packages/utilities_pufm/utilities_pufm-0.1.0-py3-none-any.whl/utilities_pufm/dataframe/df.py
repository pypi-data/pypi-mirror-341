import threading
import gc

import pandas as pd

from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from pandas.core.groupby.generic import DataFrameGroupBy

class DataFrameThreadManager:
    def __init__(self, work_function: Callable) -> None:
        
        self.worker_function = work_function
        
    def _process_chunk(self, chunk_data: tuple) -> None:
        with threading.Lock():
            return self.worker_function(**chunk_data)
    
    def parallelize_process(self, df: pd.DataFrame | DataFrameGroupBy, n_cores=(cpu_count() - 2), params=None) -> list:
        
        # Prepara chunks
        n_rows = len(df)
        if n_rows < n_cores:
            n_cores = n_rows
            print(f"Warning: Adjusted number of threads to {n_cores} to match data size")
            
        # chunks = np.array_split(df, n_cores)
        chunk_size = n_rows // n_cores # result will be integer division
        remainder = n_rows % n_cores # remainder is the rest
        
        chunks = []
        start = 0
        if isinstance(df, pd.DataFrame):
            for i in range(n_cores):
                end = start + chunk_size + (1 if i < remainder else 0)
                if params:
                    chunks.append({
                        "t_num": i,
                        "df": df.iloc[start:end],
                        "params": params
                    })
                else:
                    chunks.append({
                        "t_num": i,
                        "df": df.iloc[start:end]
                    })
                start = end
        elif isinstance(df, DataFrameGroupBy):
            df = list(df)
            for i in range(n_cores):
                end = start + chunk_size + (1 if i < remainder else 0)  # Distribui os grupos entre os chunks
                if params:
                    chunks.append({
                        "t_num": i,
                        "df": df[start:end],
                        "params": params
                    })
                else:
                    chunks.append({
                        "t_num": i,
                        "df": df[start:end]
                    })
                start = end
        elif isinstance(df, list):
            for i in range(n_cores):
                end = start + chunk_size + (1 if i < remainder else 0)  # Distribui os grupos entre os chunks
                if params:
                    chunks.append({
                        "t_num": i,
                        "df": df[start:end],
                        "params": params
                    })
                else:
                    chunks.append({
                        "t_num": i,
                        "df": df[start:end]
                    })
                start = end
        gc.collect()
        
        with ThreadPoolExecutor(max_workers=n_cores) as executor:
            results = list(executor.map(self._process_chunk, chunks))
        
        return results