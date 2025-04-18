import zipfile
import os
import io
import re

from typing import List, Tuple

from xldg.xl import XL, CrossLinkDataset



class Path:
    @staticmethod
    def list_specified_type_files_from_folder(folder_path: str, file_format: str) -> List[str]:
        files = []
        for file in os.listdir(folder_path):
            if file.endswith(file_format):
                files.append(os.path.join(folder_path, file))

        return files

    @staticmethod
    def sort_filenames_by_first_integer(strings: List[str]) -> List[str]:
        def extract_leading_integer_from_file_name(s: str) -> int:
            file_path_only = os.path.basename(s)
            match = re.match(r'^(\d+)_', file_path_only)
            return int(match.group(1)) if match else float('inf')

        sorted_strings = sorted(strings, key=extract_leading_integer_from_file_name)

        return sorted_strings

class DatasetUtil:
    @staticmethod
    def read_merox_file(self, path: str, linker: str) -> 'CrossLinkDataset':
        xls = []
        software = 'MeroX'

        with zipfile.ZipFile(path, 'r') as zip_ref:
            with zip_ref.open('Result.csv') as csv_file:
                for line in io.TextIOWrapper(csv_file, encoding='utf-8'):
                    row = line.strip().split(';')
                    xl = XL(row[7], row[6], row[8], row[9], row[20], 
                            row[11], row[10], row[12], row[13], row[21],
                            row[0], software, linker)
                    xls.append(xl)

        dataset = CrossLinkDataset(xls)
        dataset.set_xls_counter_to_one()

        return dataset

    @staticmethod
    def read_all_merox_files(self, path_list: List[str], linker: str = None) -> List['CrossLinkDataset']:
        file_content = []
    
        for path in path_list:
            print(f'Extracting: {path}')
            file_content.append(self.read_merox_file(path, linker))   

        return file_content

    @staticmethod
    def filter_all_by_score(self, dataset: List['CrossLinkDataset'], threshold: int = 50) -> List['CrossLinkDataset']:
        for data in dataset:
            data.filter_by_score(threshold)
        return dataset    

    @staticmethod
    def combine_replicas(self, dataset: List['CrossLinkDataset'], n=3) -> List['CrossLinkDataset']:
        combined_dataset = []
        buffer = []
    
        if ((len(dataset) % n) != 0):
            raise Exception(f'ERROR! dataset size {len(dataset)} is not mutiple to n={n}')
    
        for data in dataset:
            if (len(buffer) == n):
                combined_dataset.append(CrossLinkDataset.combine_datasets(buffer))
                buffer.clear()
            buffer.append(data)
        
        combined_dataset.append(CrossLinkDataset.combine_datasets(buffer))

        return combined_dataset

    @staticmethod
    def fuse_list_of_xl_datsets(self, dataset_list: List['CrossLinkDataset']) -> 'CrossLinkDataset':
        return CrossLinkDataset([element for sublist in dataset_list for element in sublist])

    @staticmethod
    def generate_custom_list_with_int_ranges(self, *diapason: Tuple[int, int]) -> List[int]:
        custom_list = []

        for pair in diapason:
            start = pair[0]
            end = pair[1]
    
            for i in range(start, end):
                custom_list.append(i)

        return custom_list

    @staticmethod
    def combine_selected_datasets(self, dataset_list: List['CrossLinkDataset'], indexes: List[int]) -> 'CrossLinkDataset':
        buffer = []
    
        for x in indexes:
            buffer.append(dataset_list[x])

        return CrossLinkDataset.combine_datasets(buffer) 