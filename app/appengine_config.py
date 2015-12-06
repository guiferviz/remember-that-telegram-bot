

import os

from google.appengine.ext import vendor


# Add any libraries installed in the 'lib' folder.
vendor.add(os.path.join(os.path.dirname(__file__), 'lib'))

# Whether we are running in the debug or in the production environment.
DEBUG = os.environ.get('SERVER_SOFTWARE', 'Dev').startswith('Dev')
