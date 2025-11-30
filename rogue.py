#coding=GBK
import pygame
import random

class Buff_bar(pygame.sprite.Sprite):
  """用于在屏幕上显示单条 Buff 选项的精灵。"""

  def __init__(self,img,rect,buff,ai_game):
    """img 是渲染好的文字图像，rect 决定位置，buff 存储具体升级信息。"""
    super().__init__()
    self.image=img            # 显示的文字/背景图
    self.rect=rect            # 显示位置矩形
    self.screen=ai_game.screen
    self.settings=ai_game.settings
    self.color=(20,20,20)
    # buff 是一个列表：[weapon_name, key, value, msg]
    self.buff=buff[:]

  def draw_buff_bar(self):
    """将 Buff 图像绘制到屏幕上。"""
    #pygame.draw.rect(self.screen,self.color,self.rect)
    self.screen.blit(self.image,self.rect)
    # print("draw buff bar")


class Rogue:
  """Roguelike 升级系统：关卡结束后随机提供 Buff 供玩家选择。"""

  def __init__(self,ai_game):
    self.ai_game=ai_game
    self.screen=ai_game.screen
    self.screen_rect=self.screen.get_rect()
    self.settings=ai_game.settings
    self.stats=ai_game.stats
    
    self.text_color=(255,255,255)
    # 使用稍小字体，避免过宽
    self.font=pygame.font.SysFont(None,35)

    # 所有武器池
    self.weapon_pool=['pistol','machineGun','shotGun','AssaultRifle','GrenadeLaucher']
    # Buff 类型池（可升级的属性）
    self.buff_pool=[
      'max_ammo','shoot_interval','reload_interval',
      'bullet_max_directX','number_of_bullets_in_one_fire',
      'bullet_can_through_aliens_number','bullet_can_explode_number',
      'bullet_can_rebound_number'
    ]
    self.initialize()

  def initialize(self):
    """初始化用于绘制的 Buff 精灵组。"""
    self.draw_buff=pygame.sprite.Group()

  def add_buff(self):
    """随机生成 3 个升级选项并保存到 second_pool 中。
    
    规则：
        - 随机选择一个武器；
        - 若该武器尚未解锁，则给出“解锁武器”作为 Buff；
        - 否则随机选择一个属性提升，并生成对应的文字描述。
    """
    self.second_pool=[]
    # self.third_pool=[]
    for i in range(3):
      #随机抽一个武器
      cur_weapon=self.weapon_pool[random.randint(0,len(self.weapon_pool)-1)]
      # cur_weapon='pistol'
      print(f"cur_weapon={cur_weapon}\n\n\n\n")
      if(not self.ai_game.gun.weapons[cur_weapon]['can_use']):
        # 如果武器尚未可用，则给解锁武器的 Buff
        self.second_pool.append([cur_weapon,'can_use',True,f"unlock {cur_weapon}"])
      else:
        # 否则从属性池中抽一个进行数值提升
        cur_buff=self.buff_pool[random.randint(0,len(self.buff_pool)-1)]
        value=0
        msg=cur_weapon+": "
        if cur_buff=='max_ammo':
          value=self.ai_game.gun.weapons[cur_weapon]['max_ammo']+5
          msg+='Increase weapon magazine capacity'
        elif cur_buff=='shoot_interval':
          value=self.ai_game.gun.weapons[cur_weapon]['shoot_interval']*0.9
          msg+='Shorten shooting interval'
        elif cur_buff=='reload_interval':
          value=self.ai_game.gun.weapons[cur_weapon]['reload_interval']*0.9
          msg+='Reduce reload time'
        elif cur_buff=='bullet_max_directX':
          value=self.ai_game.gun.weapons[cur_weapon]['bullet_max_directX']
          # 这里既可能增大散射角，也可能减小散射角
          if random.randint(0,1)==1:
            value*=1.1
            msg+="Larger shooting spread"
          else:
            value*=0.9
            msg+="Smaller shooting spread"
          
        elif cur_buff=='number_of_bullets_in_one_fire':
          value=self.ai_game.gun.weapons[cur_weapon]['number_of_bullets_in_one_fire']+1
          msg+="Fire more bullets at once"
        elif cur_buff=='bullet_can_through_aliens_number':
          value=self.ai_game.gun.weapons[cur_weapon]['bullet_can_through_aliens_number']+1
          msg+="Increase bullet damage and penetration"
        elif cur_buff=='bullet_can_explode_number':
          value=self.ai_game.gun.weapons[cur_weapon]['bullet_can_explode_number']+1
          msg+="The bullet can produce more fragments after exploding."
        elif cur_buff=='bullet_can_rebound_number':
          value=self.ai_game.gun.weapons[cur_weapon]['bullet_can_rebound_number']+1
          msg+="Bullets have stronger ricochet capability"
        # 把 [武器名, 属性名, 新值, 描述文本] 加入候选池
        self.second_pool.append([cur_weapon,cur_buff,value,msg])
      # self.prep_buff()

  def prep_buff(self):
    """根据 second_pool 中的信息生成可点击的 Buff_bar 精灵。"""
    print("new buff")
    self.draw_buff=pygame.sprite.Group()
    for i in range(3):
      print(self.second_pool[i][3])
      # 渲染文字图像，背景使用深色以区分
      buff_image=self.font.render(
        self.second_pool[i][3],True,self.text_color,(15,0,0))
      buff_rect=buff_image.get_rect()
      buff_rect.x=20
      buff_rect.y=400+i*100
      # 创建 Buff_bar 精灵，并加入组
      buff_bar=Buff_bar(buff_image,buff_rect,self.second_pool[i],self.ai_game)
      self.draw_buff.add(buff_bar)
      
  def show_buff(self):
    """在屏幕上绘制所有 Buff 选项。"""
    for i in self.draw_buff.sprites():
      # print("ckp")
      i.draw_buff_bar()
      # self.screen.blit(self.draw_buff[i][0],self.draw_buff[i][1])
