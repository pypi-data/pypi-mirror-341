from setuptools import setup, find_packages

setup(
    name='flask_todo_app',
    version='0.1.0',
    description='A simple Flask TODO app',
    author='Sergey Karpushin',
    author_email='your.email@example.com',
    url='https://github.com/<your-username>/<your-repo-name>',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)