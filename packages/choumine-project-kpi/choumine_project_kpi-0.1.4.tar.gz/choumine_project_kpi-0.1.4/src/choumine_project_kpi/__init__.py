# __init__.py（保持不变）
from .common import app
from . import tools

def main():
    app.run(transport='stdio')

if __name__ == "__main__":
    main()
