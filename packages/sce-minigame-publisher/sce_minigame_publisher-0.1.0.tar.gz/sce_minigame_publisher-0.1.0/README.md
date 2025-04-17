# auto-publish

TapTap SCE小游戏自动发布工具，用于自动化发布和管理小游戏项目。


## 功能特点

- 自动化处理游戏资源（图片、文件夹等）
- 支持批量上传游戏文件
- 自动将图片转换为 base64 编码
- 支持自定义配置参数
- 提供详细的错误处理和日志输出

## 使用方法

1. 配置 `minigame_config.json` 文件，设置相关参数
2. 将游戏资源文件放置在指定位置
3. 运行主程序：
   ```bash
   python minigame.py
   ```

## 配置文件说明

配置文件 `minigame_config.json` 包含以下主要部分：

```json
{
    "token": "your-auth-token",
    "data": {
        "project_id": "your-project-id",
        "tap_id": 123456,
        "title": "游戏标题",
        "description": "游戏描述",
        "tags": ["标签1", "标签2"],
        "version_name": "1.0.0",
        "banner": ["path/to/banner.png"],
        "icon": ["path/to/icon.png"],
        "screenshots": ["path/to/screenshot1.png", "path/to/screenshot2.png"],
        "folder": "path/to/game/folder"
    }
}
```

## 注意事项

1. 确保所有图片文件都存在且格式正确
2. 游戏资源文件夹中的文件将被自动转换为 base64 编码
3. 请妥善保管 API token，不要泄露
4. 认证令牌必须在配置文件中通过 `token` 字段设置
5. 建议在发布前先进行测试

## 常见问题解决

如果您在发布过程中遇到问题，请检查：
1. 配置文件是否正确
2. token 是否有效
3. 图片路径是否正确
4. 游戏文件夹是否存在

## 依赖项

- Python 3.6+
- requests

## 许可证

MIT 