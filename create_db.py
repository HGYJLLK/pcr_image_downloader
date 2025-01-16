import os
import json
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class PCRCharacterDB:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.image_dir = self.base_dir / 'image'
        self.info_file = self.base_dir / 'character_info.txt'
        self.db_path = self.base_dir / 'character_db.json'
        self.character_db = {}

    def is_skin_variation(self, name):
        """检查是否是皮肤变种"""
        skin_markers = ['春', '水', '鬼', '瓜', '圣', '江', '魔', '礼', '工']
        return any(marker in name for marker in skin_markers)

    def process_character_name(self, name_text):
        """
        处理角色名称
        :param name_text: 原始名称文本
        :return: 处理后的名称
        """
        name_text = name_text.strip()

        if '、' in name_text and not self.is_skin_variation(name_text):
            # 这是双人卡的情况，使用 & 连接名称
            names = [n.strip() for n in name_text.split('、')]
            return ' & '.join(names)
        else:
            # 单人卡或皮肤变种的情况
            return name_text

    def split_nicknames(self, text):
        """处理小名分割"""
        text = text.replace('，', ',').replace('、', ',').replace(' ', ',')
        return [nick.strip() for nick in text.split(',') if nick.strip()]

    def read_character_info(self):
        """从character_info.txt读取角色信息"""
        try:
            with open(self.info_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                char_info = {}
                if '小名:' in line:
                    basic_info, nicknames_part = line.split('小名:', 1)
                else:
                    basic_info, nicknames_part = line, ''

                # 处理基本信息
                basic_parts = basic_info.split(', ')
                for part in basic_parts:
                    if 'ID:' in part:
                        char_info['id'] = part.replace('ID:', '').strip()
                    elif '名称:' in part:
                        name_text = part.replace('名称:', '').strip()
                        char_info['name'] = self.process_character_name(name_text)
                    elif '星级:' in part:
                        char_info['stars'] = int(part.replace('星级:', '').strip())

                # 处理小名
                if nicknames_part:
                    char_info['nicknames'] = self.split_nicknames(nicknames_part.strip())
                else:
                    char_info['nicknames'] = []

                # 使用ID作为键
                if 'id' in char_info:
                    self.character_db[char_info['id']] = char_info

            logging.info(f"成功读取 {len(self.character_db)} 条角色信息")

        except Exception as e:
            logging.error(f"读取角色信息文件失败: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())

    def map_images(self):
        """映射图片文件"""
        try:
            image_files = list(self.image_dir.glob('*.png'))
            logging.info(f"找到 {len(image_files)} 个图片文件")

            for char_id, char_info in self.character_db.items():
                # 尝试两种文件名格式
                name_with_spaces = f"{char_info['name']}_{char_info['stars']}星.png"  # 带空格版本
                name_without_spaces = f"{char_info['name'].replace(' ', '')}_{char_info['stars']}星.png"  # 不带空格版本

                image_path = self.image_dir / name_with_spaces
                if not image_path.exists():
                    image_path = self.image_dir / name_without_spaces

                if image_path.exists():
                    char_info['image_path'] = str(image_path.relative_to(self.base_dir))
                else:
                    logging.warning(f"找不到角色图片，尝试了以下文件名:")
                    logging.warning(f"- {name_with_spaces}")
                    logging.warning(f"- {name_without_spaces}")

        except Exception as e:
            logging.error(f"映射图片文件失败: {str(e)}")

    def create_database(self):
        """创建角色数据库"""
        try:
            self.read_character_info()
            self.map_images()

            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.character_db, f, ensure_ascii=False, indent=2)

            logging.info(f"数据库已保存到: {self.db_path}")

            # 打印一些示例数据
            logging.info("数据库示例:")
            sample_count = 0
            for char_id, char_info in self.character_db.items():
                if sample_count < 3 or char_info.get('is_dual', False):
                    logging.info(json.dumps(char_info, ensure_ascii=False, indent=2))
                    sample_count += 1

        except Exception as e:
            logging.error(f"创建数据库失败: {str(e)}")


def main():
    base_dir = r'C:\Users\wdnmd\Desktop\pcr_image_downloader'
    db_creator = PCRCharacterDB(base_dir)
    db_creator.create_database()


if __name__ == "__main__":
    main()