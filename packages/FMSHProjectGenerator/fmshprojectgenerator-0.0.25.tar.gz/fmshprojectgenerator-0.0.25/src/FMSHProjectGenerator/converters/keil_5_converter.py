import os.path
import re
from copy import deepcopy

import chardet
import xmltodict

from FMSHProjectGenerator.converters import Converter, FileFormatError


class Keil5Converter(Converter):
    # 文件类型定义
    __file_types = {
        '1': 'C',
        '2': 'ASM',
        '3': 'OBJ',
        '4': 'LIB',
        '5': 'TEXT',
        '6': 'CUSTOM',
        '7': 'CPP',
        '8': 'IMAGE',
    }

    # 优化定义(optimize, optimize_hint, keil_use_optimize_hint)
    __optimizes = {
        '0': ('none', 'size', False),
        '1': ('none', 'size', False),
        '2': ('low', 'size', False),
        '3': ('medium', 'size', False),
        '4': ('high', 'size', False),
        '5': ('high', 'speed', True),
        '6': ('high', 'balanced', True),
        '7': ('high', 'size', True),
    }

    # 警告定义
    __warnings = {
        '1': 'no warnings',
        '2': 'all warnings',
        '3': 'ac5-like warnings',
        '4': 'misra compatible',
    }

    # 复位定义
    __reset_vals = {
        '0': 'normal',
        '1': 'core',
        '2': 'reset pin',
    }

    # AC6 C版本定义
    __ac6_c_lang = {
        '1': 'c90',
        '2': 'gnu90',
        '3': 'c99',
        '4': 'gnu99',
        '5': 'c11',
        '6': 'gnu11',
    }

    # AC6 C++版本定义
    __ac6_cpp_lang = {
        '1': 'c++98',
        '2': 'gnu++98',
        '3': 'c++11',
        '4': 'gnu++11',
        '5': 'c++03',
        '6': 'c++14',
        '7': 'gnu++14',
        '8': 'c++17',
        '9': 'gnu++17',
    }

    # 仿真器配置
    __debugger = {
        '0': 'UL2CM3',  # Currently not supported
        '1': 'ULP2CM3',  # Currently not supported
        '2': 'ULPL2CM3',  # Currently not supported
        '3': 'CMSIS_AGDI',  # CMSIS-DAP(Below ARM-V8M)
        '4': 'JL2CM3',  # JLink
        '6': 'ST-LINKIII-KEIL_SWO',  # Currently not supported
        '14': 'CMSIS_AGDI_V8M',  # CMSIS-DAP(ARM-V8M)
    }

    def __init__(self):
        super().__init__()

    def project_requirement(self):
        # KEIL 5 工程文件字典
        return {'uvprojx': None, 'uvoptx': None}

    def analyze_project(self, prj_files: dict, target_name: str = '', output_file: str = '') -> dict:
        # 检查工程文件配置有效性
        if 'uvprojx' not in prj_files.keys() or prj_files['uvprojx'] is None or \
                not isinstance(prj_files['uvprojx'], tuple):
            raise FileNotFoundError('Keil 5 project file(*.uvprojx) not found!')

        if 'uvoptx' not in prj_files.keys() or prj_files['uvoptx'] is None or \
                not isinstance(prj_files['uvoptx'], tuple):
            raise FileNotFoundError('Keil 5 project options file(*.uvoptx) not found!')

        # 记录工程文件相对生成工程目录路径（注意：生成工程目录总是根目录的一级子目录）
        prj_file_rel_path = os.path.join('..', prj_files['uvprojx'][1])

        # ---------------- 加载工程描述文件模板 ----------------
        prj_desc = self.load_template(self)

        # ---------------- 加载工程 ----------------
        # 读取工程文件
        with open(prj_files['uvprojx'][0], 'rb') as f:  # 先用二进制打开以获取编码
            data = f.read()  # 读取文件内容
            file_encoding = chardet.detect(data)['encoding']  # 得到文件的编码格式
        try:
            with open(prj_files['uvprojx'][0], 'r', encoding=file_encoding) as f:  # 文本模式打开
                project_xml = f.read()
        except UnicodeDecodeError:
            # 有时chardet会检测出错，此时我们使用UTF-8编码重试，此时失败将抛出错误
            with open(prj_files['uvprojx'][0], 'r', encoding='utf-8') as f:  # 文本模式打开
                project_xml = f.read()

        project = xmltodict.parse(project_xml, force_list=('Target', 'File', 'Group'))

        # 读取工程选项文件
        with open(prj_files['uvoptx'][0], 'rb') as f:  # 先用二进制打开以获取编码
            data = f.read()  # 读取文件内容
            file_encoding = chardet.detect(data)['encoding']  # 得到文件的编码格式
        try:
            with open(prj_files['uvoptx'][0], 'r', encoding=file_encoding) as f:  # 文本模式打开
                opt_xml = f.read()
        except UnicodeDecodeError:
            # 有时chardet会检测出错，此时我们使用UTF-8编码重试，此时失败将抛出错误
            with open(prj_files['uvoptx'][0], 'r', encoding='utf-8') as f:  # 文本模式打开
                opt_xml = f.read()
        project_opt = xmltodict.parse(opt_xml, force_list=('Target', 'SetRegEntry'))

        # ---------------- 寻找target对象 ----------------
        # 注意：通过target_name参数指定target，如果target_name为空串，默认选择第一个target
        target_obj = None
        target_obj_opt = None

        if target_name != '':
            for target in project['Project']['Targets']['Target']:
                if target['TargetName'] == target_name:
                    target_obj = target
                    break
            for target in project_opt['ProjectOpt']['Target']:
                if target['TargetName'] == target_name:
                    target_obj_opt = target
                    break
            if target_obj is None:
                raise FileFormatError("target " + target_name + " not found")
            elif target_obj_opt is None:
                raise FileFormatError("target " + target_name + " options not found")
        else:
            if project['Project']['Targets'] is None or \
                    project_opt['ProjectOpt'] is None:
                raise FileFormatError('no target in given project file')
            target_obj = project['Project']['Targets']['Target'][0]
            target_obj_opt = project_opt['ProjectOpt']['Target'][0]
            target_name = target_obj['TargetName']

        # ---------------- 加载芯片配置文件 ----------------
        target_chip_name = target_obj['TargetOption']['TargetCommonOption']['Device']
        target_chip_name = str.upper(target_chip_name)
        target_chip = self.load_chip(target_chip_name)

        # ---------------- 生成工程描述yaml对象 ----------------
        # 工程名称
        prj_desc['name'] = target_name

        # 工程目标
        prj_desc['target'] = target_chip_name

        # 工程选项
        # —— Target: Compiler
        try:
            prj_desc['options']['keil_compiler'] = 'v6' if \
                target_obj['uAC6'] == '1' else 'v5'  # default to AC5, keil will autocorrect it if ac5 is unavailable
        except KeyError:
            print('Target has no \'Compiler\' option, default to AC5')
            prj_desc['options']['keil_compiler'] = 'v5'

        # —— Target: Use MicroLIB
        try:
            prj_desc['options']['keil_micro_lib'] = True if target_obj['TargetOption']['TargetArmAds']['ArmAdsMisc'][
                                                                'useUlib'] == '1' else False
        except KeyError:
            print('Target has no \'Use MicroLIB\' option, default to false')
            prj_desc['options']['keil_micro_lib'] = False

        # —— C/C++(Using AC5): C99 Mode
        try:
            prj_desc['options']['c_version'] = 'c99' if \
                target_obj['TargetOption']['TargetArmAds']['Cads']['uC99'] == '1' else 'c90'
        except KeyError:
            if prj_desc['options']['keil_compiler'] == 'v5':
                # Show when AC5 is used
                print('Target has no \'C99 Mode\' option, default to c90')
            prj_desc['options']['c_version'] = 'c90'

        # —— C/C++(Using AC6): Language C (Version)
        c_ver = '1'  # default c90
        try:
            c_ver = target_obj['TargetOption']['TargetArmAds']['Cads']['v6Lang']
        except KeyError:
            if prj_desc['options']['keil_compiler'] == 'v6':
                # Show when AC6 is used
                print('Target has no \'Language C\' option, default to c90')
        if c_ver in self.__ac6_c_lang:
            prj_desc['options']['c_version'] = self.__ac6_c_lang[c_ver]

        # —— C/C++(Using AC6): Language C++ (Version)
        cpp_ver = '2'  # default c++11
        try:
            cpp_ver = target_obj['TargetOption']['TargetArmAds']['Cads']['v6LangP']
        except KeyError:
            if prj_desc['options']['keil_compiler'] == 'v6':
                # Show when AC6 is used
                print('Target has no \'Language C++\' option, default to c++11')
        if cpp_ver in self.__ac6_cpp_lang:
            prj_desc['options']['cpp_version'] = self.__ac6_cpp_lang[cpp_ver]

        # —— C/C++: Optimization
        try:
            optimize_lvl = target_obj['TargetOption']['TargetArmAds']['Cads']['Optim']
        except KeyError:
            print('Target has no \'Optimization\' option, default to 0(No Optimization)')
            optimize_lvl = 0
        prj_desc['options']['optimize'], \
        prj_desc['options']['optimize_hint'], \
        prj_desc['options']['keil_use_optimize_hint'] = self.__optimizes[optimize_lvl]

        # —— C/C++: Warnings
        try:
            warning_lvl = target_obj['TargetOption']['TargetArmAds']['Cads']['wLevel']
        except KeyError:
            print('Target has no \'Warnings\' option, default to 1(No Warnings)')
            warning_lvl = 1
        if warning_lvl in self.__warnings:
            prj_desc['options']['keil_warning'] = self.__warnings[warning_lvl]

        # 工程高级选项 —— linker script file(*.sct)
        try:
            if target_obj['TargetOption']['TargetArmAds']['LDads']['umfTarg'] == '0':
                if 'ScatterFile' in target_obj['TargetOption']['TargetArmAds']['LDads']:
                    prj_desc['advanced_options']['keil_linker_cfg'] = \
                        target_obj['TargetOption']['TargetArmAds']['LDads']['ScatterFile']
        except KeyError:
            pass

        # 调试工具
        try:
            debug_tool_flag = False
            debug_tool_sel = target_obj_opt['TargetOption']['DebugOpt']['nTsel']
            for item in target_obj_opt['TargetOption']['TargetDriverDllRegistry']['SetRegEntry']:
                if item['Key'] == self.__debugger[debug_tool_sel]:
                    debug_tool_flag = True
                    break
            if not debug_tool_flag:
                print('Target has invalid \'Debug Tool\' Option, default to JLink')
                debug_tool_sel = '4'
        except KeyError:
            print('Target has no \'Debug Tool\' Option, default to JLink')
            debug_tool_sel = '4'

        # JLink ---------------------------------------------------------------
        if debug_tool_sel == '4':
            prj_desc['debug']['tool'] = 'jlink'

            # 获取 JLink 配置
            jlink_opt = None
            try:
                for item in target_obj_opt['TargetOption']['TargetDriverDllRegistry']['SetRegEntry']:
                    if item['Key'] == 'JL2CM3':
                        jlink_opt = item['Name']
                        break
            except KeyError:
                pass

            if jlink_opt is None:
                print('debug tool not supported, relevant settings will remain default')
            else:
                # 连接选项 --------------------------------------------------------
                jlink_opt_itf = re.search('-O([0-9]*)', jlink_opt).group(1)
                jlink_opt_itf = int(jlink_opt_itf) - 6
                # 接口类型
                if jlink_opt_itf & (0b1 << 6) == 0:
                    prj_desc['debug']['interface'] = 'JTAG'
                else:
                    prj_desc['debug']['interface'] = 'SWD'
                # 连接
                if jlink_opt_itf & (0b11 << 10) == (0b00 << 10):
                    prj_desc['debug']['connect'] = 'normal'
                elif jlink_opt_itf & (0b11 << 10) == (0b01 << 10):
                    prj_desc['debug']['connect'] = 'with pre-reset'
                elif jlink_opt_itf & (0b11 << 10) == (0b10 << 10):
                    prj_desc['debug']['connect'] = 'under reset'
                else:
                    print('JLink connect type not supported, relevant settings will remain default')

                # JLink 接口速率
                jlink_opt_spd = re.search('-ZTIFSpeedSel([0-9]*)', jlink_opt).group(1)
                prj_desc['debug']['speed'] = int(jlink_opt_spd)

                # JLink 接口复位
                jlink_opt_rst = re.search('-RST([0-9]*)', jlink_opt).group(1)
                if jlink_opt_rst in self.__reset_vals:
                    prj_desc['debug']['reset'] = self.__reset_vals[jlink_opt_rst]
                else:
                    print('JLink reset type not supported, relevant settings will remain default')

                # 烧写选项
                try:
                    jlink_dl_opt = int(re.search('-FO([0-9]*)', jlink_opt).group(1))
                    prj_desc['debug']['download']['program'] = bool(jlink_dl_opt & (0b01 << 1) == (0b01 << 1))
                    prj_desc['debug']['download']['verify'] = bool(jlink_dl_opt & (0b01 << 2) == (0b01 << 2))
                    prj_desc['debug']['download']['reset-run'] = bool(jlink_dl_opt & (0b01 << 3) == (0b01 << 3))
                    jlink_dl_opt = jlink_dl_opt & ~0b01110  # 去除标志位
                    dl_erase_index = {
                        17: 'full chip',
                        1: 'sectors',
                        0: 'none',
                    }
                    if jlink_dl_opt in dl_erase_index:
                        prj_desc['debug']['download']['erase'] = dl_erase_index[jlink_dl_opt]
                    else:
                        print("JLink erase type not supported, default to \'erase sectors\'")
                        prj_desc['debug']['download']['erase'] = 'sectors'
                except IndexError:
                    print("JLink download option not found, use default value")
                    prj_desc['debug']['download']['erase'] = 'sectors'
                    prj_desc['debug']['download']['program'] = True
                    prj_desc['debug']['download']['verify'] = True
                    prj_desc['debug']['download']['reset-run'] = True

                # 工程高级选项 —— flasher configuration
                jlink_opt_fls = re.findall(
                    '-FF[0-9]([0-9a-zA-Z_]*)(.FLM)? -FS[0-9]([0-9]*) -FL[0-9]([0-9]*)( -FP[0-9]\(\$\$Device:[\S]+\$([\S]+)\))?',
                    jlink_opt)

                if jlink_opt_fls is not None:
                    for fls_name, fls_ext, fls_base, fls_size, _, fls_path in jlink_opt_fls:
                        fls_path = fls_path.replace('\\', '/')
                        fls_algo = dict(name=fls_name + fls_ext, path=fls_path if fls_path != '' else None,
                                        base=fls_base,
                                        size=fls_size)
                        if fls_algo not in target_chip['target']['keil_5_flash_algorithms']:
                            if prj_desc['advanced_options']['keil_flasher_cfg'] is None:
                                prj_desc['advanced_options']['keil_flasher_cfg'] = list()
                            prj_desc['advanced_options']['keil_flasher_cfg'].append(fls_algo)

        # CMSIS-DAP(Below ARM-V8M) --------------------------------------------
        elif debug_tool_sel == '3':
            prj_desc['debug']['tool'] = 'cmsis-dap'

            # 获取 CMSIS-DAP 配置
            dap_opt = None
            try:
                for item in target_obj_opt['TargetOption']['TargetDriverDllRegistry']['SetRegEntry']:
                    if item['Key'] == 'CMSIS_AGDI':
                        dap_opt = item['Name']
                        break
            except KeyError:
                pass

            if dap_opt is None:
                print('debug tool not supported, relevant settings will remain default')
            else:
                # 连接选项 --------------------------------------------------------
                dap_opt_itf = re.search('-O([0-9]*)', dap_opt).group(1)
                dap_opt_itf = int(dap_opt_itf) - 398
                # 接口类型
                if dap_opt_itf & (0b1 << 6) == 0:
                    prj_desc['debug']['interface'] = 'JTAG'
                else:
                    prj_desc['debug']['interface'] = 'SWD'
                # 连接
                if dap_opt_itf & (0b11 << 10) == (0b00 << 10):
                    prj_desc['debug']['connect'] = 'normal'
                elif dap_opt_itf & (0b11 << 10) == (0b01 << 10):
                    prj_desc['debug']['connect'] = 'with pre-reset'
                elif dap_opt_itf & (0b11 << 10) == (0b10 << 10):
                    prj_desc['debug']['connect'] = 'under reset'
                else:
                    print('JLink connect type not supported, relevant settings will remain default')
                # 复位
                if dap_opt_itf & (0b11 << 8) == (0b00 << 8):
                    prj_desc['debug']['reset'] = 'reset pin'
                elif dap_opt_itf & (0b11 << 8) == (0b01 << 8):
                    prj_desc['debug']['reset'] = 'normal'
                elif dap_opt_itf & (0b11 << 8) == (0b10 << 8):
                    prj_desc['debug']['reset'] = 'core'
                else:
                    print('JLink reset type not supported, relevant settings will remain default')

                # JLink 接口速率
                dap_opt_spd = re.search('-S([0-9]*)', dap_opt).group(1)
                dap_speed_index = {
                    8: 10000,
                    9: 5000,
                    10: 2000,
                    0: 1000,
                    1: 500,
                    2: 200,
                    3: 100,
                    4: 50,
                    5: 20,
                    6: 10,
                    7: 5,
                }
                if int(dap_opt_spd) in dap_speed_index:
                    prj_desc['debug']['speed'] = dap_speed_index[int(dap_opt_spd)]
                else:
                    print('CMSIS-DAP speed not supported, default to 10M')
                    prj_desc['debug']['speed'] = 8

                # 烧写选项
                try:
                    dap_dl_opt = int(re.search('-FO([0-9]*)', dap_opt).group(1))
                    prj_desc['debug']['download']['program'] = bool(int(dap_dl_opt) & (0b01 << 1) == (0b01 << 1))
                    prj_desc['debug']['download']['verify'] = bool(int(dap_dl_opt) & (0b01 << 2) == (0b01 << 2))
                    prj_desc['debug']['download']['reset-run'] = bool(int(dap_dl_opt) & (0b01 << 3) == (0b01 << 3))
                    dap_dl_opt = dap_dl_opt & ~0b01110  # 去除标志位
                    dl_erase_index = {
                        17: 'full chip',
                        1: 'sectors',
                        0: 'none',
                    }
                    if dap_dl_opt in dl_erase_index:
                        prj_desc['debug']['download']['erase'] = dl_erase_index[dap_dl_opt]
                    else:
                        print("CMSIS-DAP erase type not supported, default to \'erase sectors\'")
                        prj_desc['debug']['download']['erase'] = 'sectors'
                except IndexError:
                    print("CMSIS-DAP download option not found, use default value")
                    prj_desc['debug']['download']['erase'] = 'sectors'
                    prj_desc['debug']['download']['program'] = True
                    prj_desc['debug']['download']['verify'] = True
                    prj_desc['debug']['download']['reset-run'] = True

                # 工程高级选项 —— flasher configuration
                dap_opt_fls = re.findall(
                    '-FF[0-9]([0-9a-zA-Z_]*)(.FLM)? -FS[0-9]([0-9]*) -FL[0-9]([0-9]*)( -FP[0-9]\(\$\$Device:[\S]+\$([\S]+)\))?',
                    dap_opt)

                if dap_opt_fls is not None:
                    for fls_name, fls_ext, fls_base, fls_size, _, fls_path in dap_opt_fls:
                        fls_algo = dict(name=fls_name + fls_ext, path=fls_path if fls_path != '' else None,
                                        base=fls_base,
                                        size=fls_size)
                        if fls_algo not in target_chip['target']['keil_5_flash_algorithms']:
                            if prj_desc['advanced_options']['keil_flasher_cfg'] is None:
                                prj_desc['advanced_options']['keil_flasher_cfg'] = list()
                            prj_desc['advanced_options']['keil_flasher_cfg'].append(fls_algo)

        # CMSIS-DAP(ARM-V8M) --------------------------------------------
        elif debug_tool_sel == '14':
            prj_desc['debug']['tool'] = 'cmsis-dap'

            # 获取 CMSIS-DAP 配置
            dap_opt = None
            try:
                for item in target_obj_opt['TargetOption']['TargetDriverDllRegistry']['SetRegEntry']:
                    if item['Key'] == 'CMSIS_AGDI_V8M':
                        dap_opt = item['Name']
                        break
            except KeyError:
                pass

            if dap_opt is None:
                print('debug tool not supported, relevant settings will remain default')
            else:
                # 连接选项 --------------------------------------------------------
                dap_opt_itf = re.search('-O([0-9]*)', dap_opt).group(1)
                dap_opt_itf = int(dap_opt_itf) - 398
                # 接口类型
                if dap_opt_itf & (0b1 << 6) == 0:
                    prj_desc['debug']['interface'] = 'JTAG'
                else:
                    prj_desc['debug']['interface'] = 'SWD'
                # 连接
                if dap_opt_itf & (0b11 << 10) == (0b00 << 10):
                    prj_desc['debug']['connect'] = 'normal'
                elif dap_opt_itf & (0b11 << 10) == (0b01 << 10):
                    prj_desc['debug']['connect'] = 'with pre-reset'
                elif dap_opt_itf & (0b11 << 10) == (0b10 << 10):
                    prj_desc['debug']['connect'] = 'under reset'
                else:
                    print('JLink connect type not supported, relevant settings will remain default')
                # 复位
                if dap_opt_itf & (0b11 << 8) == (0b00 << 8):
                    prj_desc['debug']['reset'] = 'reset pin'
                elif dap_opt_itf & (0b11 << 8) == (0b01 << 8):
                    prj_desc['debug']['reset'] = 'normal'
                elif dap_opt_itf & (0b11 << 8) == (0b10 << 8):
                    prj_desc['debug']['reset'] = 'core'
                else:
                    print('JLink reset type not supported, relevant settings will remain default')

                # JLink 接口速率
                dap_opt_spd = re.search('-S([0-9]*)', dap_opt).group(1)
                dap_speed_index = {
                    8: 10000,
                    9: 5000,
                    10: 2000,
                    0: 1000,
                    1: 500,
                    2: 200,
                    3: 100,
                    4: 50,
                    5: 20,
                    6: 10,
                    7: 5,
                }
                if int(dap_opt_spd) in dap_speed_index:
                    prj_desc['debug']['speed'] = dap_speed_index[int(dap_opt_spd)]
                else:
                    print('CMSIS-DAP speed not supported, default to 10M')
                    prj_desc['debug']['speed'] = 8

                # 烧写选项
                try:
                    dap_dl_opt = int(re.search('-FO([0-9]*)', dap_opt).group(1))
                    prj_desc['debug']['download']['program'] = bool(
                        int(dap_dl_opt) & (0b01 << 1) == (0b01 << 1))
                    prj_desc['debug']['download']['verify'] = bool(int(dap_dl_opt) & (0b01 << 2) == (0b01 << 2))
                    prj_desc['debug']['download']['reset-run'] = bool(
                        int(dap_dl_opt) & (0b01 << 3) == (0b01 << 3))
                    dap_dl_opt = dap_dl_opt & ~0b01110  # 去除标志位
                    dl_erase_index = {
                        17: 'full chip',
                        1: 'sectors',
                        0: 'none',
                    }
                    if dap_dl_opt in dl_erase_index:
                        prj_desc['debug']['download']['erase'] = dl_erase_index[dap_dl_opt]
                    else:
                        print("CMSIS-DAP erase type not supported, default to \'erase sectors\'")
                        prj_desc['debug']['download']['erase'] = 'sectors'
                except IndexError:
                    print("CMSIS-DAP download option not found, use default value")
                    prj_desc['debug']['download']['erase'] = 'sectors'
                    prj_desc['debug']['download']['program'] = True
                    prj_desc['debug']['download']['verify'] = True
                    prj_desc['debug']['download']['reset-run'] = True

                # 工程高级选项 —— flasher configuration
                dap_opt_fls = re.findall(
                    '-FF[0-9]([0-9a-zA-Z_]*)(.FLM)? -FS[0-9]([0-9]*) -FL[0-9]([0-9]*)( -FP[0-9]\(\$\$Device:[\S]+\$([\S]+)\))?',
                    dap_opt)

                if dap_opt_fls is not None:
                    for fls_name, fls_ext, fls_base, fls_size, _, fls_path in dap_opt_fls:
                        fls_algo = dict(name=fls_name + fls_ext, path=fls_path if fls_path != '' else None,
                                        base=fls_base,
                                        size=fls_size)
                        if fls_algo not in target_chip['target']['keil_5_flash_algorithms']:
                            if prj_desc['advanced_options']['keil_flasher_cfg'] is None:
                                prj_desc['advanced_options']['keil_flasher_cfg'] = list()
                            prj_desc['advanced_options']['keil_flasher_cfg'].append(fls_algo)

        # 不支持的仿真器 ---------------------------------------------------------
        else:
            print('Debugger not supported, default to JLink')

        # 编译器全局定义
        try:
            defines = target_obj['TargetOption']['TargetArmAds']['Cads']['VariousControls']['Define']
            if defines is not None:
                define_list = str.split(defines, ",")
                for define in define_list:
                    if define in target_chip['defines']:
                        define_list.remove(define)
                prj_desc['defines'] = define_list
            else:
                prj_desc['defines'] = []
        except KeyError:
            print('Target has no \'Defines\', default to an empty list')
            prj_desc['defines'] = []

        # 包含路径
        prj_desc['includePaths'] = []
        try:
            includes = target_obj['TargetOption']['TargetArmAds']['Cads']['VariousControls']['IncludePath']
            if includes is not None:
                include_list = str.split(includes, ';')
                tmp_includes = include_list
            else:
                tmp_includes = []
        except KeyError:
            print('Target has no \'Includes\', default to an empty list')
            tmp_includes = []
        for include in tmp_includes:
            # 转换路径
            if not os.path.isabs(include):
                prj_desc['includePaths'].append(Converter.translate_path(include, prj_file_rel_path))
            elif include.startswith('$TOOLKIT_DIR$'):
                continue    # 屏蔽IAR特殊路径
            else:
                prj_desc['includePaths'].append(include)

        # 编译器全局定义(ASM)
        try:
            defines = target_obj['TargetOption']['TargetArmAds']['Aads']['VariousControls']['Define']
            if defines is not None:
                define_list = str.split(defines, ",")
                for define in define_list:
                    if define in target_chip['defines']:
                        define_list.remove(define)
                prj_desc['definesASM'] = define_list
            else:
                prj_desc['definesASM'] = []
        except KeyError:
            print('Target has no \'Defines(ASM)\', default to an empty list')
            prj_desc['definesASM'] = []

        # 包含路径(ASM)
        prj_desc['includePathsASM'] = []
        try:
            includes = target_obj['TargetOption']['TargetArmAds']['Aads']['VariousControls']['IncludePath']
            if includes is not None:
                include_list = str.split(includes, ';')
                tmp_includes = include_list
            else:
                tmp_includes = []
        except KeyError:
            print('Target has no \'Includes(ASM)\', default to an empty list')
            tmp_includes = []
        for include in tmp_includes:
            # 转换路径
            if include.startswith('$TOOLKIT_DIR$'):
                continue    # 屏蔽IAR特殊路径
            if not os.path.isabs(include):
                prj_desc['includePathsASM'].append(Converter.translate_path(include, prj_file_rel_path))
            else:
                prj_desc['includePathsASM'].append(include)

        # 文件组
        prj_desc['groups'] = list()
        try:
            groups = target_obj['Groups']['Group']
        except KeyError:
            print('Target has no \'File Groups\', default to an empty list')
            groups = []

        for group in groups:
            parent_dir_obj = prj_desc
            group_name = group['GroupName']

            # 确定当前组的父对象（根下的组父对象为根对象）
            if str.find(group['GroupName'], '/') != -1 or str.find(group['GroupName'], '\\') != -1:
                # 该文件组为子文件组
                group_dir = str.replace(group['GroupName'], '\\', '/')
                parent_dir = str.split(group_dir, '/')[:-1]
                group_name = str.split(group_dir, '/')[-1]

                # 寻找父目录对象（不存在则自动添加）
                for p_dir in parent_dir:
                    group_exist_flag = False
                    if parent_dir_obj['groups'] is None:
                        parent_dir_obj['groups'] = list()
                    for project_group in parent_dir_obj['groups']:
                        if project_group['name'] == p_dir:
                            parent_dir_obj = project_group
                            group_exist_flag = True
                            break

                    # 不存在该父目录，进行创建
                    if not group_exist_flag:
                        tmp_group = dict(name=p_dir, files=None, groups=None)
                        if parent_dir_obj['groups'] is None:
                            parent_dir_obj['groups'] = list()
                        parent_dir_obj['groups'].append(tmp_group)
                        parent_dir_obj = tmp_group

            # 创建组
            self_obj = dict(name=group_name, files=None, groups=None)

            # 添加文件到组
            if 'Files' in group and group['Files'] is not None:
                for file in group['Files']['File']:
                    if self_obj['files'] is None:
                        self_obj['files'] = list()
                    f_name = file['FileName']
                    f_type = 'TEXT'
                    if file['FileType'] in self.__file_types:
                        f_type = self.__file_types[file['FileType']]
                    f_path = file['FilePath']
                    if f_path.startswith('$TOOLKIT_DIR$'):
                        continue    # 屏蔽IAR特殊路径文件
                    if not os.path.isabs(f_path):  # 路径转换
                        f_path = Converter.translate_path(f_path, prj_file_rel_path)
                    self_obj['files'].append(dict(name=f_name, type=f_type, path=f_path))

            # 添加组到父对象
            if parent_dir_obj['groups'] is None:
                parent_dir_obj['groups'] = list()
            parent_dir_obj['groups'].append(self_obj)

        # 处理工程根目录文件（$$ROOT$$组）
        for group in prj_desc['groups']:
            if group['name'] == '$$ROOT$$':
                prj_desc['files'] = deepcopy(group['files'])
                prj_desc['groups'].remove(group)
                break

        # ---------------- 如果output_file不为None, 返回工程描述yaml对象 ----------------
        if output_file != '':
            f = open(output_file, 'w')
            self._yml.dump(prj_desc, f)
            f.close()

        return prj_desc
