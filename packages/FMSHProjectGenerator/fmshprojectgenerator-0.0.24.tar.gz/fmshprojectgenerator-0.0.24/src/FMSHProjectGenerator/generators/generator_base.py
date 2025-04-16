class Generator:
    # 生成工程抽象接口
    def generate(self, prj_info, target_info, prj_path, version, **kwargs):
        pass

    # 获取生成工程的名称
    def project_filepath(self, prj_info, prj_path) -> str:
        pass
