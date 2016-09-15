from setuptools import find_packages, setup

setup(
    name='pycharts',
    version='0.1.1b1',
    url='https://github.com/ycharts/pycharts',
    license='MIT',
    description='Client for the YCharts API',
    author='YCharts Engineering',
    author_email='support@ycharts.com',
    keywords='development ycharts api rest restful',
    packages = find_packages(),
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    	'Programming Language :: Python :: 3.2',
    	'Programming Language :: Python :: 3.3',
    	'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ]
)