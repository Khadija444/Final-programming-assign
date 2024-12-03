import pickle

class StorageLayer:
    @staticmethod
    def save_data(filename, data):
        #saves the data to a binary file
        with open(filename, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def load_data(filename):
        #loads the data from a binary file
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None
        