import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from app.main import App

if __name__ == "__main__":
    app = App()
