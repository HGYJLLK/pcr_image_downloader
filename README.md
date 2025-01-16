# PCR Image Downloader 

## 项目简介
这是一个基于Python的公主连结wiki的抓包，主要用于学习图像处理和角色识别。作为一名学生，我创建这个项目纯粹出于学习目的，用于给游戏中识别角色的功能，这是我项目的一小部分后续还会添加。

## 项目功能
- 从抓包的Excel文件中读取角色数据
- 下载不同星级的角色头像
- 生成角色信息映射文件
- （后续开发中）基于OpenCV的角色识别功能
- 内部写了详细的注释，可以修改参考使用

## 技术栈
- Python 3.x
- pandas
- openpyxl
- requests
- logging

## 项目结构
```
pcr_image_downloader/
│
├── .venv/                 # Python虚拟环境
├── image/                 # 下载的图片存储位置
├── main.py               # 主程序
├── characters.xlsx       # 角色数据文件
├── character_info.txt    # 生成的角色信息映射
└── download.log          # 下载日志
```

## 使用方法
1. 创建并激活虚拟环境
2. 安装依赖：
```bash
pip install pandas openpyxl requests
```
3. 运行程序：
```bash
python main.py
```

## 数据来源与鸣谢
- 角色数据来源：[碧蓝档案 Wiki](https://wiki.biligame.com/pcr/%E8%A7%92%E8%89%B2%E5%88%AB%E7%A7%B0)
- 特别感谢公主连结Wiki的贡献者们，花舞攻略组提供的宝贵资料
- 数据采集工具：八爪鱼采集器8

## 免责声明
本项目仅用于学习和教育目的。所有用到的角色数据和图片的版权归原作者所有。如有侵权，请联系我们删除。

## 注意事项
*本项目仅供学习交流使用*