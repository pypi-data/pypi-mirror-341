from setuptools import setup, find_packages

setup(
    name='IndianSign',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    package_data={'IndianSign': ['optimized_model.h5']},
    install_requires=[
        'numpy',
        'mediapipe',
        'opencv-python'
    ],
    python_requires='>=3.6',
    description='Sign Language Detection using Mediapipe and LSTM',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Atharva',
)
