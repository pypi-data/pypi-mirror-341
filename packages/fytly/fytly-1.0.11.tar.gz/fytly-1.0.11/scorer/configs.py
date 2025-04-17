from configparser import ConfigParser


class GraderConfigs:
    props = {}

    # default constructor
    def __init__(self):
        self.props = self._load_configs()

    def _load_configs(self):
        dict = {}
        config = ConfigParser()
        with open(r'E:/sankalp/grader/configs/app.properties') as f:
            config.read_string('[config]\n' + f.read())

        for k, v in config['config'].items():
            dict[k] = v
        return dict
#E:\appsuite\common\config
