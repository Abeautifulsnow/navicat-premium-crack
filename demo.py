import winreg

# Delete HKEY_CURRENT_USER\Software\PremiumSoft\NavicatPremium\Update
try:
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\PremiumSoft\\NavicatPremium\\Update",
        0,
        winreg.KEY_ALL_ACCESS,
    )
    print(f"Update: {key}")
    winreg.DeleteKey(key, "")
    key.Close()
    print(
        "Deleted key: HKEY_CURRENT_USER\\Software\\PremiumSoft\\NavicatPremium\\Update"
    )
except WindowsError:
    pass

# Delete HKEY_CURRENT_USER\Software\PremiumSoft\NavicatPremium\Registration[version and language]
try:
    reg_path = "Software\\PremiumSoft\\NavicatPremium"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    for i in range(winreg.QueryInfoKey(key)[0]):
        subkey_name = winreg.EnumKey(key, i)
        if "Registration" in subkey_name:
            subkey_path = reg_path + "\\" + subkey_name
            subkey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, subkey_path, 0, winreg.KEY_ALL_ACCESS
            )
            value_names = [
                winreg.EnumValue(subkey, j)[0]
                for j in range(winreg.QueryInfoKey(subkey)[1])
            ]
            for value_name in value_names:
                print(f"Registration: {value_name}")
                winreg.DeleteValue(subkey, value_name)
            print("Deleted values from key:", subkey_path)
            subkey.Close()
    key.Close()
except WindowsError:
    pass

# Delete Info and ShellFolder under HKEY_CURRENT_USER\Software\Classes\CLSID
try:
    reg_path = "Software\\Classes\\CLSID"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
    for i in range(winreg.QueryInfoKey(key)[0]):
        subkey_name = winreg.EnumKey(key, i)
        subkey_path = reg_path + "\\" + subkey_name
        subkey = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, subkey_path, 0, winreg.KEY_ALL_ACCESS
        )
        for value_name in ["Info", "ShellFolder"]:
            try:
                print(f"Info-ShellFolder: {(subkey, value_name)}")
                winreg.DeleteValue(subkey, value_name)
            except WindowsError:
                pass
        print("Deleted values from key CLSID:", subkey_path)
        subkey.Close()
    key.Close()
except WindowsError:
    pass
