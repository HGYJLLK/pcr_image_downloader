import pandas as pd
import requests
import os
from urllib.parse import urlparse
import logging

# 设置基础路径和图片保存路径
BASE_DIR = r'C:\Users\wdnmd\Desktop\pcr_image_downloader'
IMAGE_DIR = os.path.join(BASE_DIR, 'image')

# 设置日志
log_file = os.path.join(BASE_DIR, 'download.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class PCRImageDownloader:
    def __init__(self, excel_path):
        """
        初始化下载器
        :param excel_path: Excel文件路径
        """
        self.excel_path = os.path.join(BASE_DIR, excel_path)
        self.output_dir = IMAGE_DIR
        self.ensure_output_dir()

    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"创建输出目录: {self.output_dir}")

    def read_excel(self):
        """
        读取Excel文件内容，处理多个星级的图片链接
        :return: 包含角色信息的列表
        """
        try:
            df = pd.read_excel(self.excel_path, engine='openpyxl')
            character_data = []

            # 遍历每一行
            for index, row in df.iterrows():
                char_id = str(row[0])  # 编号
                nickname = str(row[7]) if pd.notna(row[7]) else None  # 小名

                # 处理1-2星图片
                if pd.notna(row[1]) and pd.notna(row[2]):
                    character_data.append({
                        'id': f"{char_id}_1",
                        'url': str(row[1]),
                        'name': str(row[2]),
                        'stars': 1,
                        'nickname': nickname
                    })

                # 处理3-5星图片
                if pd.notna(row[3]) and pd.notna(row[4]):
                    character_data.append({
                        'id': f"{char_id}_3",
                        'url': str(row[3]),
                        'name': str(row[4]),
                        'stars': 3,
                        'nickname': nickname
                    })

                # 处理6星图片
                if pd.notna(row[5]) and pd.notna(row[6]):
                    character_data.append({
                        'id': f"{char_id}_6",
                        'url': str(row[5]),
                        'name': str(row[6]),
                        'stars': 6,
                        'nickname': nickname
                    })

            logging.info(f"成功读取到 {len(character_data)} 条角色数据")
            return character_data
        except Exception as e:
            logging.error(f"读取Excel文件失败: {str(e)}")
            return []

    def download_image(self, url, filename):
        """
        下载单个图片
        :param url: 图片URL
        :param filename: 保存的文件名
        :return: 是否下载成功
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            file_path = os.path.join(self.output_dir, filename)

            # 检查文件是否已存在
            if os.path.exists(file_path):
                logging.info(f"图片已存在，跳过下载: {filename}")
                return True

            with open(file_path, 'wb') as f:
                f.write(response.content)

            logging.info(f"成功下载图片: {filename}")
            return True
        except Exception as e:
            logging.error(f"下载图片失败 {url}: {str(e)}")
            return False

    def create_character_info_file(self, character_data):
        """
        创建角色信息映射文件
        :param character_data: 角色数据列表
        """
        try:
            info_file = os.path.join(BASE_DIR, 'character_info.txt')
            with open(info_file, 'w', encoding='utf-8') as f:
                for char in character_data:
                    info_line = f"ID: {char['id']}, 名称: {char['name']}, 星级: {char['stars']}"
                    if char['nickname']:
                        info_line += f", 小名: {char['nickname']}"
                    f.write(info_line + '\n')
            logging.info(f"角色信息已保存到 {info_file}")
        except Exception as e:
            logging.error(f"保存角色信息失败: {str(e)}")

    def process_all_characters(self):
        """处理所有角色的图片下载"""
        character_data = self.read_excel()
        if not character_data:
            logging.error("没有找到角色数据")
            return

        success_count = 0
        fail_count = 0

        for char in character_data:
            # 构建文件名：角色名_星级.png
            filename = f"{char['name']}_{char['stars']}星.png"

            # 下载图片
            if self.download_image(char['url'], filename):
                success_count += 1
            else:
                fail_count += 1

        # 创建角色信息映射文件
        self.create_character_info_file(character_data)

        logging.info(f"下载完成。成功: {success_count}, 失败: {fail_count}")


def main():
    # 使用示例
    excel_filename = 'characters.xlsx'  # Excel文件名

    if not os.path.exists(os.path.join(BASE_DIR, excel_filename)):
        logging.error(f"Excel文件不存在: {excel_filename}")
        return

    downloader = PCRImageDownloader(excel_filename)
    downloader.process_all_characters()


if __name__ == "__main__":
    main()