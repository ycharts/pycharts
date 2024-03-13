from setuptools import find_packages, setup

setup(
    name='pycharts',
    version='0.1.5',
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    	'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
