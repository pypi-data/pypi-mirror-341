import importlib.resources

def get_data():
    return importlib.resources.files(__package__).joinpath("data.txt").read_text()
