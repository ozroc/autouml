'''
Decorators for all object types
'''

import types
import logging
import inspect
import autouml.formatter


def get_decorator(
    logger_name='autouml',
    show_arguments=True,
    use_instance_ids=False
):
    '''
    This function will return a decorator wrapper 
    '''

    LOGGER = logging.getLogger(logger_name)
    autouml.formatter.USE_INSTANCE_ID = use_instance_ids

    def class_dec(orig_class):
        '''
        Takes a given class and returns a copy 
        with all its public methods 
        and class constructor decorated
        '''
        for name, method in inspect.getmembers(orig_class, inspect.ismethod):
            if not name.startswith('__'):
                setattr(orig_class, name, method_dec(method))
            elif name == '__init__':
                setattr(orig_class, name, constructor_dec(method))
        return orig_class

    def function_dec(orig_func):
        '''
        Simple function decorator
        '''
        def wrapper(*args, **kwargs):
            'Wrapping function for decorator'
            class_from = None
            class_to = None
            the_method = orig_func
            LOGGER.info(
                autouml.formatter.generic_arrow(
                    class_from,
                    class_to,
                    the_method,
                    args[1:],
                    kwargs,
                    use_instance_ids=use_instance_ids
                )
            )
            return orig_func(*args, **kwargs)
        return wrapper

    def constructor_dec(*orig_func):
        '''
        Decorates a constructor method
        '''

        orig_func = orig_func[0]

        def wrapper(*args, **kwargs):
            'Wrapping function for decorator'
            stack = inspect.stack()
            try:
                class_from = stack[1][0].f_locals['self']
            except:
                class_from = None
            class_to = args[0]
            the_method = orig_func
            LOGGER.info(
                autouml.formatter.constructor_arrow(
                    class_from,
                    class_to,
                    the_method,
                    args[1:],
                    kwargs
                )
            )
            return orig_func(*args, **kwargs)
        return wrapper

    def method_dec(*orig_func):
        '''
        Decorates a method
        '''
        orig_func = orig_func[0]

        def wrapper(*args, **kwargs):
            'Wrapping function for decorator'
            stack = inspect.stack()
            try:
                class_from = stack[1][0].f_locals['self']
            except:
                class_from = None
            class_to = args[0]
            the_method = orig_func

            LOGGER.info(
                autouml.formatter.method_arrow(
                    class_from,
                    class_to,
                    the_method,
                    args[1:],
                    kwargs
                )
            )
            return orig_func(*args, **kwargs)
        return wrapper

    __TYPEWRAPPERS = {
        types.FunctionType: method_dec,
        types.MethodType: method_dec,
        'generic': class_dec
    }

    def autodecorate(*args, **kwargs):
        '''
        This is an automatic decorator.
        It will analyse the type of the object to decorate
        and will apply the appropiate decorator.
        '''
        content_type = type(args[0])
        if content_type in __TYPEWRAPPERS.keys():
            return __TYPEWRAPPERS[content_type](*args, **kwargs)
        else:
            return __TYPEWRAPPERS['generic'](*args, **kwargs)

    return autodecorate
