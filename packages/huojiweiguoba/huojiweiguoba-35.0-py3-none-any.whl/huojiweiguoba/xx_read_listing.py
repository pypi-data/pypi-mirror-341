import os.path
import time
from pathlib import Path
import pandas
import yaml
from PIL import Image
from natsort import natsorted
import shutil

from tools import get_aspect_ratio
from huojiweiguoba import lbw_datetime

def load_yaml(file):
    with open(file, 'r', encoding='utf-8') as f:
        # return yaml.load(f, Loader=yaml.FullLoader)
        return yaml.safe_load(f)

class ReadListingInfo:
    '''读取上新文件夹信息'''

    def __init__(self, listing_folder_path,yaml_rule):
        self.yaml_rule = yaml_rule
        self.listing_folder_path = listing_folder_path  # 上新文件夹路径
        self.listing_shop_folder_path = Path(listing_folder_path).parent.resolve().__str__()  # 店铺文件夹
        self.listing_shop_log_file = (Path(listing_folder_path).parent / "上架日志.txt").resolve().__str__() # 店铺日志
        self.listing_shop_folder_name = Path(listing_folder_path).parent.name  # 店铺名
        self.listing_folder_name = Path(listing_folder_path).name  # 上新文件夹名
        self.listing_plat_name = Path(listing_folder_path).parent.parent.parent.name  # 上新平台
        self.listing_plat_type = Path(listing_folder_path).parent.parent.name  # 上新分类(男女童)
        # category
        self.category_config_file_path = None  # 分类配置文件路径
        self.category_config_file_name = None  # 分类配置文件名
        self.category_config_file_sheet = None  # 分类配置文件sheet
        self.category_config_items = None  # 分类配置数据
        self.goods_title = None  # 商品标题
        # img
        self.main_img_items = None  # 主图
        self.long_main_img_items = None  # 主图长图
        self.detail_img_items = None  # 详情图
        self.sku_img_items = None  # SKU图
        self.long_sku_img_items = None  # SKU长图
        # sku具体配置信息
        self.sku_info_items = None  # sku配置信息

    def record_log(self,bid:str):
        text = f"[{lbw_datetime.get_local_now_date()}] 上架成功 宝贝ID:{bid} {self.listing_folder_name}\n"
        with open(self.listing_shop_log_file,'a') as f:
            f.write(text)

    def end_action(self,text):
        text = f"[{lbw_datetime.get_local_now_date()}] {text}"
        end_file_path = (Path(self.listing_folder_path) / "日志.txt").resolve().__str__()
        with open(end_file_path,'w') as f:
            f.write(text)

    def load_img(self):
        plat_rule_folder = FOLDER_RULE['structure'][self.listing_plat_name]['folder']
        # 从文件夹规则中载入对应图片
        for x in plat_rule_folder:
            # 文件夹路径
            path = Path(self.listing_folder_path) / x['name']
            # 查看是否必须拥有+文件夹是否存在
            if x['required'] and not Path(path).is_dir():
                raise ValueError(f"缺少【{x['name']}】文件夹")
            # 获取文件夹中得所有对应类型图片
            files = [f for f in path.glob("*") if f.suffix.lower()[1:] in x['file_type']]
            # 是否需要自然排序
            if x['sort']:
                files = natsorted(files,key= lambda y:y.stem.lower())
            # 校验图片张数
            if len(files)<x['file_num_limit']['min'] or len(files)>x['file_num_limit']['max']:
                raise ValueError(f"【{path.name}】文件夹：图片数量应该为{x['file_num_limit']['min']}-{x['file_num_limit']['max']}张")
            # 校验其他
            for f in files:
                # 获取图片高和宽
                img = Image.open(f)
                w,h = img.size
                size = os.path.getsize(f) / (1024 * 1024) # 单位MB
                # 校验图片大小
                if size<x['file_size_limit']['min'] or size>x['file_size_limit']['max']:
                    raise ValueError(f"【{path.name}】文件夹：【{Path(f).name}】大小应该为{x['file_size_limit']['min']}-{x['file_size_limit']['max']}MB")
                # 校验图片尺寸
                if w<x['file_pixel_limit']['width_min'] or w>x['file_pixel_limit']['width_max']:
                    raise ValueError(f"【{path.name}】文件夹：【{Path(f).name}】 宽区间应该为{x['file_pixel_limit']['width_min']}px-{x['file_pixel_limit']['width_max']}px")
                if h<x['file_pixel_limit']['height_min'] or h>x['file_pixel_limit']['height_max']:
                    raise ValueError(f"【{path.name}】文件夹：【{Path(f).name}】 高区间应该为{x['file_pixel_limit']['height_min']}px-{x['file_pixel_limit']['height_max']}px")
                # 校验图片比例
                if x['file_pixel_limit']['width_height_ratio']:
                    ratio = f"{get_aspect_ratio(w,h)[0]}:{get_aspect_ratio(w,h)[1]}"
                    if ratio != x['file_pixel_limit']['width_height_ratio']:
                        raise ValueError(f"【{path.name}】文件夹：【{Path(f).name}】 比例应该为{x['file_pixel_limit']['width_height_ratio']},目前为{ratio}")
            # 图片新增到对应对象中
            self.__setattr__(x['object_name'], {i.stem:{"local_path":i.__str__()} for i in files})

    def load_price_stock(self):
        plat_rule_file = self.yaml_rule['structure'][self.listing_plat_name]['file']
        # 从文件规则中载入对应
        for x in plat_rule_file:
            # 文件路径
            path = Path(self.listing_folder_path) / (x['name']+f".{x['file_type']}")
            # 查看是否必须拥有+文件是否存在
            if x['required'] and not Path(path).is_file():
                raise ValueError(f"缺少【{x['name']}】文件")
            # 判断文件类型
            if x['file_type'] == "xlsx":
                file_df = pandas.read_excel(path)
                # 检查需求列是否都存在
                need_rows = ['SKU名称','主图','长图','价格','库存','跑编码名称']
                for i in need_rows:
                    if i not in file_df.columns:
                        raise ValueError(f"【{x['name']}】文件中缺少【{i}】列")
                # 将所有nan转换为None
                file_df = file_df.fillna(value="")
                file_df['主图'] = file_df['主图'].astype(str)
                file_df['长图'] = file_df['长图'].astype(str)
                file_df['价格'] = file_df['价格'].astype(float)
                file_df['库存'] = file_df['库存'].astype(int)
                file_items = file_df.to_dict('records')
            # if x['file_type']=="txt":
            #     file_list = []
            #     with path.open(encoding='utf-8') as f:
            #         for line in f.readlines():
            #             file_list.append([str(i) for i in line.strip().split("/")])
            #     file_items = [dict(zip(file_list[0], i)) for i in file_list[1:]]
            else:
                raise ValueError(f"文件类型应该为xlsx，目前为{x['file_type']},联系管理员增加其他类型文件读取")
            # 文件新增到对应对象中
            self.__setattr__(x['object_name'], file_items)

    def move_listing_folder(self):
        move_path = self.listing_folder_path.replace(self.yaml_rule['listing_path'],self.yaml_rule['listing_backups_path'])
        if not Path(move_path).parent.exists():
            Path(move_path).mkdir(parents=True)
        # 查看目标文件夹是否存在
        if Path(move_path).exists():
            shutil.rmtree(move_path)
        # 移动文件夹
        shutil.move(self.listing_folder_path,move_path)
        # 查看原文件夹是否还在 还在需要删除
        try:
            if Path(self.listing_folder_path).exists():
                shutil.rmtree(self.listing_folder_path)
        except Exception as e:
            raise ValueError(f"已完成上架提交,文件夹被占用删除失败,请手动删除此文件夹!{str(e)}")


    def load_category(self):
        if self.listing_folder_name.count("_") < 2:
            raise ValueError("上新文件夹名 _ 符号少于2个")
        self.category_config_file_name = self.listing_folder_name.split("_")[0]
        self.category_config_file_sheet = self.listing_folder_name.split("_")[1]
        self.goods_title = self.listing_folder_name.split("_")[2]
        self.category_config_file_path = ((
                Path(self.listing_folder_path).parent.parent / f"{self.category_config_file_name}.xlsx").resolve().__str__())
        # 在上新文件夹父级目录寻找分类配置文件
        if not Path(self.category_config_file_path).is_file():
            raise FileNotFoundError(f"找不到上新文件夹的分类配置文件：{self.category_config_file_path}")
        # 读取分类配置文件
        if self.category_config_file_sheet not in pandas.ExcelFile(self.category_config_file_path).sheet_names:
            raise ValueError(f"类目文件【{self.category_config_file_path}】sheet：{self.category_config_file_sheet} 不存在,请联系管理员添加")
        df = pandas.read_excel(self.category_config_file_path, sheet_name=self.category_config_file_sheet)
        # 将所有nan转换为None
        df = df.fillna(value="")
        df['值'] = df['值'].astype(str)
        df['属性'] = df['属性'].astype(str)
        df_list = df.to_dict("records")
        df_items = {x['属性']:x['值'] for x in df_list}
        self.category_config_items = df_items


