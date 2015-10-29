'''
autouml provides decorators to trace method
calls in your code during execution time.
'''

from autouml.version import __version__
import autouml.decorators


__OPTIONS__ = {
    'show_arguments': False,
    'use_instance_ids': True
}


def set_options(show_arguments=False,
                use_instance_ids=False
                ):
    'fill in internal options dictionary'
    __OPTIONS__['show_arguments'] = show_arguments
    __OPTIONS__['use_instance_ids'] = use_instance_ids


def sequence_dia(*args, **kwargs):
    'gets the configured decorator'
    return autouml.decorators.get_decorator(
        show_arguments=__OPTIONS__['show_arguments'],
        use_instance_ids=__OPTIONS__['use_instance_ids']
    )(*args, **kwargs)
