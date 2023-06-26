import json


class ServerConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data


if __name__ == '__main__':
    json_reader = ServerConfigLoader('ServerConfig.json')  # Replace 'data.json' with your JSON file path
    json_data = json_reader.read_json()
    print(json_data)