import argparse

def getArgs(params):
    parser = argparse.ArgumentParser()
    for name, value in params.items():
        _help = value['help'] if 'help' in value else None
        _type = value['type'] if 'type' in value else None
        _default = value['default'] if 'default' in value else None
        parser.add_argument(name, help=_help, default=_default, type=_type)
    return parser.parse_args()

#[EOF]
