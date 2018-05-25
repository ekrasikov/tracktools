class StorageHelper():
    '''Helper Class to save workout in persistent storage'''
    def __init__(self, storage_endpoint):
        self.storage_endpoint = storage_endpoint
        pass

    def save_workout(self, workout):
        '''Save workout to storage_endpoint, return id'''
        pass

    def load_workout(self, id):
        '''Load workout from storage_endpoint, return workout'''
        pass
