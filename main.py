import os
import configparser
import json
import shutil



def read_configJson():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        return config

def write_configJson(config: dict):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        f.close()


def read_configInI(filePath: str):
    config = configparser.ConfigParser()
    config.read(filePath, encoding='utf-8')
    return {section: dict(config.items(section)) for section in config.sections()}

def write_configInI(filePath: str, config: dict):
    configParser = configparser.ConfigParser()
    for section in config:
        configParser[section] = config[section]

    with open(filePath, 'w', encoding='utf-8') as f:
        configParser.write(f)
        f.close()

def main():
    # 读取脚本config.json，判断是否存在config.json文件，如果不存在则创建一个

    config: dict = {}

    if not os.path.exists('config.json'):
        config = {
            'yuanshen': {
                'path': '',
                'server': 'cn',
                'version': '5.1.0',
            },
        }
        write_configJson(config)

    # 读取config.json文件，判断原神安装路径是否存在，如果不存在则提示用户输入
    config = read_configJson()

    if not config['yuanshen']['path']:
        editYuanShenPath(config)
    
    # 读取config.ini文件，获取原神版本号、cps、channel
    yuanshen_config = read_configInI(os.path.join(config['yuanshen']['path'], 'config.ini'))
    version = yuanshen_config['general']['game_version']

    if version != config['yuanshen']['version']:
        print('原神版本不匹配，可能切换程序不生效')
    
    print(f"当前原神版本：{version}")
    print(f"当前原神cps：{yuanshen_config['general']['cps']}")
    print(f"当前原神channel：{yuanshen_config['general']['channel']}")
    print(f"当前原神路径：{config['yuanshen']['path']}")
    print(f"当前程序支持版本：{config['yuanshen']['version']} \n")

    print('每次使用前，必须重启一次米哈游登录器！！！')
    print('每次使用前，必须重启一次米哈游登录器！！！')
    print('每次使用前，必须重启一次米哈游登录器！！！')
    print('请选择：1.切换B服 2.切换国服 3.修改原神安装路径 q.退出')
    choice = input('请输入选项：')

    if choice == '1'  or choice == '2':
        if choice == '1':
            yuanshen_config['general']['cps'] = 'bilibili'
            yuanshen_config['general']['channel'] = '14'
            yuanshen_config['general']['sub_channel'] = '0'
            
            pluginPath = os.path.join(config['yuanshen']['path'], 'YuanShen_Data\\Plugins\\PCGameSDK.dll')
            sdkPkgVersionPath = os.path.join(config['yuanshen']['path'], 'sdk_pkg_version')
            shutil.copy('PCGameSDK.dll', pluginPath)
            shutil.copy('sdk_pkg_version', sdkPkgVersionPath)

            if os.path.exists(pluginPath) and os.path.exists(sdkPkgVersionPath):
                print('切换B服成功。')
            else:
                print('切换B服失败，文件复制失败。')

        elif choice == '2':
            yuanshen_config['general']['cps'] = 'mihoyo'
            yuanshen_config['general']['channel'] = '1'
            yuanshen_config['general']['sub_channel'] = '1'

            pluginPath = os.path.join(config['yuanshen']['path'], 'YuanShen_Data\\Plugins\\PCGameSDK.dll')
            sdkPkgVersionPath = os.path.join(config['yuanshen']['path'], 'sdk_pkg_version')
            if os.path.exists(pluginPath) and os.path.exists(sdkPkgVersionPath):
                os.remove(pluginPath)
                if os.path.exists(pluginPath):
                    print('删除B服插件失败')
                else:
                    print('已删除B服插件')
                    print('已切换到官服')
            else:
                print('未找到B服插件，无需删除')
                print('已切换到官服')

        write_configInI(os.path.join(config['yuanshen']['path'], 'config.ini'), yuanshen_config)
    elif choice == '3':
        editYuanShenPath(config)
    else:
        exit()
    


    
def editYuanShenPath(config: dict):
    while True:
        path = input('请输入原神安装路径：')
        if os.path.exists(os.path.join(path, 'YuanShen.exe')):
            print('路径存在, 检测版本中...')
            break
        else:
            print('路径不存在，请重新输入')
    config['yuanshen']['path'] = path
    write_configJson(config)



if __name__ == '__main__':
    main()