from FMSHProjectGenerator import ProjectGenerator
from FMSHProjectGenerator.converters import Keil5Converter, IARConverter
from FMSHProjectGenerator.generators import IARGenerator, IARVersionType, Keil5Generator, Keil5VersionType
import os
import click

AVAILABLE_CONVERTERS = {
    'Keil5': Keil5Converter,
    'IAR': IARConverter,
}

AVAILABLE_GENERATORS = {
    'Keil5': Keil5VersionType.V5,
    'Keil5_27': Keil5VersionType.V5_27,
    'Keil5_32': Keil5VersionType.V5_32,
    'IAR7': IARVersionType.V7,
    'IAR8_32': IARVersionType.V8_32,
}


@click.group()
def fmshproject():
    pass


@fmshproject.command('convert')
@click.argument('project_path', type=click.Path(exists=True))
@click.argument('src_type', type=click.Choice(list(AVAILABLE_CONVERTERS.keys())))
@click.argument('dst_type', type=click.Choice(list(AVAILABLE_GENERATORS.keys())))
# TODO: optional configuration file(.json)
def convert(project_path, src_type, dst_type):
    # create an instance
    proj_gen = ProjectGenerator()
    # convert source project to project description file
    proj_gen.convert(src_prj_path=project_path,
                     converter=AVAILABLE_CONVERTERS[src_type](),
                     output_file=os.path.join(project_path, 'project.yaml'))
    # convert project description file to destination project
    if dst_type.startswith('Keil5'):
        generator = Keil5Generator()
    elif dst_type.startswith('IAR'):
        generator = IARGenerator()
    else:
        raise Exception()
    proj_gen.generate(dest_prj_path=project_path,
                      generator=generator,
                      generator_version=AVAILABLE_GENERATORS[dst_type],
                      input_desc=os.path.join(project_path, 'project.yaml'))
