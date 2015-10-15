import types
import log
import inspect
import formatter

def class_dec(orig_class):
     for name, m in inspect.getmembers(orig_class, inspect.ismethod):
        if not name.startswith('__'):
            setattr(orig_class, name, method_dec(m))
        elif name == '__init__':
            setattr(orig_class, name, constructor_dec(m))
     return orig_class


def function_dec(orig_func):
    def wrapper(*args, **kwargs):
        stack = inspect.stack()
        the_class = '['
        the_method = '\b'
        method_from = ''
        end_method = ''
        the_class2 = '__main__'
        the_method2 = orig_func.__name__
        log.logging.info("%s->%s%s: %s%s" % (the_class, 'o' if the_method2 == '__init__' else '', the_class2, the_method2, formatter.args(args[1:],kwargs)))
        return orig_func(*args, **kwargs)
    return wrapper


def constructor_dec(*orig_func):
    orig_func=orig_func[0]
    def wrapper(*args, **kwargs):
        stack = inspect.stack()
        try:
            the_class = str(stack[1][0].f_locals['self'].__class__).replace('__main__.','')+' '
        except:
            the_class = '['
        the_method = stack[1][0].f_code.co_name
        method_from = '''group %s
    ''' % (the_method)
        end_method = '''
end'''
        the_class2 = ' '+str(args[0].__class__).replace('__main__.','')
        the_method2 = orig_func.__name__
    
        log.logging.info("%s->o%s: %s%s" % (the_class, the_class2, the_method2, formatter.args(args[1:],kwargs)))
        return orig_func(*args, **kwargs)
    return wrapper

def method_dec(*orig_func):
    orig_func=orig_func[0]
    def wrapper(*args, **kwargs):
        stack = inspect.stack()
        try:
            the_class = str(stack[1][0].f_locals['self'].__class__).replace('__main__.','')+' '
        except:
            the_class = '['
        the_method = stack[1][0].f_code.co_name
        method_from = '''group %s
    ''' % (the_method)
        end_method = '''
end'''
        the_class2 = ' '+str(args[0].__class__).replace('__main__.','')
        the_method2 = orig_func.__name__
    
        log.logging.info("%s->%s: %s%s" % (the_class, the_class2, the_method2, formatter.args(args[1:],kwargs)))
        return orig_func(*args, **kwargs)
    return wrapper


__typewrappers = {
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
    content_type=type(args[0])
    if content_type in __typewrappers.keys():
        return __typewrappers[content_type](*args, **kwargs)
    else:
        return __typewrappers['generic'](*args, **kwargs)



