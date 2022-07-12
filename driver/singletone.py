class Singletone(type):
    """Singletone pattern as a metaclass."""
    _instance = None

    def __call__(cls, *args, **kwargs): 
        if not Singletone._instance:            
            Singletone._instance = super(Singletone, cls).__call__(*args, **kwargs)               
        return Singletone._instance

    @staticmethod
    def get_instance():
        return Singletone._instance
        