from setuptools import setup, find_packages
import stpp_tplot

setup(
    name='stpp_tplot',  # パッケージ名 (pip install で使う名前)
    version=stpp_tplot.__version__,  # バージョン (Semantic Versioning に従うことを推奨)
    packages=find_packages(where='stpp_tplot'),  # パッケージを自動検出 (stpp_tplotディレクトリ内)
    package_dir={'': 'stpp_tplot'}, # パッケージのルートディレクトリを指定
    install_requires=[  # 依存するライブラリ
        'matplotlib==3.10.1',
        'pyspedas==1.7.19',
        'seaborn>=0.11.0',
        'pytz==2025.2',
        'numpy==2.2.4',
    ],
    author='Kohki Tachi',  # あなたの名前 (作者名)
    author_email='ktachiresearch@gmail.com',  # あなたのメールアドレス (作者メールアドレス)
    description='Simple time series plotting library based on pyspedas and matplotlib.',  # 簡単な説明
    long_description=open('README.md').read(),  # 詳細な説明 (README.md を読み込む)
    long_description_content_type='text/markdown',  # README.md の形式
    url='https://github.com/JackKTachi/stpp_tplot',  # ライブラリのURL (GitHubリポジトリなど)
    license='MIT',  # ライセンス (例: MIT License)
    classifiers=[  # PyPIでの分類 (任意だが推奨)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research', # 対象ユーザー
        'Topic :: Scientific/Engineering :: Visualization', # トピック
    ],
)