from setuptools import setup, find_packages
import io
import os

version = os.environ.get('RELEASE_VERSION', '0.3.0'
'').lstrip('v')

setup(
    name="kirara-ai-email",
    version=version,
    packages=find_packages(),
    include_package_data=True,  # 这行很重要
    package_data={
        "kirara_email": ["example/*.yaml", "example/*.yml"],
    },
    install_requires=[
        "msal",
        "kirara-ai>=3.2.0",
    ],
    entry_points={
        'chatgpt_mirai.plugins': [
            'kirara_email = kirara_email:EmailPlugin'
        ]
    },
    author="chuanSir",
    author_email="416448943@qq.com",

    description="收发邮件 for lss233/chatgpt-mirai-qq-bot，提供收取未读邮件和发送邮件的block，首次发送或收取邮件请一并提供发件人邮箱和授权码（授权码获取路径：qq邮箱-设置-账号与安全-安全设置-开启服务-获取授权码）",
    long_description=io.open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chuanSir123/kirara-ai-emial",
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Affero General Public License v3',
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/chuanSir123/kirara-ai-emial/issues",
        "Documentation": "https://github.com/chuanSir123/kirara-ai-emial/wiki",
        "Source Code": "https://github.com/chuanSir123/kirara-ai-emial",
    },
    python_requires=">=3.8",
)
