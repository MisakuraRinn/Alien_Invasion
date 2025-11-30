#coding=GBK
import math

class Settings:
  """存储游戏中的所有设置，包括静态和动态部分。"""

  def __init__(self,ai_game):
    # 屏幕设置
    self.screen_width=800
    self.screen_height=1000
    self.bg_color=(230,230,230)
    self.ai_game=ai_game   # 引用主游戏对象，方便访问 stats 等

    # 飞船设置
    self.ship_limit=3

    # 子弹设置
    # 速度为动态属性，稍后在 initialize_dynamic_settings 中设置
    self.bullet_width=3
    self.bullet_height=15
    self.bullet_color=(60,60,60)
    # 同屏允许的最大子弹数
    self.bullet_allowed=1000
    
    # 外星人设置（部分为动态属性）
    # self.alien_speed=1
    self.fleet_drop_speed=10
    # 1 为向右，-1 为向左
    self.fleet_direction=1
    
    # 游戏节奏加快相关设置
    self.alien_max_speed=20
    self.speedup_scale=1.1
    self.score_scale=1.5

    # 初始化随游戏进行而变化的设置
    self.initialize_dynamic_settings()
    
  def initialize_dynamic_settings(self):
    """初始化随游戏进行而变化的设置（在重新开始时会被重置）。"""
    self.ship_speed=5
    self.bullet_speed=15
    self.alien_speed=1
    self.alien_points=50   # 每个外星人基础得分
    self.fleet_direction=1
    # 当前剩余弹药数（由 Gun 管理具体逻辑）
    self.ammo_left=0
    
  def increase_speed(self):
    """根据当前关卡提升游戏速度与得分参数。"""
    # 外星人速度随关卡以 log2 形式增加，上限为 15
    self.alien_speed=min(1+math.log2(self.ai_game.stats.level),15)
    # 得分也随关卡缓慢上升
    self.alien_points=int(50+self.ai_game.stats.level)
