Alien Invasion — Extended Roguelike Edition

自制强化版外星人入侵（Python + Pygame）

? 项目简介

本项目基于《Python Crash Course》中的 Alien Invasion 游戏框架进行扩展开发，加入大量现代游戏机制，包括：

? 新增特色功能（全部由我自行实现）

五种武器系统（手枪/机枪/散弹枪/突击步枪/榴弹发射器）

动态子弹 UI 显示与真实换弹机制（threading 实现）

随机 Roguelike 升级系统（三选一 buff）

随等级自动调整的难度曲线（速度 + 血量 + 刷怪密度）

子弹穿透/爆炸/反弹系统

持久化高分存档（data.txt）

? 目录结构
Alien_Invasion/
│
├── alien_invasion.py     # 主程序入口
├── settings.py           # 动态难度、速度、子弹/外星人参数
├── ship.py               # 飞船
├── bullet.py             # 弹道、穿透、反弹、爆炸
├── alien.py              # 外星人生成 + 生命值
├── gun.py                # 五把武器 + 切换 + 升级
├── rogue.py              # Roguelike 随机升级系统
├── scoreboard.py         # 分数、生命、弹药 UI
├── game_stats.py         # 状态管理，高分读取/写入
├── button.py             # Play 按钮
├── data.txt              # 高分保存
└── voices/ images/       # 音效与图像资源

?? 运行方法
1. 安装依赖
pip install pygame

2. 运行游戏
python alien_invasion.py

? 游戏操作方式
按键	功能
← / →	移动
SPACE	开火
1~5	切换武器（解锁后可用）
Q	保存高分并退出
鼠标点击	选择升级 buff
? 武器系统
武器	特点
Pistol	标准单发，稳定
Machine Gun	高射速，低伤害
Shotgun	多发散射
Assault Rifle	高穿透力
Grenade Launcher	爆炸 + 多碎片
? Roguelike 升级系统

每过一关自动弹出三选一升级，包括：

解锁新武器

提升射速

增大装弹量

增强穿透能力

增加弹片个数

提升反弹次数

修改散射角度

每局体验完全不同。

? 高分系统

退出游戏（按 Q）时自动写入文件：

data.txt


再次进入游戏自动加载。

? Project 14-4 / 14-6 完成说明

? 14-4：最高分持久化存储已完整实现

? 14-6：通过新增武器系统 + buff 系统 + 动态 UI 完成“扩展游戏”要求

? 预览截图

（你自行补图）

? License

本项目仅用于课程学习。