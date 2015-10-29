

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
        allargs.append('%s' % str(item))

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
    if the_class is not None:
        if use_id:
            return ' %s@%s' % (
                str(the_class.__class__.__name__).replace('__main__.', ''),
                id(the_class)
            )
        else:
            return ' %s' % str(the_class.__class__.__name__).replace('__main__.', '')
    else:
        return '['


def method_name(the_method):
    return the_method.__name__


def generic_arrow(class1, class2, the_method, args, kwargs, arrow='', use_instance_ids=False):
    '''
    Returns a sequence string

    >>> generic_arrow('A', 'B', 'f', 'x', {} )
    'A -> B: f(x)'

    '''
    return "%(class1)s->%(arrow)s %(class2)s: %(method)s%(args)s" % {
        'class1': class_name(class1, use_instance_ids),
        'class2': class_name(class2, use_instance_ids),
        'method': method_name(the_method),
        'args': format_args(args, kwargs),
        'arrow': arrow
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
    kwargs['arrow'] = 'o'
    return generic_arrow(*args, **kwargs)
