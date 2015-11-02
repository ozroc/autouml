'''
Formatters for beutifying logs
'''
import types
import inspect


__BOXES__ = {}


def draw_box(class_name):
    return '''
box "%s" 
  participant %s
end box
''' % (class_name, '\n  participant '.join(__BOXES__[class_name]))


def class_box(class_id_name):
    if '@' in class_id_name:
        class_name, id_name = class_id_name.split('@')
        if class_name not in __BOXES__.keys():
            __BOXES__[class_name] = [id_name]
            return draw_box(class_name)
        elif id_name not in __BOXES__[class_name]:
            __BOXES__[class_name].append(id_name)
            return draw_box(class_name)
    return ''


def format_args(args, kwargs):
    """
    Makes a nice string representation of all the arguments
    Taken from `format_args <https://gist.github.com/beng/7817597>`_

    >>> args = (1, 2)
    >>> kwargs = {'one': 1, 'two': 2}
    >>> format_args(args, kwargs)
    '(1, 2, two=2, one=1)'

    """

    allargs = []
    for item in args:
        try:
            allargs.append('%s' % str(item))
        except:
            allargs.append(item.__class__)

    for key, item in kwargs.items():
        allargs.append('%s=%s' % (key, str(item)))

    formattedArgs = '(%s)' % ', '.join(allargs)

    if len(formattedArgs) > 150:
        return formattedArgs[:146] + " ..."
    return formattedArgs


def class_name(the_class, use_id=False):
    '''
    Returns class name and, optionally, instance id
    '''
    if type(the_class) == types.InstanceType:
        if use_id:
            return ' %s@%s' % (
                str(the_class.__class__.__name__).replace('__main__.', ''),
                id(the_class)
            )
        else:
            return ' %s' % str(the_class.__class__.__name__).replace('__main__.', '')
    else:
        return None


def method_name(the_method):
    return the_method.__name__


def generic_arrow(class1, class2, the_method, args, kwargs, arrow='', use_instance_ids=False, show_arguments=True):
    '''
    Returns a sequence string

    >>> generic_arrow('A', 'B', 'f', 'x', {} )
    'A -> B: f(x)'

    '''
    class_name_1 = class_name(class1, use_instance_ids)
    class_name_2 = class_name(class2, use_instance_ids)
    if class_name_1 is None:
        class_name_1 = '__main__'
    if class_name_2 is None:
        class_name_2 = '__main__'
    if len(args) > 0:
        if id(class2) == id(args[0]):
            args = list(args)
            args[0] = 'self'
    return "%(class1)s->%(arrow)s%(class2)s: %(method)s%(args)s%(box1)s%(box2)s" % {
        'class1': class_name_1.split('@')[-1],
        'class2': class_name_2.split('@')[-1],
        'method': method_name(the_method),
        'args': format_args(args, kwargs) if show_arguments else '',
        'arrow': arrow,
        'box1': class_box(class_name_1),
        'box2': class_box(class_name_2)
    }


def method_arrow(*args, **kwargs):
    '''
    Returns a sequence string arrow for methods

    >>> method_arrow('A', 'B', 'f', 'x', {} )
    'A -> B: f(x)'

    '''

    return generic_arrow(*args, **kwargs)


def constructor_arrow(*args, **kwargs):
    '''
    Returns a sequence string arrow for constructor methods

    >>> constructor_arrow('A', 'B', '__init__', 'x', {} )
    'A ->o B: __init__(x)'

    '''
    kwargs['arrow'] = 'o '
    return generic_arrow(*args, **kwargs)
