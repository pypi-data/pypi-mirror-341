import json
import os
from copy import deepcopy

from jinja2 import Environment, FileSystemLoader, select_autoescape
from ruamel.yaml import YAML

from FMSHProjectGenerator.converters import Converter
from FMSHProjectGenerator.generators import Generator


class ProjectGenerator:
    def __init__(self):
        # ruamel.yaml对象
        self.__yaml = YAML(typ='rt')

        # 工程对象
        self.__prj_desc = None

    def convert(self, src_prj_path, converter: Converter, output_file: str = '') -> dict:
        # 获取转换器所需工程文件
        req = converter.project_requirement()

        # 查找工程文件
        for root, dirs, files in os.walk(src_prj_path, topdown=False):
            for name in files:
                ext_name = name.split('.')[-1]
                if ext_name in req.keys():
                    _file = os.path.join(root, name)
                    _file_dir = os.path.relpath(root, src_prj_path).replace('\\', '/')
                    req[ext_name] = (_file, _file_dir)

        # 转换并保存工程对象，并返回
        self.__prj_desc = converter.analyze_project(req, output_file=output_file)
        return self.__prj_desc

    def generate(self, dest_prj_path, generator: Generator, generator_version, input_desc=None, **kwargs):
        # 加载工程描述
        if input_desc is None:
            # 使用已有内容进行转换
            if self.__prj_desc is None:
                # 无可用配置，报错
                raise Exception('input_desc param is not valid!')
        else:
            # 文件形式
            if isinstance(input_desc, str):
                try:
                    f = open(input_desc, 'r')
                    self.__prj_desc = self.__yaml.load(f)
                    f.close()
                except FileNotFoundError:
                    raise FileNotFoundError('project description file not exists!')
            # 字典形式
            elif isinstance(input_desc, dict):
                self.__prj_desc = deepcopy(input_desc)
            else:
                # 配置格式不正确，报错
                raise Exception('failed to load project!')

        # 检查芯片型号是否正确，并加载芯片配置
        chip = None
        if self.__prj_desc['target'] is not None:
            chip_file = os.path.join(os.path.dirname(__file__), 'chips', str.upper(self.__prj_desc['target']) + '.json')
            if os.path.exists(chip_file):
                if os.access(chip_file, os.R_OK):
                    f = open(chip_file, 'r')
                    chip = json.load(fp=f)
                    f.close()
        if chip is None:
            raise Exception("Configuration file not found for chip " + self.__prj_desc['target'])

        # 添加芯片的工程相关参数到工程
        # 全局定义
        if 'defines' not in self.__prj_desc or self.__prj_desc['defines'] is None:
            self.__prj_desc['defines'] = []
        self.__prj_desc['defines'] = chip['defines'] + self.__prj_desc['defines']

        # 生成工程
        generator.generate(self.__prj_desc, chip['target'], dest_prj_path, generator_version, **kwargs)
