from setuptools import setup, find_packages

setup(
    name="wedata_feature_engineering",  # 包名称
    version="0.1.0",                   # 版本号
    packages=find_packages(exclude=["tests*"]),  # 自动发现所有包，排除tests目录
    install_requires=[                 # 依赖包
        'pyspark>=3.0.0',
        'delta-spark>=1.0.0',
        'pandas>=1.0.0'               # 新增常用数据处理依赖
    ],
    python_requires='>=3.7',           # Python版本要求
    author="meahqian",                 # 作者
    author_email="",                   # 新增作者邮箱(建议添加)
    description="Wedata Feature Engineering Library",  # 描述
    long_description=open("README.md").read(),  # 新增详细描述(需README.md文件)
    long_description_content_type="text/markdown",  # 描述内容类型
    license="Apache 2.0",              # 许可证
    url="",                            # 新增项目URL(建议添加)
    classifiers=[                      # 新增分类器
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
