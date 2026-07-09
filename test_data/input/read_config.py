def read_config(filepath):
    config = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                config[key] = value
    except FileNotFoundError:
        print(f"配置文件 {filepath} 不存在，使用默认配置")
        config = {"debug": "false", "port": "8080"}
    except ValueError:
        print("配置文件格式错误，请检查每行是否为 key=value 格式")
        config = {}
    except PermissionError:
        print(f"没有权限读取 {filepath}")
        config = {}
    else:
        print(f"成功加载配置文件，共 {len(config)} 项配置")
    finally:
        # 即使前面有 return，这里也会执行
        print("配置加载完成")
    
    return config

config = read_config("app.conf")