from util.json_util import JsonUtils 


class ConfigManager:
    """Methods for parsing and getting config data."""
    _config = {}
    _test_data = {}
    _config_js = {}    

    @staticmethod
    def parse_config_for_driver(config='config.json'):
        """Parse data for Webdriver's settings ."""
        if not ConfigManager._config:
            ConfigManager._config = JsonUtils.read_from_json(config) 
        options = []
        methods = []
        if 'flags' in ConfigManager._config: 
            for k, v in ConfigManager._config['flags'].items():                
                if v == 'True':                    
                    if k == 'incognito':                        
                        options.append("--incognito")
                    if k == 'jenkins':                        
                        options.extend((
                            "--headless", "--disable-dev-shm-usage", \
                            "--no-sandbox", "--window-size=1920x1080", \
                            "--verbose", "--disable-gpu", \
                            "disable-infobars", "--disable-extensions"))
                    if k == 'maximize_window':
                        methods.append("maximize_window")            
        return options, methods

    @staticmethod
    def get_value_from_config(key, config='config.json'):        
        """Get specific value by key from config data."""
        if not ConfigManager._config:
            ConfigManager._config = JsonUtils.read_from_json(config)
        return ConfigManager._config.get(key)   

    @staticmethod
    def get_value_from_test_data(key, test_data='tests/test_data/test_data.json'):        
        """Get value from test data by key."""
        if not ConfigManager._test_data:
            ConfigManager._test_data = JsonUtils.read_from_json(test_data)
        return ConfigManager._test_data[key]

    @staticmethod
    def get_js_path(key, js_config='config_js_scripts.json'):
        """Get path to JS script by key.
        Returns:
            Str: path to script or None: if no such key
        """
        if not ConfigManager._config_js:
            ConfigManager._config_js = JsonUtils.read_from_json(js_config)
        return ConfigManager._config_js[key]
