#coding=GBK

class GameStats:
  """跟踪游戏的统计信息。
  
  负责记录：当前得分、最高分、当前关卡、剩余飞船数等。
  在游戏运行期间由 AlienInvasion 主类持有。
  """

  def __init__(self,ai_game):
    """初始化统计信息。
    
    参数：
        ai_game: AlienInvasion 实例，用于访问 settings 等共享对象。
    """
    self.settings=ai_game.settings
    # 初始化可变的统计信息（会在游戏开始/重新开始时重置）
    self.reset_stats()
    # 当前得分（score）和最高分（high_score）
    self.score=0
    self.high_score=0
    # 当前关卡
    self.level=1

  def reset_stats(self):
    """初始化（或重置）在游戏运行期间会变化的统计信息。
    
    调用时机：
        - 游戏第一次启动时
        - 玩家点击 Play 按钮重新开始时
    注意：
        - 最高分 high_score 不在这里重置，而是由外部控制，且可以持久化保存。
    """
    self.score=0
    self.level=1
    # 剩余飞船数从配置中读取
    self.ships_left=self.settings.ship_limit
    # 每次重新开始游戏时，重置动态设置（速度等）
    self.settings.initialize_dynamic_settings()
