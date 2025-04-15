# setup.py
from setuptools import setup, find_packages

setup(
    name='imgeval',  # 新的独特项目名称
    version='0.1.0',
    description='Image metrics evaluation package: PSNR, SSIM, RFID, LPIPS and visualization',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/imgeval',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'torch',
        'scipy',
        'tqdm',
        'scikit-image',
        'lpips',
        'torchvision'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
