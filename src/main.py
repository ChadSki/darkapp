import sys

from gui import MainApplication


def main(argv):
    app = MainApplication(argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
