import os
import glob

# noinspection PyUnresolvedReferences
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))]