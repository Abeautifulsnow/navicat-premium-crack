import winreg
import os
from collections import deque


# root
HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER

# key path
PREMIUM_PATH = r'Software\PremiumSoft'
CLSID_PATH = r'Software\Classes\CLSID'


def get_sub_keys(root, reg_path: str) -> list:
    key_result = winreg.OpenKeyEx(root, reg_path)
    i: int = 0
    sub_keys_list: list = list()

    while True:
        try:
            sub_keys = winreg.EnumKey(key_result, i)
            sub_keys_list.append(sub_keys)
            i += 1
        except expression:
            break
    
    return sub_keys_list


def get_all_keys(root, key_path: str) -> list:
    all_keys_list: list = list()

    qeque = deque()
    qeque.append(key_path)

    while len(qeque) != 0:
        sub_key_path = qeque.popleft()

        for item in get_sub_keys(root, sub_key_path):
            item_path = os.path.join(sub_key_path, item)

            if len(get_sub_keys(root, item_path)) != 0:
                qeque.append(item_path)
                all_keys_list.append(item_path)
            else:
                all_keys_list.append(item_path)
    
    return all_keys_list


def main():
    clsid_all_keys_list = get_all_keys(HKEY_CURRENT_USER, CLSID_PATH)
    premium_all_keys_list = get_all_keys(HKEY_CURRENT_USER, PREMIUM_PATH)

    for clsid_item in clsid_all_keys_list:
        if "Info" in clsid_item:
            clsid_item_prefix = os.path.dirname(clsid_item)
            print(f"# Info item: {clsid_item}")
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, clsid_item)
            winreg.DeleteKeyEx(HKEY_CURRENT_USER, clsid_item_prefix)
    
    for premium_item in reversed(premium_all_keys_list):
        winreg.DeleteKeyEx(HKEY_CURRENT_USER, premium_item)


if __name__ == "__main__":
    main()
