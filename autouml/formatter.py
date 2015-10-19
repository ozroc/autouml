

def format_args(args, kwargs):
    """
    Makes a nice string representation of all the arguments
    Taken from `format_args <https://gist.github.com/beng/7817597>`_
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


def generic_arrow(class1, class2, method, args, kwargs, arrow=''):
    '''
    Returns a sequence string

    >>> import autouml
    >>> autouml.formatter.generic_arrow('A', 'B', 'f', 'x', {} )
    'A -> B: f(x)'

    '''
    if class1 != '[':
        class1 += ' '
    return "%(class1)s->%(arrow)s %(class2)s: %(method)s%(args)s" % {
        'class1': class1,
        'class2': class2,
        'method': method,
        'args': format_args(args, kwargs),
        'arrow': arrow
    }


def method_arrow(*args):
    '''
    Returns a sequence string arrow for methods

    >>> import autouml
    >>> autouml.formatter.method_arrow('A', 'B', 'f', 'x', {} )
    'A -> B: f(x)'

    '''
    return generic_arrow(*args, arrow='')


def constructor_arrow(*args):
    '''
    Returns a sequence string arrow for methods

    >>> import autouml
    >>> autouml.formatter.constructor_arrow('A', 'B', '__init__', 'x', {} )
    'A ->o B: __init__(x)'

    '''
    return generic_arrow(*args, arrow='o')
