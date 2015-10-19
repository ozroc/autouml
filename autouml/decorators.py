'''
Decorators for all object types
'''

import types
import logging
import inspect
import autouml.formatter

LOGGER = logging.getLogger('autouml')


def class_dec(orig_class):
    '''
    Decorates all public methods and class constructor
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
        #stack = inspect.stack()
        the_class = '['
        #the_method = '\b'
        #method_from = ''
        #end_method = ''
        the_class2 = '__main__'
        the_method2 = orig_func.__name__
        LOGGER.info(
            autouml.formatter.generic_arrow(
                the_class, the_class2, the_method2, args[1:], kwargs
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
            the_class = str(stack[1][0].f_locals['self'].__class__).replace(
                '__main__.', '') + ' '
        except:
            the_class = '['
#        the_method = stack[1][0].f_code.co_name
        #method_from = '''group %s
#    ''' % (the_method)
        #end_method = '''
#end'''
        the_class2 = ' ' + str(args[0].__class__).replace('__main__.', '')
        the_method2 = orig_func.__name__

        LOGGER.info(
            autouml.formatter.constructor_arrow(
                the_class, the_class2, the_method2, args[1:], kwargs
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
            the_class = str(stack[1][0].f_locals['self'].__class__).replace(
                '__main__.', '') + ' '
        except:
            the_class = '['
#        the_method = stack[1][0].f_code.co_name
#        method_from = '''group %s
#    ''' % (the_method)
#        end_method = '''
#end'''
        the_class2 = ' ' + str(args[0].__class__).replace('__main__.', '')
        the_method2 = orig_func.__name__

        LOGGER.info(
            autouml.formatter.method_arrow(
                the_class,
                the_class2,
                the_method2,
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
