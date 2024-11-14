import json
import os
import sys
import logging
from datetime import datetime

# 数据文件路径
DATA_FILE = "items_data.json"
LOG_FILE = "operation_log.txt"

# 存储物品信息的字典
items = {}

# 设置日志配置
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_operation(operation, details=""):
    """记录操作日志"""
    logging.info(f"操作: {operation}, 详情: {details}")

def load_data():
    """加载文件中的物品数据"""
    global items
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            items = json.load(file)
        print("数据已加载。")
        log_operation("加载数据", "成功加载物品数据")
    else:
        print("没有找到数据文件，初始化为空列表。")
        log_operation("加载数据", "没有找到数据文件，初始化为空列表")

def save_data():
    """将物品数据保存到文件"""
    with open(DATA_FILE, 'w') as file:
        json.dump(items, file)
    print("数据已保存。")
    log_operation("保存数据", "成功保存物品数据")

def add_item(name, description, contact):
    """添加物品"""
    if name in items:
        print(f"物品 '{name}' 已存在！")
        log_operation("添加物品", f"物品 '{name}' 已存在")
    else:
        items[name] = {'description': description, 'contact': contact}
        print(f"已添加物品 '{name}'")
        log_operation("添加物品", f"物品 '{name}' 添加成功")
        save_data()  # 每次添加物品后保存数据

def delete_item(name):
    """删除物品"""
    if name in items:
        del items[name]
        print(f"物品 '{name}' 已删除！")
        log_operation("删除物品", f"物品 '{name}' 已删除")
        save_data()  # 每次删除物品后保存数据
    else:
        print(f"未找到物品 '{name}'")
        log_operation("删除物品", f"未找到物品 '{name}'")

def display_items():
    """显示所有物品"""
    if items:
        print("当前物品列表:")
        for name, info in items.items():
            print(f"物品名称: {name}\n描述: {info['description']}\n联系人: {info['contact']}\n")
        log_operation("显示物品列表", "显示当前所有物品")
    else:
        print("物品列表为空！")
        log_operation("显示物品列表", "物品列表为空")

def search_item(name):
    """查找物品"""
    if name in items:
        info = items[name]
        print(f"物品名称: {name}\n描述: {info['description']}\n联系人: {info['contact']}\n")
        log_operation("查找物品", f"找到物品 '{name}'")
    else:
        print(f"未找到物品 '{name}'")
        log_operation("查找物品", f"未找到物品 '{name}'")

def modify_item(name):
    """修改物品信息"""
    if name in items:
        print(f"找到物品 '{name}'，请选择要修改的信息：")
        print("1. 修改物品描述")
        print("2. 修改联系人信息")
        choice = input("请输入操作编号: ").strip()
        
        if choice == '1':
            new_description = input("请输入新的物品描述: ").strip()
            items[name]['description'] = new_description
            print(f"物品 '{name}' 的描述已更新为：{new_description}")
            log_operation("修改物品", f"物品 '{name}' 描述已修改为：{new_description}")
            save_data()
        
        elif choice == '2':
            new_contact = input("请输入新的联系人信息: ").strip()
            items[name]['contact'] = new_contact
            print(f"物品 '{name}' 的联系人信息已更新为：{new_contact}")
            log_operation("修改物品", f"物品 '{name}' 联系人已修改为：{new_contact}")
            save_data()
        
        else:
            print("无效选择，请重新选择。")
            log_operation("修改物品", f"物品 '{name}' 修改操作无效选择")
    else:
        print(f"未找到物品 '{name}'，无法修改信息。")
        log_operation("修改物品", f"未找到物品 '{name}'，无法修改信息")

def main():
    print("欢迎使用物品‘复活’软件！")
    load_data()  # 启动时加载数据
    while True:
        print("\n请选择操作: ")
        print("1. 添加物品")
        print("2. 删除物品")
        print("3. 显示物品列表")
        print("4. 查找物品")
        print("5. 修改物品信息")
        print("6. 退出")
        
        choice = input("请输入操作编号: ").strip()
        
        if choice == '1':
            name = input("请输入物品名称: ").strip()
            description = input("请输入物品描述: ").strip()
            contact = input("请输入联系人信息: ").strip()
            add_item(name, description, contact)
        
        elif choice == '2':
            name = input("请输入要删除的物品名称: ").strip()
            delete_item(name)
        
        elif choice == '3':
            display_items()
        
        elif choice == '4':
            name = input("请输入要查找的物品名称: ").strip()
            search_item(name)
        
        elif choice == '5':
            name = input("请输入要修改的物品名称: ").strip()
            modify_item(name)
        
        elif choice == '6':
            print("程序已退出。")
            save_data()  # 退出时保存数据
            log_operation("退出程序", "程序已退出")
            sys.exit()
        
        else:
            print("无效输入，请重新选择！")
            log_operation("无效输入", "用户输入无效操作")

if __name__ == "__main__":
    main()
