#coding=GBK
import sys
import time
import random 
import threading
import pygame
import math
import os, sys

def resource_path(relative_path):
    """资源路径工具函数，兼容 PyInstaller 打包。"""
    if hasattr(sys, '_MEIPASS'):   # PyInstaller 打包后的临时目录
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, relative_path)

# sound_path = resource_path(r"voices\machineGun\MachineGunBurst2.ogg")
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from gun import Gun
from rogue import Rogue

class AlienInvasion:
  """管理游戏资源和行为的主类。"""

  def __init__(self):
    """初始化游戏，并创建所有资源。"""
    pygame.init()
    pygame.mixer.init()

    # 声音通道和音效预留
    self.sound_machinegunBrust=[]             
    self.sound_shotgunBrust=[]
    
    # 多个独立的音频通道，分别用于枪声、装弹、命中等
    self.channel1=pygame.mixer.Channel(0)
    self.channel2=pygame.mixer.Channel(1)
    self.channel3=pygame.mixer.Channel(3)
    # pygame.mixer.music.set_volume(1)

    # 时钟对象，用于帧率控制
    self.clock=pygame.time.Clock()

    # 设置与窗口
    self.settings=Settings(self)
    self.screen=pygame.display.set_mode(
      (self.settings.screen_width,self.settings.screen_height))

    # 命中音效
    self.se_hit=pygame.mixer.Sound(
      resource_path(r"voices/hit/Hit_Metal_HighPitch3.ogg"))

    # 游戏状态标志
    self.game_active=False

    # 统计信息与 UI
    self.stats=GameStats(self)
    self.sb=Scoreboard(self)

    # 玩家相关对象
    self.ship=Ship(self)
    self.gun=Gun(self)
    self.rogue=Rogue(self)

    # 子弹与外星人精灵组
    self.bullets=pygame.sprite.Group()
    self.aliens=pygame.sprite.Group()

    # Play 按钮
    self.play_button=Button(self,"Play")
    
    # 是否处于选择 Buff 状态
    self.is_choosing_buff=False
    
    # 射击相关计时与状态
    self.is_shooting=False
    self.shoot_time1=time.time()

    # 读取最高分（若 data.txt 存在）
    if os.path.exists("data.txt"):      
      with open("data.txt", "r", encoding="GBK") as f:
        self.stats.high_score = int(f.read())
        self.sb.prep_high_score()

    # 换弹计时与状态
    self.reload_time1=time.time()
    self.is_reloading=False

    # 创建第一波外星人
    self._create_fleet()

    # 设置窗口标题
    pygame.display.set_caption("Alien Invasion")

  def run_game(self):
    """开始游戏的主循环。"""  
    while True:
      # 处理事件
      self._check_events()

      # 如果游戏处于进行状态且当前不在选择 Buff，则更新游戏逻辑
      if self.game_active and not self.is_choosing_buff:
        self.ship.update()
        self._update_aliens()
        self._update_bullets()
        self._keep_shooting()

      # 无论是否在游戏中，均需要更新屏幕
      self._update_screen()
      
      # 控制帧率为 60 FPS
      self.clock.tick(60)

  # ------------------- 事件处理 -------------------

  def _check_events(self):
    """响应按键和鼠标事件。"""
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        # 直接退出（这里不写入高分，真正写入在按 Q 时触发）
        sys.exit()
      elif event.type==pygame.KEYDOWN:
        self._check_keydown_events(event)
      elif event.type==pygame.KEYUP:
        self._check_keyup_events(event)
      elif event.type==pygame.MOUSEBUTTONDOWN:
        mouse_pos=pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)
        self._check_buff_bar_button(mouse_pos)
  
  # ------------------- 屏幕更新 -------------------

  def _update_screen(self):
    """重绘屏幕上的所有元素，并切换到新屏幕。"""
    # 填充背景色
    self.screen.fill(self.settings.bg_color)

    # 外星人、飞船、子弹
    self.aliens.draw(self.screen)
    self.ship.blitme()
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    
    # 若游戏未激活，显示 Play 按钮
    if not self.game_active:
      self.play_button.draw_button()
    
    # 显示计分板、生命、弹药
    self.sb.show_score()

    # 若处于选择 Buff 状态，则在屏幕上绘制 Buff 选项
    if self.is_choosing_buff:
      self.rogue.show_buff()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
    
  # ------------------- 子弹相关 -------------------

  def _update_bullets(self):
    """更新所有子弹的位置，并处理越界和碰撞。"""
    self.bullets.update()

    # 处理子弹越界与反弹逻辑
    for bullet in self.bullets.copy():
        # 如果没有反弹次数且完全飞出屏幕，则触发爆炸碎片并删除
        if bullet.bullet_can_rebound_number==0 and (
          bullet.rect.bottom<=0 or
          bullet.rect.top>=self.settings.screen_height or
          bullet.rect.right<=0 or
          bullet.rect.left>=self.settings.screen_width):
          for i in range(self.gun.current_gun['bullet_can_explode_number']):
            if len(self.bullets)<self.settings.bullet_allowed and not bullet.is_piece:
              self._boom(bullet)
          self.bullets.remove(bullet)
        # 上下边界反弹
        elif (bullet.rect.bottom<=0 or bullet.rect.top>=self.settings.screen_height):
          bullet.directY*=-1
          bullet.bullet_can_rebound_number-=1
        # 左右边界反弹
        elif bullet.rect.right<=0 or bullet.rect.left>=self.settings.screen_width:
          bullet.directX*=-1
          bullet.bullet_can_rebound_number-=1

    # 检查子弹与外星人的碰撞
    self._check_bullet_alien_collisions()

  def _check_bullet_alien_collisions(self):
    """处理子弹与外星人的碰撞，包括得分、血量、爆炸等效果。"""
    # groupcollide: 子弹组 vs 外星人组；False 表示不立即删除
    collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,False,False)
    if collisions:
      # 播放命中音效
      self.channel3.play(self.se_hit)
      for bullet,aliens in collisions.copy().items():
        # 每击中一个外星人，加固定分数
        self.stats.score+=self.settings.alien_points*len(aliens)

        # 子弹耐久（穿透次数）减一
        bullet.health-=1
        if bullet.health==0:
          # 若子弹用尽耐久，生成爆炸碎片并删除
          for i in range(self.gun.current_gun['bullet_can_explode_number']):
            if len(self.bullets)<self.settings.bullet_allowed and not bullet.is_piece:
              self._boom(bullet)
          self.bullets.remove(bullet)

        # 处理被击中的外星人血量
        for i in aliens:
          i.health-=1
          if i.health==0:
            self.aliens.remove(i)

      # 更新分数显示，并检查是否刷新了最高分
      self.sb.prep_score()
      self.sb.check_high_score()

    # 如果外星人全部被消灭，则生成新一波并触发升级选择
    if not self.aliens:
      # self.bullets.empty()
      self._create_fleet()
      self.stats.level+=1
      self.settings.increase_speed()
      self.sb.prep_level()
      # 进入选择 Buff 状态
      self.is_choosing_buff=True
      self.rogue.add_buff()
      self.rogue.prep_buff()

  def _boom(self,bullet):
    """在子弹死亡时，生成若干碎片子弹，实现爆炸效果。"""
    new_piece=Bullet(self)
    dir=random.randint(0,1)
    new_piece.is_piece=True
    new_piece.health=1 
    new_piece.bullet_max_directX=1
    # 随机散射方向，保证单位长度
    new_piece.directX=random.uniform(-1,1)
    new_piece.directY=math.sqrt(1- new_piece.directX* new_piece.directX)
    if dir==0:new_piece.directY*=-1
    # 在原子弹附近随机偏移生成碎片
    new_piece.x=bullet.x+random.uniform(-50,50)*new_piece.directX
    new_piece.y=bullet.y+random.uniform(-50,50)*new_piece.directY
    self.bullets.add(new_piece)
    
  # ------------------- 外星人相关 -------------------

  def _check_aliens_bottom(self):
    """检查是否有外星人到达屏幕底部。"""
    for alien in self.aliens.sprites():
      if alien.rect.bottom>=self.settings.screen_height:
        print("到达边界")
        self._ship_hit()
        break
  
  def _update_aliens(self):
    """更新外星人群的整体行为。"""
    # 先检查是否有外星人到达左右边界
    self._check_fleet_edges() 
    # 更新每个外星人的移动
    self.aliens.update()

    # 检测飞船与外星人的直接碰撞
    if pygame.sprite.spritecollideany(self.ship,self.aliens):
      self._ship_hit()

    # 检查外星人是否触底
    self._check_aliens_bottom()
  
  def _ship_hit(self):
    """响应飞船与外星人碰撞，或外星人到达底部的事件。"""
    if self.stats.ships_left>0:
      # 扣除一条命
      self.stats.ships_left-=1
      self.sb.prep_ships()
      # 清空子弹和外星人并重新创建
      self.bullets.empty()
      self.aliens.empty()
      self._create_fleet()
      self.ship.center_ship()
      # 暂停片刻给玩家缓冲
      time.sleep(0.5)
    else :
      # 没有生命了，游戏结束
      self.game_active=False
      pygame.mouse.set_visible(True)
  
  # ------------------- Buff 选择与按钮 -------------------

  def _check_buff_bar_button(self,mouse_pos):
    """检查玩家是否点击了某个 Buff 选项。"""
    print("ckp")
    for i in self.rogue.draw_buff.sprites():
      buff_bar_clicked=i.rect.collidepoint(mouse_pos)
      if buff_bar_clicked and self.is_choosing_buff:
        print("ckp2")
        buff=i.buff   # [weapon, key, value, msg]
        # 升级武器属性
        self.gun.weapon_level_up(buff[0],buff[1],buff[2])
        self.is_choosing_buff=False
        # 清空当前 Buff 显示
        self.rogue.draw_buff.empty()
        break

  def _check_play_button(self,mouse_pos):
    """在玩家点击 Play 按钮时开始游戏。"""
    button_clicked=self.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not self.game_active:
      # 重置统计信息与 UI
      self.stats.reset_stats()
      self.sb.prep_score()
      self.sb.prep_ships()
      self.sb.prep_level()
      self.sb.prep_ammo()
      # 重置武器系统的动态设置
      self.gun.initialize_dynamic_settings()
      self.game_active=True
      # 清空子弹与外星人，并重新生成
      self.bullets.empty()
      self.aliens.empty()
      self._create_fleet()
      self.ship.center_ship()
      # pygame.mouse.set_visible(False)

  # ------------------- 射击与换弹 -------------------

  def _keep_shooting(self):
    """持续射击逻辑：根据时间间隔和弹药状态决定是否发射子弹或开始换弹。"""
    self.shoot_time2=time.time()
    
    # 正在射击、未在换弹、间隔已到、且还有子弹
    if (self.is_shooting and not self.is_reloading and
        (self.shoot_time2-self.shoot_time1>self.gun.current_gun['shoot_interval']) and
        self.settings.ammo_left>0):
      print("shoot")
      self._fire_bullet()
      self.shoot_time1=self.shoot_time2
    elif self.is_shooting and self.settings.ammo_left==0 and not self.is_reloading:
      # 没子弹了，自动开始换弹
      print("reloading")
      self._reload()
      self.is_reloading=True
      
  def _reload(self):
    """使用 threading.Timer 模拟逐颗装填的换弹过程。"""
    if(self.settings.ammo_left<self.gun.current_gun['max_ammo']):
      # 播放换弹音效
      self.channel2.play(self.gun.current_gun['se_reload'][0])
      self.settings.ammo_left+=1
      self.sb.prep_ammo()
      # 到时间后再次调用 _reload，直到装满
      timer=threading.Timer(self.gun.current_gun['reload_interval'],self._reload)
      timer.start()
    else :
      # 装填完毕，稍微延迟后结束换弹状态
      timer=threading.Timer(0.75,self._change_is_reloading)
      timer.start()
      print("finish reload")   

  def _change_is_reloading(self):
    """在延迟之后结束换弹状态。"""
    self.is_reloading=False

  def _fire_bullet(self):
    """根据当前武器参数发射子弹。"""
    if len(self.bullets)<self.settings.bullet_allowed:                
      # 播放枪声（从该武器的射击音效池中随机选一个）
      self.channel1.play(
        self.gun.current_gun['se_shot'][random.randint(0,-1+len(self.gun.current_gun['se_shot']))])
      # 子弹数量减一，并更新 UI
      self.settings.ammo_left-=1
      self.sb.prep_ammo()
      # 按照 number_of_bullets_in_one_fire 生成多发子弹
      for i in range(self.gun.current_gun['number_of_bullets_in_one_fire']):
        new_bullet=Bullet(self)
        self.bullets.add(new_bullet)

  # ------------------- 外星人舰队创建 -------------------

  def _create_fleet(self):
    """创建一整群外星人，随机分布在屏幕上方区域。"""
    alien=Alien(self)
    alien_width,alien_height=alien.rect.size
    # 从屏幕上半部分逐行随机生成
    current_x,current_y=alien_width,-self.settings.screen_height/2
    while current_y <0:
      while current_x <(self.settings.screen_width-2*alien_width):
        self._create_alien(current_x,current_y)
        # 横向间距随等级变化
        current_x+=random.uniform(5/self.stats.level,5)*alien_width
      current_x=alien_width
      current_y+=random.randint(1,5)*alien_height
  
  def _create_alien(self,x_position,y_position):
    """创建单个外星人并放置在指定位置。"""
    new_alien=Alien(self) 
    new_alien.x=x_position
    new_alien.rect.x=x_position
    new_alien.rect.y=y_position
    self.aliens.add(new_alien)
    
  def _check_fleet_edges(self):
    """如果有外星人到达边缘，则整群下移并改变方向。"""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break
        
  def _change_fleet_direction(self):
    """将整群外星人向下移动一行，并改变移动方向。"""
    for alien in self.aliens.sprites():
      alien.rect.y+=self.settings.fleet_drop_speed
    self.settings.fleet_direction*=-1
    
  # ------------------- 键盘事件 -------------------

  def _check_keydown_events(self,event):
    """响应按键按下事件。"""
    if event.key ==pygame.K_RIGHT:
      self.ship.moving_right=True
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=True
    if event.key==pygame.K_q:
      # 按 Q 退出前，写入最高分到文件
      print("exit")
      with open("data.txt", "w", encoding="GBK") as f:
        f.write(str(self.stats.high_score))
      sys.exit()
    if event.key==pygame.K_SPACE and self.game_active:
      self.is_shooting=True
    # 数字键 1~5 切换武器（前提是该武器已解锁）
    if event.key==pygame.K_1 and self.gun.weapons["pistol"]["can_use"] and self.game_active:
      self.gun.change_weapon("pistol")
    if event.key==pygame.K_2 and self.gun.weapons["machineGun"]["can_use"] and self.game_active:
      self.gun.change_weapon("machineGun")
    if event.key==pygame.K_3 and self.gun.weapons["shotGun"]["can_use"] and self.game_active:
      self.gun.change_weapon("shotGun")
    if event.key==pygame.K_4 and self.gun.weapons["AssaultRifle"]["can_use"] and self.game_active:
      self.gun.change_weapon("AssaultRifle")
    if event.key==pygame.K_5 and self.gun.weapons["GrenadeLaucher"]["can_use"] and self.game_active:
      self.gun.change_weapon("GrenadeLaucher")
    
  def _check_keyup_events(self,event):
    """响应按键松开事件。"""
    if event.key==pygame.K_RIGHT:
      self.ship.moving_right=False
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=False
    if event.key==pygame.K_SPACE:
      self.is_shooting=False

# 只在本文件直接运行时启动游戏
if __name__=="__main__":
  ai=AlienInvasion()
  ai.run_game()
