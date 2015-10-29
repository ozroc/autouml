'''
autouml provides decorators to trace method
calls in your code during execution time.
'''

from autouml.version import __version__
import autouml.decorators

sequence_dia = autouml.decorators.get_decorator()
