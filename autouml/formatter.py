
#  format_args taken from https://gist.github.com/beng/7817597
def args(args, kwargs):
    """
    makes a nice string representation of all the arguments
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
