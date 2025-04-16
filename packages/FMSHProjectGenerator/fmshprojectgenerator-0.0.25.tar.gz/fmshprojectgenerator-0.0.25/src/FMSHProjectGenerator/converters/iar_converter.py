import re
import os

import chardet
import xmltodict

from FMSHProjectGenerator.converters import Converter, FileFormatError


class IARConverter(Converter):
    # 优化等级
    __optimize_level = {
        '0': 'none',
        '1': 'low',
        '2': 'medium',
        '3': 'high',
    }

    # 优化策略
    __optimize_hint = {
        '0': 'balanced',
        '1': 'size',
        '2': 'speed',
    }

    # 仿真器
    __debugger = {
        'JLINK_ID': 'jlink',
    }

    # Jlink: 复位
    __jlink_reset = {
        '5': 'normal',
        '8': 'core',
        '10': 'reset pin',
    }

    def __init__(self):
        super().__init__()

    @staticmethod
    def _find_option(settings: list, setting_name: str, option_name: str, raise_error: bool = True):
        try:
            _opts = None
            for _setting in settings:
                if _setting['name'] == setting_name:
                    _opts = _setting['data']['option']
                    break
            if _opts is not None:
                for _opt in _opts:
                    if _opt['name'] == option_name:
                        return _opt['state']
        except KeyError:
            pass
        if raise_error:
            raise FileFormatError('解析配置 ' + setting_name + '.' + option_name + ' 失败')

    @staticmethod
    def _process_path(path_name: str, prj_file_rel_path: str) -> str:
        path_name = path_name.replace('\\', '/')
        if not os.path.isabs(path_name):
            if path_name.startswith('$PROJ_DIR$/'):
                path_name = path_name.replace('$PROJ_DIR$/', './', 1)
            if not path_name.startswith('$TOOLKIT_DIR$'):   # 特殊工具链路径标志不做处理
                path_name = Converter.translate_path(path_name, prj_file_rel_path)
        return path_name

    @staticmethod
    def _get_file_info(file_path: str) -> dict:
        _file_name = file_path.replace('\\', '/').split('/')[-1]
        _file_ext = _file_name.split('.')[-1]
        _file_type = 'TXT'
        if _file_ext.lower() == 'c':
            _file_type = 'C'
        elif _file_ext.lower() in ['s', 'asm']:
            _file_type = 'ASM'
        elif _file_ext == 'CPP':
            _file_type = 'CPP'
        elif _file_ext.lower() in ['lib']:
            _file_type = 'LIB'
        return {'name': _file_name, 'type': _file_type, 'path': file_path}

    @staticmethod
    def _create_group(group, prj_file_rel_path) -> dict:
        # 创建组对象
        prj_group = {
            'name': group['name'],
            'files': None,
            'groups': None,
        }
        # 添加文件
        if 'file' in group and group['file'] is not None:
            prj_group['files'] = []
            if not isinstance(group['file'], list):
                _file_name = group['file']['name']
                _file_name = IARConverter._process_path(_file_name, prj_file_rel_path)
                prj_group['files'].append(IARConverter._get_file_info(_file_name))
            else:
                for _file in group['file']:
                    _file_name = _file['name']
                    _file_name = IARConverter._process_path(_file_name, prj_file_rel_path)
                    prj_group['files'].append(IARConverter._get_file_info(_file_name))
        # 添加组
        if 'group' in group and group['group'] is not None:
            prj_group['groups'] = []
            if not isinstance(group['group'], list):
                prj_group['groups'].append(IARConverter._create_group(group['group'], prj_file_rel_path))
            else:
                for group in group['group']:
                    prj_group['groups'].append(IARConverter._create_group(group, prj_file_rel_path))
        return prj_group

    def project_requirement(self):
        # IAR 工程文件字典
        return {'ewp': None, 'ewd': None}

    def analyze_project(self, prj_files: dict, target_name: str = '', output_file: str = '') -> dict:
        # 检查文件有效性
        if 'ewp' not in prj_files.keys() or prj_files['ewp'] is None or \
                not isinstance(prj_files['ewp'], tuple):
            raise FileNotFoundError('IAR project file(*.ewp) not found!')

        if 'ewd' not in prj_files.keys() or prj_files['ewd'] is None or \
                not isinstance(prj_files['ewd'], tuple):
            raise FileNotFoundError('IAR debug file(*.ewd) not found!')

        # 记录工程文件相对生成工程目录路径（注意：生成工程目录总是根目录的一级子目录）
        prj_file_rel_path = os.path.join('..', prj_files['ewp'][1])

        # ---------------- 加载工程描述文件模板 ----------------
        prj_desc = self.load_template(self)

        # ---------------- 加载工程 ----------------
        # 读取工程文件
        with open(prj_files['ewp'][0], 'rb') as f:  # 先用二进制打开以获取编码
            data = f.read()  # 读取文件内容
            file_encoding = chardet.detect(data)['encoding']  # 得到文件的编码格式
        try:
            with open(prj_files['ewp'][0], 'r', encoding=file_encoding) as f:  # 文本模式打开
                _xml = f.read()
        except UnicodeDecodeError:
            # 有时chardet会检测出错，此时我们使用UTF-8编码重试，此时失败将抛出错误
            with open(prj_files['ewp'][0], 'r', encoding='utf-8') as f:  # 文本模式打开
                _xml = f.read()
        project = xmltodict.parse(_xml, force_list=())['project']
        # 如果有多个配置，选择第一个调试配置
        if isinstance(project['configuration'], list):
            project_config = project['configuration'][0]
            for _cfg in project['configuration']:
                if _cfg['debug'] == '1':
                    project_config = _cfg
                    break
        else:
            project_config = project['configuration']
        project_settings = project_config['settings']

        # 读取调试选项文件
        with open(prj_files['ewd'][0], 'rb') as f:  # 先用二进制打开以获取编码
            data = f.read()  # 读取文件内容
            file_encoding = chardet.detect(data)['encoding']  # 得到文件的编码格式
        try:
            with open(prj_files['ewd'][0], 'r', encoding=file_encoding) as f:  # 文本模式打开
                _xml = f.read()
        except UnicodeDecodeError:
            # 有时chardet会检测出错，此时我们使用UTF-8编码重试，此时失败将抛出错误
            with open(prj_files['ewd'][0], 'r', encoding='utf-8') as f:  # 文本模式打开
                _xml = f.read()
        project_dbg = xmltodict.parse(_xml, force_list=())['project']
        # 如果有多个配置，选择第一个调试配置
        if isinstance(project_dbg['configuration'], list):
            project_dbg_config = project_dbg['configuration'][0]
            for _cfg in project_dbg['configuration']:
                if _cfg['debug'] == '1':
                    project_dbg_config = _cfg
                    break
        else:
            project_dbg_config = project_dbg['configuration']
        project_dbg_settings = project_dbg_config['settings']

        # ---------------- 加载芯片配置文件 ----------------
        target_chip_name = self._find_option(project_settings, 'General', 'OGChipSelectEditMenu')
        target_chip_name = target_chip_name.split('\t')[0].upper()
        target_chip = self.load_chip(target_chip_name)

        # ---------------- 生成工程描述yaml对象 ----------------
        # 工程名称
        try:
            prj_desc['name'] = project_config['name']
        except KeyError:
            raise FileFormatError('Cannot find target name')

        # 工程目标
        prj_desc['target'] = target_chip_name

        # 工程选项
        # —— Options: C/C++ dialect (Version)
        try:
            c_ver = self._find_option(project_settings, 'ICCARM', 'IccCDialect')
            if c_ver == 0:
                prj_desc['options']['c_version'] = 'c90'  # C89 in IAR, we change it to C90:
            else:
                prj_desc['options']['c_version'] = 'c99'  # Standard C in IAR, we change it to C99:
        except (KeyError, FileFormatError):
            print('Target has no \'C dialect\' option, default to C90')
            prj_desc['options']['c_version'] = 'c90'
        # IAR C++ version is unknown, set to c++11
        prj_desc['options']['cpp_version'] = 'c++11'

        # —— Options: C/C++: Optimization
        try:
            optimize_lvl = self._find_option(project_settings, 'ICCARM', 'CCOptLevel')
            optimize_strategy = self._find_option(project_settings, 'ICCARM', 'CCOptStrategy')
        except (KeyError, FileFormatError):
            print('Target has wrong \'Optimization\' option, default to 0(No Optimization)')
            optimize_lvl = '0'
            optimize_strategy = '0'
        prj_desc['options']['optimize'] = self.__optimize_level[optimize_lvl]
        prj_desc['options']['optimize_hint'] = self.__optimize_hint[optimize_strategy]
        if prj_desc['options']['optimize'] == 'high' and prj_desc['options']['optimize_hint'] != 'speed':
            # Select best strategy
            prj_desc['options']['keil_use_optimize_hint'] = True
        else:
            prj_desc['options']['keil_use_optimize_hint'] = False

        # —— C/C++: IAR Lib
        try:
            rt_lib = self._find_option(project_settings, 'General', 'GRuntimeLibSelect')
        except (KeyError, FileFormatError):
            print('Target has no \'Library\' option, default to Full')
            rt_lib = '2'
        if rt_lib == '2':
            prj_desc['options']['iar_lib'] = 'full'
        else:
            prj_desc['options']['iar_lib'] = 'normal'

        # 由于Keil配置相对复杂，此处需要自动推断部分Keil配置，否则可能生成的Keil工程不符合预期
        if target_chip['target']['cpu_type'] in ['Cortex-M33', 'Cortex-M23', 'Star-MC1']:
            prj_desc['options']['keil_compiler'] = 'v6'
            prj_desc['options']['keil_warning'] = 'ac5-like warnings'
        else:
            prj_desc['options']['keil_compiler'] = 'v5'
            prj_desc['options']['keil_warning'] = 'all warnings'

        # 工程高级选项 —— linker script file(*.icf)
        try:
            icf_override = self._find_option(project_settings, 'ILINK', 'IlinkIcfOverride')
            if icf_override != '0':
                prj_desc['advanced_options']['iar_linker_cfg'] = \
                    self._find_option(project_settings, 'ILINK', 'IlinkIcfFile')
        except (KeyError, FileFormatError):
            pass

        # 调试工具
        try:
            jlink_sel = self._find_option(project_dbg_settings, 'JLINK_ID', 'CCJLinkInterfaceRadio')
            if jlink_sel == '1':
                debug_tool_sel = 'jlink'
            else:
                print('Target has unsupported \'Debug Tool\' Option, default to JLink')
                debug_tool_sel = 'jlink'
        except (KeyError, FileFormatError):
            print('Target has no \'Debug Tool\' Option, default to JLink')
            debug_tool_sel = 'jlink'

        # JLink ---------------------------------------------------------------
        if debug_tool_sel == 'jlink':
            prj_desc['debug']['tool'] = 'jlink'

            # -- 接口
            prj_desc['debug']['interface'] = 'SWD'  # 我们暂时固定选择SWD

            # -- 速率
            try:
                prj_desc['debug']['speed'] = int(self._find_option(project_dbg_settings, 'JLINK_ID', 'JLinkSpeed'))
            except (KeyError, FileFormatError):
                print('Target has no \'Jlink.speed\' Option, default to \'5000\'')
                prj_desc['debug']['speed'] = 5000

            # -- 连接
            prj_desc['debug']['connect'] = 'with pre-reset'  # 我们暂时固定选择with pre-reset

            # -- 复位
            try:
                reset = self._find_option(project_dbg_settings, 'JLINK_ID', 'CCJLinkResetList')
                if reset in self.__jlink_reset:
                    prj_desc['debug']['reset'] = self.__jlink_reset[reset]
                else:
                    print('Target has unsupported \'Jlink.reset\' Option, default to \'reset pin\'')
                    prj_desc['debug']['reset'] = 'reset pin'
            except (KeyError, FileFormatError):
                print('Target has no \'Jlink.reset\' Option, default to \'reset pin\'')
                prj_desc['debug']['reset'] = 'reset pin'

            # -- 下载（使用默认配置）
            prj_desc['debug']['download']['erase'] = 'sectors'
            prj_desc['debug']['download']['program'] = True
            prj_desc['debug']['download']['verify'] = True
            prj_desc['debug']['download']['reset-run'] = True

            # -- FlashLoader
            try:
                loader_override = self._find_option(project_dbg_settings, 'C-SPY', 'OverrideDefFlashBoard')
                if loader_override != '0':
                    prj_desc['advanced_options']['iar_flasher_cfg'] = \
                        self._find_option(project_dbg_settings, 'C-SPY', 'FlashLoadersV3')
            except (KeyError, FileFormatError):
                pass

        # 编译器全局定义
        try:
            defines = self._find_option(project_settings, 'ICCARM', 'CCDefines')
            if defines is not None:
                if isinstance(defines, str):
                    prj_desc['defines'] = [defines]
                else:
                    prj_desc['defines'] = defines
            else:
                prj_desc['defines'] = []
        except (KeyError, FileFormatError):
            print('Target has no \'Defines\', default to an empty list')
            prj_desc['defines'] = []
        # 去除芯片的define
        for define in prj_desc['defines']:
            if define in target_chip['defines']:
                prj_desc['defines'].remove(define)

        # 包含路径
        try:
            includes = self._find_option(project_settings, 'ICCARM', 'CCIncludePath2')
            if includes is not None:
                if isinstance(includes, str):
                    includes = self._process_path(includes, prj_file_rel_path)
                    prj_desc['includePaths'] = [includes]
                else:
                    prj_desc['includePaths'] = []
                    for include in includes:
                        include = self._process_path(include, prj_file_rel_path)
                        prj_desc['includePaths'].append(include)
            else:
                prj_desc['includePaths'] = []
        except (KeyError, FileFormatError):
            print('Target has no \'Includes\', default to an empty list')
            prj_desc['includePaths'] = []

        # 编译器全局定义(ASM)
        try:
            defines = self._find_option(project_settings, 'AARM', 'ADefines')
            if defines is not None:
                if isinstance(defines, str):
                    prj_desc['definesASM'] = [defines]
                else:
                    prj_desc['definesASM'] = defines
            else:
                prj_desc['definesASM'] = []
        except (KeyError, FileFormatError):
            print('Target has no \'Defines(ASM)\', default to an empty list')
            prj_desc['definesASM'] = []

        # 包含路径(ASM)
        try:
            includes = self._find_option(project_settings, 'AARM', 'AUserIncludes')
            if includes is not None:
                if isinstance(includes, str):
                    includes = self._process_path(includes, prj_file_rel_path)
                    prj_desc['includePathsASM'] = [includes]
                else:
                    prj_desc['includePathsASM'] = []
                    for include in includes:
                        include = self._process_path(include, prj_file_rel_path)
                        prj_desc['includePathsASM'].append(include)
            else:
                prj_desc['includePathsASM'] = []
        except (KeyError, FileFormatError):
            print('Target has no \'IncludesASM\', default to an empty list')
            prj_desc['includePathsASM'] = []

        # 文件组
        prj_desc['groups'] = []
        try:
            groups = project['group']
            if not isinstance(groups, list):
                prj_desc['groups'] = [self._create_group(groups, prj_file_rel_path)]
            else:
                for group in groups:
                    prj_desc['groups'].append(self._create_group(group, prj_file_rel_path))
        except KeyError:
            print('Target has wrong \'File Groups\', default to an empty list')
            prj_desc['groups'] = []

        if 'file' in project and project['file'] is not None:
            prj_desc['files'] = []
            if not isinstance(project['file'], list):
                _file_name = project['file']['name']
                _file_name = IARConverter._process_path(_file_name, prj_file_rel_path)
                prj_desc['files'].append(IARConverter._get_file_info(_file_name))
            else:
                for _file in project['file']:
                    _file_name = _file['name']
                    _file_name = IARConverter._process_path(_file_name, prj_file_rel_path)
                    prj_desc['files'].append(IARConverter._get_file_info(_file_name))

        # ---------------- 如果output_file不为None, 返回工程描述yaml对象 ----------------
        if output_file != '':
            f = open(output_file, 'w')
            self._yml.dump(prj_desc, f)
            f.close()

        return prj_desc
