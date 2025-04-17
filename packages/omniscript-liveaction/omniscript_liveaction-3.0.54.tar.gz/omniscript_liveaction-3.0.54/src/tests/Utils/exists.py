import os


def get_data_directory() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))


def data_directory_exists() -> bool:
    """ Check if the data directory exists for conditionally skipped tests """
    data_directory_path = get_data_directory()
    return os.path.exists(data_directory_path)
