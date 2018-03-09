"""For dynamic plugins loading
As an asynchronous celery task implementation.
It could be imported as module, and call load_plugins(*args, **kwargs)
to load any plugin(s) you want.
Function(s):
 .. 1. load_plugins(*args, **kwargs)
 .. 2. check_plugins(*args, **kwargs)
"""