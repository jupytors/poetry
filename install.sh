pip install -r requirements.txt
cd data
git clone https://github.com/chinese-poetry/chinese-poetry.git raw/chinese-poetry
cd ..
python data/scripts/import_data.py
python app.py

cat << EOF
poetry-website/
├── app.py                  # Flask 主应用
├── config.py               # 配置文件
├── database.py             # 数据库连接
├── models.py               # 数据模型
├── requirements.txt        # Python 依赖
├── data/                   # 数据目录
│   ├── poetry.db          # SQLite 数据库
│   └── scripts/
│       └── import_data.py # 数据导入脚本
├── templates/              # HTML 模板
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页
│   ├── poem_detail.html   # 诗词详情
│   ├── search.html        # 搜索页
│   ├── author.html        # 作者页
│   ├── authors.html       # 作者列表
│   ├── dynasty.html       # 朝代页
│   └── dynasties.html     # 朝代列表
├── static/                 # 静态文件
│   ├── css/
│   │   └── style.css      # 样式文件
│   └── js/
│       └── main.js        # JavaScript
└── docs/                   # 文档
    └── deployment.md      # 部署文档
EOF