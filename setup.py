"""setup file for project"""

from setuptools import setup, find_packages

setup_config = {"name": "api_buster",
                "version": "1.0.0",
                "description": "Web app for process automation of critical McMakler business process",
                "url": "PLACEHOLDER",
                "author": "Willi Kristen",
                "author_mail": "willi.kristen@live.de",
                "license": "Willi Kristen Proprietary"}

install_requires = ["certifi==2022.6.15",
                    "charset-normalizer==2.1.0",
                    "click==8.1.3",
                    "Flask==2.1.3",
                    "Flask-Login==0.6.1",
                    "Flask-SQLAlchemy==2.5.1",
                    "greenlet==1.1.2",
                    "idna==3.3",
                    "itsdangerous==2.1.2",
                    "Jinja2==3.1.2",
                    "MarkupSafe==2.1.1",
                    "regex==2022.7.9",
                    "requests==2.28.1",
                    "SQLAlchemy==1.4.39",
                    "urllib3==1.26.10",
                    "Werkzeug==2.1.2"]

tests_require = ["pytest==7.1.2",
                 "testcontainers==3.6.1"]

setup_config['install_requires'] = install_requires
setup_config['tests_require'] = tests_require
setup_config['extras_require'] = {"tests": tests_require}
setup_config['packages'] = find_packages(include=["api_buster", "api_buster.*"])

if __name__ == '__main__':
    setup(**setup_config)