def get_folder_listing_task(plat_name,gender,yaml_path,wait_time=10):
    FOLDER_RULE = load_yaml(yaml_path)
    if not Path(FOLDER_RULE['listing_path']).is_dir():
        raise ValueError(f"找不到上新源文件夹：{FOLDER_RULE['listing_path']}")
    plat_listing_path = Path(FOLDER_RULE['listing_path']) / plat_name
    if not plat_listing_path.is_dir():
        raise ValueError(f"找不到上新平台文件夹：{plat_listing_path}")
    plat_gender_path = plat_listing_path / gender
    if not plat_gender_path.is_dir():
        raise ValueError(f"找不到上新分类文件夹：{plat_gender_path}")
    # 遍历文件夹
    while True:
        # 获取文件夹下的所有店铺文件夹
        shops_dir = [f for f in plat_gender_path.iterdir() if f.is_dir()]
        # 循环店铺
        for shop in shops_dir:
            # 获取店铺中得所有上架文件夹
            listing_dir = [f for f in shop.iterdir() if f.is_dir()]
            # 循环上架文件夹
            for listing in listing_dir:
                if "日志.txt" not in [x.name.__str__() for x in listing.iterdir() if x.is_file()]:
                    # 等待文件夹文件加载完成时间
                    print(f"\n=========================等待{wait_time}秒开始\n当前上架文件夹：{listing}")
                    time.sleep(wait_time)
                    # 获取上架文件夹中得所有上架文件
                    rli = ReadListingInfo(listing.__str__(),FOLDER_RULE)
                    # rli.load_category()
                    # rli.load_img()
                    # rli.load_price_stock()
                    yield rli
        time.sleep(wait_time)