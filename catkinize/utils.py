import os
import re

from genmsg import msg_loader


def is_valid_version(version):
    """Check if `version` is a valid version according to
    http://ros.org/reps/rep-0127.html#version
    """
    match = re.match(r'^\d+\.\d+\.\d+$', version)
    return match is not None


def get_message_files(project_path):
    if not os.path.exists(os.path.join(project_path, 'msg')):
      return []
    return [filename for filename in os.listdir(os.path.join(project_path, 'msg')) if filename.endswith('.msg')]


def get_message_dependencies(project_path):
    result = set()
    
    for message_file in get_message_files(project_path):
        msg_context = msg_loader.MsgContext()
        file_path = os.path.join(project_path, 'msg', message_file)
        full_name = 'null/null' # doesn't matter so don't bother being correct
        msgspec = msg_loader.load_msg_from_file(msg_context, file_path, full_name)
        
        result.update(type_.split('/')[0]
          for type_ in msgspec.types if '/' in type_)
    
    return result
