import os
from enum import Enum, unique

from jinja2 import Environment, FileSystemLoader, select_autoescape

from FMSHProjectGenerator.converters import IARConverter
from FMSHProjectGenerator.generators import Generator


# IAR 版本定义
@unique
class IARVersionType(Enum):
    V7 = 1  # IAR V7.50测试正常，也适用于其他V7.x版本，但是有可能报“broken option“错误，不影响使用
    V8_32 = 2  # IAR V8.32测试正常，也适用于其他V8.x版本，但是有可能报“broken option“错误，不影响使用


# Additional template tests
def is_abspath(path: str):
    return os.path.isabs(path)


def is_toolkit_path(path: str):
    return path.startswith('$TOOLKIT_DIR$')


class IARGenerator(Generator):
    # Jinja2环境
    __env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def __init__(self):
        # 添加自定义测试
        self.__env.tests['abspath'] = is_abspath
        self.__env.tests['toolkit_path'] = is_toolkit_path

    @staticmethod
    def combine_files(base_files: list, append_files: list):
        if append_files is None:
            return
        if len(append_files) != 0:
            for append_file in append_files:
                find_flag = False
                for base_file in base_files:
                    if base_file['name'] == append_file['name']:
                        find_flag = True
                        break
                if not find_flag:
                    base_files.append(append_file)

    def combine_groups(self, base_groups: list, append_groups: list):
        if base_groups is None or append_groups is None:
            return
        if len(append_groups) != 0:
            for append_group in append_groups:
                # 在基础组中寻找是否已经有相同组
                find_flag = False
                for base_group in base_groups:
                    # 有相同组，合并这两组的文件，并递归合并子组
                    if base_group['name'] == append_group['name']:
                        find_flag = True
                        # 用户可通过在生成group列表中添加'overwrite'=True禁止合并
                        if 'overwrite' in base_group and base_group['overwrite']:
                            break
                        if 'files' in append_group and append_group['files'] is not None:
                            if 'files' not in base_group:
                                base_group['files'] = []
                            self.combine_files(base_group['files'], append_group['files'])
                        if 'groups' in append_group:
                            if 'groups' not in base_group:
                                base_group['groups'] = []
                            self.combine_groups(base_group['groups'], append_group['groups'])
                        break

                # 没有相同组，直接将该组插入
                if not find_flag:
                    base_groups.append(append_group)

    # 生成工程接口
    def generate(self, prj_info, target_info, prj_path, version: IARVersionType, **kwargs):
        """
        生成IAR工程。
        可选参数：
        1. combine：默认False。控制生成的工程是否与前一次工程进行合并。
        """
        # 设定配置 ---------------------------------------------
        __combine = False
        if 'combine' in kwargs and kwargs['combine'] is True:
            __combine = True

        # --------------------- 路径处理 -----------------------
        # 项目文件路径
        prj_file_path = os.path.join(prj_path, 'EWARM')

        # 检查路径是否存在
        if not os.path.exists(prj_file_path):
            os.makedirs(prj_file_path)
        if not os.path.exists(os.path.join(prj_file_path, 'settings')):
            os.makedirs(os.path.join(prj_file_path, 'settings'))

        # ----------- 检查工程文件是否需要修改target配置 -----------
        # 检查工程是否需要覆盖默认的链接配置文件
        if prj_info['advanced_options']['iar_linker_cfg'] is not None:
            target_info['iar_linker_cfg'] = prj_info['advanced_options']['iar_linker_cfg']

        # 检查工程是否需要覆盖默认的烧写配置文件
        if prj_info['advanced_options']['iar_flasher_cfg'] is not None:
            target_info['iar_flasher_cfg'] = prj_info['advanced_options']['iar_flasher_cfg']

        # 合并工程文件中的文件组、预处理宏定义和包含路径 ---------------
        if __combine:
            # 检查是否已经存在工程文件（*.uvprojx）和选项文件（*.uvoptx）
            f_prj_name = os.path.join(prj_file_path, prj_info['name'] + ".ewp")
            f_opt_name = os.path.join(prj_file_path, prj_info['name'] + ".ewd")
            if os.path.exists(f_prj_name) and os.path.exists(f_opt_name):
                # 读取工程和选项并进行合并
                if version in [IARVersionType.V7, IARVersionType.V8_32]:
                    cvt = IARConverter()
                    cvt_desc = cvt.analyze_project({'ewp': (f_prj_name, './EWARM'),
                                                    'ewd': (f_opt_name, './EWARM')})
                    # 合并预处理宏定义
                    prj_info['defines'] = list(set(prj_info['defines'] + cvt_desc['defines']))
                    prj_info['definesASM'] = list(set(prj_info['definesASM'] + cvt_desc['definesASM']))
                    # 合并包含路径
                    prj_info['includePaths'] = list(set(prj_info['includePaths'] + cvt_desc['includePaths']))
                    prj_info['includePathsASM'] = list(
                        set(prj_info['includePathsASM'] + cvt_desc['includePathsASM']))
                    # 合并工程组
                    self.combine_groups(prj_info['groups'], cvt_desc['groups'])

        # -------------------- 生成工程文件 ---------------------
        # IAR 8.32
        if version == IARVersionType.V8_32:
            # IAR 8.32 工作空间文件(*.eww)
            tpl = self.__env.get_template('iar_8_32_eww.xml')
            eww_name = 'Project.eww'
            with open(os.path.join(prj_file_path, eww_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 8.32 工程文件(*.ewp)
            tpl = self.__env.get_template('iar_8_32_ewp.xml')
            ewp_name = prj_info['name'] + '.ewp'
            with open(os.path.join(prj_file_path, ewp_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 8.32 工程调试选项文件(*.ewd)
            tpl = self.__env.get_template('iar_8_32_ewd.xml')
            ewd_name = prj_info['name'] + '.ewd'
            with open(os.path.join(prj_file_path, ewd_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 8.32 JLink 配置文件(*.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                jlink_setting_name = prj_info['name'] + '_' + prj_info['name'] + '.jlink'
                tpl = self.__env.get_template('iar_8_32_jlink_setting.ini')
                with open(os.path.join(prj_file_path, 'settings', jlink_setting_name), mode='w', encoding='utf-8') as f:
                    f.write(tpl.render(target=target_info))

        # IAR 7
        elif version == IARVersionType.V7:
            # IAR 7 工作空间文件(*.eww)
            tpl = self.__env.get_template('iar_7_eww.xml')
            eww_name = 'Project.eww'
            with open(os.path.join(prj_file_path, eww_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 7 工程文件(*.ewp)
            tpl = self.__env.get_template('iar_7_ewp.xml')
            ewp_name = prj_info['name'] + '.ewp'
            f = open(os.path.join(prj_file_path, ewp_name), mode='w', encoding='utf-8')
            f.write(tpl.render(project=prj_info, target=target_info))
            f.close()

            # IAR 7 工程调试选项文件(*.ewd)
            tpl = self.__env.get_template('iar_7_ewd.xml')
            ewd_name = prj_info['name'] + '.ewd'
            with open(os.path.join(prj_file_path, ewd_name), mode='w', encoding='utf-8') as f:
                f.write(tpl.render(project=prj_info, target=target_info))

            # IAR 7 JLink 配置文件(*.ini)
            if str.lower(prj_info['debug']['tool']) == 'jlink':
                jlink_setting_name = prj_info['name'] + '_' + prj_info['name'] + '.jlink'
                tpl = self.__env.get_template('iar_7_jlink_setting.ini')
                with open(os.path.join(prj_file_path, 'settings', jlink_setting_name), mode='w', encoding='utf-8') as f:
                    f.write(tpl.render(target=target_info))

    # 获取生成工程的名称
    def project_filepath(self, prj_info, prj_path) -> str:
        filename = 'Project.eww'
        return os.path.join(prj_path, 'EWARM', filename)
