from glob import glob

from setuptools import setup

package_name = 'rqt_pr2_dashboard'

setup(
    name=package_name,
    version='2.0.0',
    package_dir={'': 'src'},
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'plugin.xml']),
        ('share/' + package_name + '/images', glob('images/*.svg')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sammy Pfeiffer',
    maintainer_email='Sammy.Pfeiffer@student.uts.edu.au',
    description='rqt dashboard for the PR2: motors, breakers, runstops, battery, diagnostics.',
    license='BSD',
    entry_points={
        'console_scripts': [
            'rqt_pr2_dashboard = rqt_pr2_dashboard.main:main',
        ],
    },
)
