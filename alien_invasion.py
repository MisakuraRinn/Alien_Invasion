#coding=GBK
import sys
import time
import random 
import threading
import pygame
import math
import os, sys

def resource_path(relative_path):
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
  """管理游戏资源和行为"""
  def __init__(self):
    pygame.init()
    pygame.mixer.init()
    self.sound_machinegunBrust=[]             
    
    self.sound_shotgunBrust=[]
    
    self.channel1=pygame.mixer.Channel(0)
    self.channel2=pygame.mixer.Channel(1)
    self.channel3=pygame.mixer.Channel(3)
    # pygame.mixer.music.set_volume(1)
    self.clock=pygame.time.Clock()
    self.settings=Settings(self)
    self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
    self.se_hit=pygame.mixer.Sound(resource_path(r"voices/hit/Hit_Metal_HighPitch3.ogg"))
    self.game_active=False
    self.stats=GameStats(self)
    self.sb=Scoreboard(self)
    self.ship=Ship(self)
    self.gun=Gun(self)
    self.rogue=Rogue(self)
    self.bullets=pygame.sprite.Group()
    self.aliens=pygame.sprite.Group()
    self.play_button=Button(self,"Play")
    
    self.is_choosing_buff=False
    
    self.is_shooting=False
    self.shoot_time1=time.time()
    if os.path.exists("data.txt"):      
      with open("data.txt", "r", encoding="GBK") as f:
        self.stats.high_score = int(f.read())
        self.sb.prep_high_score()
    self.reload_time1=time.time()
    self.is_reloading=False
    self._create_fleet()
    # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    # self.settings.screen_width=self.screen.get_rect().width
    # self.settings.screen_height=self.screen.get_rect().height
    pygame.display.set_caption("Alien Invasion")
    # self.bg_color=(2)
  def run_game(self):
    """开始游戏的主循环"""  
    while True:
      # 监听事件
      # sys("cls")
      self._check_events()
      if self.game_active and not self.is_choosing_buff:
        self.ship.update()
        self._update_aliens()
        self._update_bullets()
        self._keep_shooting()
      self._update_screen()
      
      
      # if self.is_shooting:self._fire_bullet()
      
      self.clock.tick(60)
      # print(len(self.bullets))
  def _check_events(self):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        sys.exit()
      elif event.type==pygame.KEYDOWN:
        self._check_keydown_events(event)
      elif event.type==pygame.KEYUP:
        self._check_keyup_events(event)
      elif event.type==pygame.MOUSEBUTTONDOWN:
        mouse_pos=pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)
        self._check_buff_bar_button(mouse_pos)
  
  def _update_screen(self):
    self.screen.fill(self.settings.bg_color)
    self.aliens.draw(self.screen)
    self.ship.blitme()
    for bullet in self.bullets.sprites():
      bullet.draw_bullet()
    
    if not self.game_active:
      self.play_button.draw_button()
    
    self.sb.show_score()
    if self.is_choosing_buff:
      self.rogue.show_buff()
    pygame.display.flip()
    
      
  def _update_bullets(self):
    self.bullets.update()
    for bullet in self.bullets.copy():
        if bullet.bullet_can_rebound_number==0 and (bullet.rect.bottom<=0 or bullet.rect.top>=self.settings.screen_height or bullet.rect.right<=0 or bullet.rect.left>=self.settings.screen_width):
          for i in range(self.gun.current_gun['bullet_can_explode_number']):
            if len(self.bullets)<self.settings.bullet_allowed and not bullet.is_piece:
              self._boom(bullet)
          self.bullets.remove(bullet)
        elif (bullet.rect.bottom<=0 or bullet.rect.top>=self.settings.screen_height):
          bullet.directY*=-1
          bullet.bullet_can_rebound_number-=1
        elif bullet.rect.right<=0 or bullet.rect.left>=self.settings.screen_width:
          bullet.directX*=-1
          bullet.bullet_can_rebound_number-=1
    self._check_bullet_alien_collisions()

  def _check_bullet_alien_collisions(self):
    """响应碰装"""
    collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,False,False)
    if collisions:
      self.channel3.play(self.se_hit)
      for bullet,aliens in collisions.copy().items():
        # print(f"bullet.health{bullet.health}")
        self.stats.score+=self.settings.alien_points*len(aliens)
        bullet.health-=1
        if bullet.health==0:
          for i in range(self.gun.current_gun['bullet_can_explode_number']):
            if len(self.bullets)<self.settings.bullet_allowed and not bullet.is_piece:
              self._boom(bullet)
          self.bullets.remove(bullet)
        for i in aliens:
          i.health-=1
          if i.health==0:
            self.aliens.remove(i)
      # self.stats.score+=self.settings.alien_points
      self.sb.prep_score()
      self.sb.check_high_score()
    if not self.aliens:
      # self.bullets.empty()
      self._create_fleet()
      self.stats.level+=1
      self.settings.increase_speed()
      self.sb.prep_level()
      # self.game_active=False
      self.is_choosing_buff=True
      self.rogue.add_buff()
      self.rogue.prep_buff()
  def _boom(self,bullet):
    new_piece=Bullet(self)
    dir=random.randint(0,1)
    new_piece.is_piece=True
    new_piece.health=1 
    # new_piece.rect.x=bullet.x-random.uniform(-5,5)
    # new_piece.rect.y=bullet.y-random.uniform(-5,5)
    new_piece.bullet_max_directX=1
    new_piece.directX=random.uniform(-1,1)
    new_piece.directY=math.sqrt(1- new_piece.directX* new_piece.directX)
    if dir==0:new_piece.directY*=-1;
    new_piece.x=bullet.x+random.uniform(-50,50)*new_piece.directX
    new_piece.y=bullet.y+random.uniform(-50,50)*new_piece.directY
    self.bullets.add(new_piece)
    
    
  def _check_aliens_bottom(self):
    for alien in self.aliens.sprites():
      if alien.rect.bottom>=self.settings.screen_height:
        print("到达边界")
        self._ship_hit()
        break
  
  def _update_aliens(self):
    """更新外星舰队中所有外星人的位置"""
    self._check_fleet_edges() 
    self.aliens.update()
    if pygame.sprite.spritecollideany(self.ship,self.aliens):
      self._ship_hit()
      # print("ship hit")
    self._check_aliens_bottom()
  
  def _ship_hit(self):
    """响应飞船和外星人的碰撞"""
    if self.stats.ships_left>0:
      self.stats.ships_left-=1
      self.sb.prep_ships()
      self.bullets.empty()
      self.aliens.empty()
      self._create_fleet()
      self.ship.center_ship()
      time.sleep(0.5)
    else :
      self.game_active=False
      pygame.mouse.set_visible(True)
  
  def _check_buff_bar_button(self,mouse_pos):
    print("ckp")
    for i in self.rogue.draw_buff.sprites():
      buff_bar_clicked=i.rect.collidepoint(mouse_pos)
      if buff_bar_clicked and self.is_choosing_buff:
        print("ckp2")
        buff=i.buff
        self.gun.weapon_level_up(buff[0],buff[1],buff[2])
        self.is_choosing_buff=False
        self.rogue.draw_buff.empty()
        # self.rogue.prep_buff()
        break
  def _check_play_button(self,mouse_pos):
    button_clicked=self.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not self.game_active:
      self.stats.reset_stats()
      self.sb.prep_score()
      self.sb.prep_ships()
      self.sb.prep_level()
      self.sb.prep_ammo()
      self.gun.initialize_dynamic_settings()
      self.game_active=True
      self.bullets.empty()
      self.aliens.empty()
      
      self._create_fleet()
      self.ship.center_ship()
      # pygame.mouse.set_visible(False)

  def _keep_shooting(self):
    self.shoot_time2=time.time()
    
    if self.is_shooting and not self.is_reloading and (self.shoot_time2-self.shoot_time1>self.gun.current_gun['shoot_interval']) and self.settings.ammo_left>0:
      print("shoot")
      self._fire_bullet()
      self.shoot_time1=self.shoot_time2
    elif self.is_shooting and self.settings.ammo_left==0 and not self.is_reloading:
      print("reloading")
      
      self._reload()
      self.is_reloading=True
      
  def _reload(self):
    
    if(self.settings.ammo_left<self.gun.current_gun['max_ammo']):
      self.channel2.play(self.gun.current_gun['se_reload'][0])
      self.settings.ammo_left+=1
      self.sb.prep_ammo()
      timer=threading.Timer(self.gun.current_gun['reload_interval'],self._reload)
      timer.start()
    else :
      timer=threading.Timer(0.75,self._change_is_reloading)
      timer.start()
      # self.is_reloading=False
      print("finish reload")   
  def _change_is_reloading(self):
    self.is_reloading=False
  def _fire_bullet(self):
    if len(self.bullets)<self.settings.bullet_allowed:                
      # self.channel1.play(self.sound_machinegunBrust[random.randint(0,len(self.sound_machinegunBrust)-1)])
      self.channel1.play(self.gun.current_gun['se_shot'][random.randint(0,-1+len(self.gun.current_gun['se_shot']))])
      self.settings.ammo_left-=1
      # if(self.settings.ammo_left)
      self.sb.prep_ammo()
      for i in range(self.gun.current_gun['number_of_bullets_in_one_fire']):
        new_bullet=Bullet(self)
        self.bullets.add(new_bullet)
        
  def _create_fleet(self):
    """创建一个外星舰队"""
    # self.aliens.add(alien)
    alien=Alien(self)
    alien_width,alien_height=alien.rect.size
    current_x,current_y=alien_width,-self.settings.screen_height/2
    while current_y <0:
      while current_x <(self.settings.screen_width-2*alien_width):
        self._create_alien(current_x,current_y)
        current_x+=random.uniform(5/self.stats.level,5)*alien_width
      current_x=alien_width
      current_y+=random.randint(1,5)*alien_height
      # print(current_y)
  
  def _create_alien(self,x_position,y_position):
    """创建一个外星人，并将其加入外星舰队"""
    new_alien=Alien(self) 
    new_alien.x=x_position
    new_alien.rect.x=x_position
    new_alien.rect.y=y_position
    self.aliens.add(new_alien)
    
  def _check_fleet_edges(self):
    """在边缘的处理情况"""
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self._change_fleet_direction()
        break
        
  def _change_fleet_direction(self):
    """将整个舰队下移，并改变方向"""
    for alien in self.aliens.sprites():
      alien.rect.y+=self.settings.fleet_drop_speed
    self.settings.fleet_direction*=-1
    
    
  def _check_keydown_events(self,event):
    """响应按下"""
    if event.key ==pygame.K_RIGHT:
      self.ship.moving_right=True
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=True
    if event.key==pygame.K_q:
      print("exit")
      with open("data.txt", "w", encoding="GBK") as f:
        f.write(str(self.stats.high_score))
      sys.exit()
    if event.key==pygame.K_SPACE and self.game_active:
      self.is_shooting=True
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
    if event.key==pygame.K_RIGHT:
      self.ship.moving_right=False
    if event.key==pygame.K_LEFT:
      self.ship.moving_left=False
    if event.key==pygame.K_SPACE:
      self.is_shooting=False
if __name__=="__main__":
  ai=AlienInvasion()
  ai.run_game()
