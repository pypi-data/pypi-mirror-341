from setuptools import setup, find_packages

setup(
    name='onetouchlite',  # 包名
    version='0.0.7',  # 版本号
    author='17fine',  # 作者
    author_email='2756601885@qq.com',  # 作者邮箱
    description='一个简单的轻量，集成了大多数OneTouch用法的工具包',  # 包的简短描述
    long_description=open('README.md', encoding="utf8").read(),  # 读取 README.md 文件作为长描述
    long_description_content_type='text/markdown',  # 长描述的内容类型
    url='https://gitee.com/SunnyB0y/onetouch',  # 包的官网地址
    packages=find_packages(),  # 自动查找包内的所有包和子包
    package_data={
        'onetouchlite': ['utils/progress.dll', 'utils/libprogress.so'],  # 包含 C 扩展文件
    },
    install_requires=[  # 依赖的包列表

    ],
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python版本要求
)
