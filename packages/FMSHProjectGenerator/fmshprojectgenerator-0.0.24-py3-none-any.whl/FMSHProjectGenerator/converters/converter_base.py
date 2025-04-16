import json
import os

from ruamel.yaml import YAML


class Converter:
    def __init__(self):
        # ruamel.yaml实例
        self._yml = YAML(typ='rt')

        # 将None输出设定为null
        def represent_none(self, data):
            return self.represent_scalar('tag:yaml.org,2002:null', 'null')

        self._yml.representer.add_representer(type(None), represent_none)

        # 设定ruamel.yaml流格式
        self._yml.default_flow_style = False

    # 获取工程模板文件路径
    @staticmethod
    def load_template(self):
        f = open(os.path.join(os.path.dirname(__file__), '..', 'assets', 'project_template.yaml'))
        tmp = self._yml.load(f)
        f.close()
        return tmp

    @staticmethod
    def load_chip(chip_name: str):
        chip = None
        if chip_name is not None:
            chip_file = os.path.join(os.path.dirname(__file__), '..', 'chips', chip_name + '.json')
            if os.path.exists(chip_file):
                if os.access(chip_file, os.R_OK):
                    f = open(chip_file, 'r')
                    chip = json.load(fp=f)
                    f.close()
        if chip is None:
            raise ChipNotFoundError(chip_name)
        return chip

    @staticmethod
    def translate_path(raw_path, rel_path):
        _path = os.path.join(rel_path, raw_path)
        return os.path.normpath(_path).replace('\\', '/')

    # 获取工程文件需求抽象接口
    def project_requirement(self) -> dict:
        pass

    # 分析工程抽象接口
    def analyze_project(self, prj_files: dict, target_name: str = '', output_file: str = '') -> dict:
        """
        分析目标工程并返回工程描述信息。

        :param prj_files: 工程文件路径字典，所需内容依据不同的解析器的实现有所不同。
        :param target_name: （可选，部分解析器指定此项无效）目标名称。如果一个工具链工程中有多个目标，可以通过该项指定需要转换哪个目标。默认转换首个搜索到的目标。
        :param output_file: （可选）输出文件路径。指定该项可以将工程描述信息到处到文件中（yaml格式）。
        """
        pass


class FileFormatError(Exception):
    pass


class ChipNotFoundError(Exception):
    pass
