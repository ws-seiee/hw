import json
import os
import sys
import logging
from datetime import datetime
import getpass

DATA_FILE = "items_data.json"
LOG_FILE = "operation_log.txt"
USERS_FILE = "users_data.json"

# 存储物品信息的字典
items = {}
users = {}

# 设置日志
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_operation(operation, details=""):
    """记录操作日志"""
    logging.info(f"操作: {operation}, 详情: {details}")

def load_data():
    """加载物品和用户数据"""
    global items, users
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            items = json.load(file)
        print("物品数据已加载。")
        log_operation("加载数据", "成功加载物品数据")
    else:
        print("没有找到物品数据文件，初始化为空字典。")
        log_operation("加载数据", "没有找到物品数据文件，初始化为空字典")
        items = {}

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            users = json.load(file)
        print("用户数据已加载。")
        log_operation("加载数据", "成功加载用户数据")
    else:
        print("没有找到用户数据文件，初始化为空字典。")
        log_operation("加载数据", "没有找到用户数据文件，初始化为空字典")
        users = {}

def save_data():
    """将物品数据和用户数据保存到文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)
    print("数据已保存。")
    log_operation("保存数据", "成功保存物品和用户数据")

def add_item_type():
    """管理员设置新的物品类型"""
    name = input("请输入物品类型名称: ").strip()
    if name in items:
        print(f"物品类型 '{name}' 已存在！")
    else:
        attributes = input("请输入该类型物品的属性名称（用逗号分隔）: ").strip().split(',')
        items[name] = {
            "attributes": [attr.strip() for attr in attributes],
            "items": []
        }
        print(f"物品类型 '{name}' 已添加。")
        log_operation("添加物品类型", f"物品类型 '{name}' 添加成功")
        save_data()

def modify_item_type():
    """管理员修改物品类型"""
    name = input("请输入要修改的物品类型名称: ").strip()
    if name in items:
        new_attributes = input("请输入新的物品类型属性（用逗号分隔）: ").strip().split(',')
        items[name]["attributes"] = [attr.strip() for attr in new_attributes]
        print(f"物品类型 '{name}' 的属性已修改。")
        log_operation("修改物品类型", f"物品类型 '{name}' 修改成功")
        save_data()
    else:
        print(f"物品类型 '{name}' 不存在！")

def add_item():
    """添加物品"""
    if len(items) == 0:
        print("请先添加物品类型！")
        return

    item_type = input("请选择物品类型（例如：食品、书籍等）: ").strip()
    if item_type not in items:
        print(f"物品类型 '{item_type}' 不存在！")
        return

    print(f"物品类型 '{item_type}' 属性: {', '.join(items[item_type]['attributes'])}")
    
    item_info = {}
    for attr in items[item_type]['attributes']:
        item_info[attr] = input(f"请输入 {attr}: ").strip()

    # 物品基本信息
    item_name = item_info.get("物品名称")
    if item_name:
        items[item_type]["items"].append(item_info)
        print(f"已添加物品 '{item_name}' 到类型 '{item_type}'")
        log_operation("添加物品", f"物品 '{item_name}' 添加到类型 '{item_type}'")
        save_data()
    else:
        print("物品名称不能为空！")

def search_item():
    """根据类型和关键字搜索物品"""
    if len(items) == 0:
        print("请先添加物品类型！")
        return

    item_type = input("请输入物品类型进行搜索: ").strip()
    if item_type not in items:
        print(f"物品类型 '{item_type}' 不存在！")
        return

    keyword = input("请输入搜索关键字: ").strip()
    found_items = []
    for item in items[item_type]["items"]:
        if any(keyword.lower() in str(value).lower() for key, value in item.items()):
            found_items.append(item)

    if found_items:
        print(f"找到以下符合条件的物品：")
        for item in found_items:
            print(item)
    else:
        print("未找到符合条件的物品。")
    log_operation("查找物品", f"按关键字 '{keyword}' 搜索物品")

def register_user():
    """用户注册"""
    print("欢迎注册！")
    name = input("请输入用户名: ").strip()
    if name in users:
        print(f"用户名 '{name}' 已存在！")
    else:
        address = input("请输入住址: ").strip()
        phone = input("请输入手机号码: ").strip()
        email = input("请输入电子邮箱: ").strip()
        password = getpass.getpass("请输入密码: ").strip()
        users[name] = {
            "address": address,
            "phone": phone,
            "email": email,
            "password": password,
            "role": "user",
            "approved": False
        }
        print(f"用户 '{name}' 注册成功，等待管理员批准。")
        log_operation("用户注册", f"用户 '{name}' 注册成功，等待管理员批准")
        save_data()

def approve_user():
    """管理员批准用户"""
    name = input("请输入要批准的用户名: ").strip()
    if name in users:
        if users[name]["role"] == "admin":
            print("管理员账户无需批准。")
            return
        if users[name]["approved"]:
            print(f"用户 '{name}' 已经被批准。")
            return
        users[name]["approved"] = True
        print(f"用户 '{name}' 已批准。")
        log_operation("用户批准", f"用户 '{name}' 被批准")
        save_data()
    else:
        print(f"用户 '{name}' 不存在！")

def login():
    """用户登录"""
    print("欢迎登录物品复活系统！")
    name = input("请输入用户名: ").strip()
    if name not in users:
        print("用户名不存在！")
        log_operation("登录失败", f"用户名 '{name}' 不存在")
        return None

    password = getpass.getpass("请输入密码: ").strip()
    if users[name]["password"] != password:
        print("密码错误！")
        log_operation("登录失败", f"用户名 '{name}' 密码错误")
        return None

    if users[name]["role"] == "user" and not users[name]["approved"]:
        print("您的账户尚未被批准，请联系管理员。")
        log_operation("登录失败", f"用户 '{name}' 未被批准")
        return None

    print(f"欢迎，{name}！")
    log_operation("登录成功", f"用户 '{name}' 登录成功")
    return users[name]["role"]

def main():
    print("欢迎使用物品复活系统！")
    load_data()  # 启动时加载数据

    while True:
        role = login()
        if role is None:
            retry = input("是否重新登录？（y/n）：").strip().lower()
            if retry != 'y':
                print("程序已退出。")
                log_operation("退出程序", "用户选择退出")
                sys.exit()
            else:
                continue

        if role == "admin":
            while True:
                print("\n管理员菜单:")
                print("1. 添加物品类型")
                print("2. 修改物品类型")
                print("3. 批准用户")
                print("4. 添加管理员")
                print("5. 退出")
                choice = input("请输入操作编号: ").strip()

                if choice == '1':
                    add_item_type()
                elif choice == '2':
                    modify_item_type()
                elif choice == '3':
                    approve_user()
                elif choice == '4':
                    add_admin()
                elif choice == '5':
                    print("程序已退出。")
                    log_operation("退出程序", "管理员退出")
                    save_data()  # 退出时保存数据
                    sys.exit()
                else:
                    print("无效输入，请重新选择！")

        elif role == "user":
            while True:
                print("\n普通用户菜单:")
                print("1. 添加物品")
                print("2. 搜索物品")
                print("3. 退出")
                choice = input("请输入操作编号: ").strip()

                if choice == '1':
                    add_item()
                elif choice == '2':
                    search_item()
                elif choice == '3':
                    print("程序已退出。")
                    log_operation("退出程序", "用户退出")
                    sys.exit()
                else:
                    print("无效输入，请重新选择！")

def add_admin():
    """添加管理员"""
    name = input("请输入新管理员的用户名: ").strip()
    if name in users:
        print(f"用户名 '{name}' 已存在！")
    else:
        address = input("请输入住址: ").strip()
        phone = input("请输入手机号码: ").strip()
        email = input("请输入电子邮箱: ").strip()
        password = getpass.getpass("请输入密码: ").strip()
        users[name] = {
            "address": address,
            "phone": phone,
            "email": email,
            "password": password,
            "role": "admin",
            "approved": True  # 管理员无需批准
        }
        print(f"管理员 '{name}' 添加成功。")
        log_operation("添加管理员", f"管理员 '{name}' 添加成功")
        save_data()

if __name__ == "__main__":
    main()
