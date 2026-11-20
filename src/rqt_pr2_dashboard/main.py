import sys

from rqt_gui.main import Main

from rqt_pr2_dashboard.pr2_dashboard import PR2Dashboard


def main():
    plugin = 'rqt_pr2_dashboard.pr2_dashboard.PR2Dashboard'
    sys.exit(Main().main(sys.argv, standalone=plugin,
                         plugin_argument_provider=PR2Dashboard.add_arguments))


if __name__ == '__main__':
    main()
