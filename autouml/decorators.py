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

    def module_dec(orig_module):
        '''
        Takes a given module and returns a copy 
        with all its public classes and methods 
        decorated
        '''
        for name, method in inspect.getmembers(orig_module):
            setattr(orig_module, name, autodecorate(method))
        return orig_module

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
                    args,
                    kwargs,
                    show_arguments=show_arguments,
                    use_instance_ids=use_instance_ids
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
            try:
                class_to = args[0]
            except:
                class_to = None
            the_method = orig_func
            LOGGER.info(
                autouml.formatter.method_arrow(
                    class_from,
                    class_to,
                    the_method,
                    args,
                    kwargs,
                    show_arguments=show_arguments,
                    use_instance_ids=use_instance_ids
                )
            )
            return orig_func(*args, **kwargs)
        return wrapper

    def no_dec(orig_func):
        '''
        Decorates nothing
        '''
        return orig_func

    __TYPEWRAPPERS = {
        types.FunctionType: method_dec,
        types.MethodType: method_dec,
        types.BuiltinFunctionType: method_dec,
        types.BuiltinMethodType: method_dec,
        types.ModuleType: module_dec,
        types.ClassType: class_dec,
    }

    def autodecorate(*args, **kwargs):
        '''
        This is an automatic decorator.
        It will analyse the type of the object to decorate
        and will apply the appropiate decorator.
        '''
        content_type = type(args[0])
        return __TYPEWRAPPERS.get(content_type, no_dec)(*args, **kwargs)

    return autodecorate
