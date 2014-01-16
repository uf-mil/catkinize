import os
import re

from genmsg import msg_loader


def is_valid_version(version):
    """Check if `version` is a valid version according to
    http://ros.org/reps/rep-0127.html#version
    """
    match = re.match(r'^\d+\.\d+\.\d+$', version)
    return match is not None


def produce_funcs(directory, ext):
    def get_files(project_path):
        if not os.path.exists(os.path.join(project_path, directory)):
            return []
        return [filename for filename in os.listdir(os.path.join(project_path, directory)) if filename.endswith(ext)]


    def get_dependencies(project_path):
        result = set()
        
        for filename in get_files(project_path):
            with open(os.path.join(project_path, directory, filename), 'rb') as f:
                for line in f:
                    line = line.split('#')[0].strip()
                    if not line or line == '---': continue
                    type_, name = line.split(' ')
                    type_ = type_.split('[')[0]
                    
                    if '/' in type_:
                        pkg, type2_ = type_.split('/')
                        result.add(pkg)
                    elif type_ == 'Header':
                        result.add('std_msgs')
        
        return result
    
    return get_files, get_dependencies

get_message_files, get_message_dependencies = produce_funcs('msg', '.msg')
get_service_files, get_service_dependencies = produce_funcs('srv', '.srv')
get_action_files, get_action_dependencies = produce_funcs('action', '.action')
get_config_files, _ = produce_funcs('cfg', '.cfg')
