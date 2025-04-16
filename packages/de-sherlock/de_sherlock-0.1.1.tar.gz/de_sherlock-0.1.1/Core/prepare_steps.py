class Step:
    def __init__(self, name, title, description,step_number=None,timestamp=None,unique_id=None,config=None,DebugMode=False):
        self.name = name
        self.title = title
        self.description = description
        self.step_number = step_number
        self.timestamp_for_file_path = timestamp
        self.unique_id=unique_id
        self.config = config
        self.DebugMode= DebugMode



