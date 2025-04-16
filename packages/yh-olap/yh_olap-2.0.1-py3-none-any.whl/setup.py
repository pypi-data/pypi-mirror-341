from setuptools import setup, find_packages

setup(
    name='yh_olap',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        'aiofiles',
        'httpx',
        # 'requests',
        'pandas',
        'numpy',
        'pyotp',
        'selenium',
        'webdriver_manager',
        # 'requests_toolbelt',
        'yhlogin',
    ],
)