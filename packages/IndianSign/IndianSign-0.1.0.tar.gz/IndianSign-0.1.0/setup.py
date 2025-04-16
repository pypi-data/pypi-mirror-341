from setuptools import setup, find_packages

setup(
    name='IndianSign',
    version='0.1.0',
    description='Sign Language Detection using Mediapipe and LSTM',
    author='Your Name',
    packages=find_packages(),
    include_package_data=True,
    package_data={'IndianSign': ['optimized_model.h5']},
    install_requires=[
        'numpy',
        'opencv-python',
        'mediapipe',
        'tensorflow',
    ],
)
