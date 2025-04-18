import h5py, yaml, sys, os, json
from torch import Tensor, from_numpy
import numpy as np
from numpy import ndarray
import torch

from typing import Any

# Interfaces between numpy and torch tensors
def torch_to_numpy(tensor: Tensor | ndarray, dtype: type = np.float32) -> ndarray:

    if isinstance(tensor, Tensor):
        # Convert to torch tensor to numpy array
        return (tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()).astype(dtype)

    elif isinstance(tensor, ndarray):
        # Return the array itself
        return tensor
    else:
        raise ValueError("Input must be a torch.Tensor or np.ndarray")


def numpy_to_torch(array: Tensor | ndarray, dtype: torch.dtype = torch.float32) -> Tensor:

    if isinstance(array, ndarray):
        # Convert numpy array to torch tensor
        return from_numpy(array).to(torch.float32)

    elif isinstance(array, Tensor):
        # Return the tensor itself
        return array
    else:
        raise ValueError("Input must be a torch.Tensor or np.ndarray")


# Conversion functions from json/yml to hdf5 and vice versa
def json_yml_to_hdf5(input_filepath: str, output_hdf5_filepath: str):
    """
    Convert a JSON or YAML file to an HDF5 file. 
    Each key from the config file becomes a dataset in the HDF5 file.

    Parameters:
        input_filepath (str): Path to the JSON or YAML file.
        output_hdf5_filepath (str): Path where the HDF5 file will be saved.
    """

    # Load data from JSON or YAML file.
    parsed_data_dict = load_json_yml(input_filepath)

    # Open the HDF5 file for writing.
    with h5py.File(output_hdf5_filepath, 'w') as hdf5_file:

        # For every key, create a dataset.
        for key, value in parsed_data_dict.items():
            # If the value is a list of numbers, convert it to a NumPy array.
            if isinstance(value, list) and all(isinstance(i, (int, float)) for i in value):
                data = np.array(value)
            else:
                data = value
                
            # Write dataset
            hdf5_file.create_dataset(key, data=data)


def load_json_yml(filepath : str) -> Any:
    """
    Load a data file from a JSON or YAML file.
    
    Parameters:
        filepath (str): The path to the JSON or YAML file.
        
    Returns:
        dict: The configuration data.
    """
    # Check file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Input file {input_filepath} not found.")

    ext = os.path.splitext(filepath)[1].lower()

    with open(filepath, 'r') as f:
        if ext == '.json':
            return json.load(f)
        
        elif ext in ('.yaml', '.yml'):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
        
def hdf5_to_json_yml(input_hdf5_filepath: str, output_filepath: str):
    """
    Convert an HDF5 file (with each key stored as a dataset in the root)
    into a single JSON or YAML file.

    Parameters:
        input_hdf5_filepath (str): Path to the HDF5 file.
        output_filepath (str): Path where the output file will be saved.  
                               Format (JSON or YAML) is determined by the extension.
    """
    data_to_parse = {}

    # Open the HDF5 file for reading.
    with h5py.File(input_hdf5_filepath, 'r') as hdf5_file:

        for key in hdf5_file.keys():
            data = hdf5_file[key][()]
            # If the data is stored as a numpy array, convert to list (or scalar if single value).
            if isinstance(data, np.ndarray):
                if data.ndim == 0:
                    data = data.item()
                else:
                    data = data.tolist()

            elif hasattr(data, 'tolist'):
                data = data.tolist()

            data_to_parse[key] = data

    # Determine the output format from the file extension.
    if output_filepath.lower().endswith('.json'):

        # To json format
        with open(output_filepath, 'w') as f:
            json.dump(data_to_parse, f, indent=4)

    elif output_filepath.lower().endswith(('.yaml', '.yml')):

        # To yaml format
        with open(output_filepath, 'w') as f:
            yaml.dump(data_to_parse, f)
    else:
        raise ValueError(
            "Output file must have a .json, .yaml, or .yml extension.")


def merge_json_yml_to_hdf5(input_filepaths: list[str], output_hdf5_filepath : str):
    """
    Merge multiple JSON or YAML configuration files into a single HDF5 file.
    For each key found in any input file, the HDF5 file will include a dataset
    containing a list of values gathered from the input files. If a key is missing in
    a file, None will be used as a placeholder.
    
    Parameters:
        input_filepaths (list[str]): List of paths to JSON or YAML files.
        output_hdf5_filepath (str): Path where the output HDF5 file will be saved.
    """
    # Compute the union of keys from all input files.
    all_keys = set()
    parsed_file_list = []

    for filepath in input_filepaths:

        parsed_file = load_json_yml(filepath)
        parsed_file_list.append(parsed_file)
        all_keys.update(parsed_file.keys())

    # Initialize a dictionary to hold merged data.
    merged_data : dict[str, Any] = {key: [] for key in all_keys}

    # For each file, append the value for each key (or None if key not found).
    for parsed_file in parsed_file_list:

        for key in all_keys:
            merged_data[key].append(parsed_file.get(key, None))

    # Write merged data to the HDF5 file.
    with h5py.File(output_hdf5_filepath, 'w') as hdf5_file:
        for key, value_list in merged_data.items():
            try:
                # Try converting to a numpy array (works well if data is homogeneous).
                data_array = np.array(value_list)
                hdf5_file.create_dataset(key, data=data_array)
            
            except Exception:
                # Fallback: store as a JSON string in case of heterogeneous data.
                json_string = json.dumps(value_list)
                dtype = h5py.string_dtype(encoding='utf-8')
                hdf5_file.create_dataset(key, data=json_string, dtype=dtype)

if __name__ == '__main__':

    output_filename = "merged_labels"
    
    # Get files in folder_path
    folder_path = "/home/peterc/devDir/projects-DART/operative/operative-develop/dataset_gen/output/Dataset_ABRAM_6547698b4de39d19e9b7d8a561c9b94d/labels"

    output_filename = os.path.join(folder_path, output_filename)
    input_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.json', '.yaml', '.yml'))]

    # Merge multiple configuration files into one HDF5 file.
    merge_json_yml_to_hdf5(input_files, output_filename + ".hdf5")

    # Try to load the merged file
    with h5py.File(output_filename + ".hdf5", 'r') as hdf5_file:
        for key in hdf5_file.keys():
            print(f"{key}: {hdf5_file[key][()]}")
