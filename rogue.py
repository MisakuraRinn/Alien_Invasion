#coding=GBK
import pygame
import random
class Buff_bar(pygame.sprite.Sprite):
  def __init__(self,img,rect,buff,ai_game):
    super().__init__()
    self.image=img
    self.rect=rect
    self.screen=ai_game.screen
    self.settings=ai_game.settings
    self.color=(20,20,20)
    self.buff=buff[:]
  def draw_buff_bar(self):
    # pygame.draw.rect(self.screen,self.color,self.rect)
    self.screen.blit(self.image,self.rect)
    # print("draw buff bar")
class Rogue:
  def __init__(self,ai_game):
    self.ai_game=ai_game
    self.screen=ai_game.screen
    self.screen_rect=self.screen.get_rect()
    self.settings=ai_game.settings
    self.stats=ai_game.stats
    
    self.text_color=(255,255,255)
    self.font=pygame.font.SysFont(None,35)
    self.weapon_pool=['pistol','machineGun','shotGun','AssaultRifle','GrenadeLaucher']
    self.buff_pool=['max_ammo','shoot_interval','reload_interval','bullet_max_directX','number_of_bullets_in_one_fire','bullet_can_through_aliens_number','bullet_can_explode_number','bullet_can_rebound_number']
    self.initialize()
  def initialize(self):
    self.draw_buff=pygame.sprite.Group()
  def add_buff(self):
    self.second_pool=[]
    # self.third_pool=[]
    for i in range(3):
      cur_weapon=self.weapon_pool[random.randint(0,len(self.weapon_pool)-1)]
      # cur_weapon='pistol'
      print(f"cur_weapon={cur_weapon}\n\n\n\n")
      if(not self.ai_game.gun.weapons[cur_weapon]['can_use']):
        self.second_pool.append([cur_weapon,'can_use',True,f"unlock {cur_weapon}"])
      else:
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
          # add=1
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
        self.second_pool.append([cur_weapon,cur_buff,value,msg])
      # self.prep_buff()
  def prep_buff(self):
    print("new buff")
    self.draw_buff=pygame.sprite.Group()
    for i in range(3):
      print(self.second_pool[i][3])
      buff_image=self.font.render(self.second_pool[i][3],True,self.text_color,(15,0,0))
      buff_rect=buff_image.get_rect()
      buff_rect.x=20
      buff_rect.y=400+i*100
      # self.draw_buff.append([self.buff_image,self.buff_rect])
      buff_bar=Buff_bar(buff_image,buff_rect,self.second_pool[i],self.ai_game)
      self.draw_buff.add(buff_bar)
      
  def show_buff(self):
    for i in self.draw_buff.sprites():
      # print("ckp")
      i.draw_buff_bar()
      # self.screen.blit(self.draw_buff[i][0],self.draw_buff[i][1])
      