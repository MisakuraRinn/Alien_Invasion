#coding=GBK
import pygame
import os, sys

def resource_path(relative_path):
    """资源路径函数，兼容打包与开发环境。"""
    if hasattr(sys, '_MEIPASS'):   # PyInstaller 打包后的临时目录
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, relative_path)

class Gun:
  """武器系统类：管理多种武器的参数、音效以及切换与升级。"""

  def __init__(self,ai_game):
    self.ai_game=ai_game
    self.settings=ai_game.settings
    self.stats=ai_game.stats
    self.sb=ai_game.sb

    # 初始化武器配置和音效
    self.initialize_dynamic_settings()

    # 每种武器都使用一个字典记录属性
    self.weapons={
      'pistol':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':True,
        'max_ammo':12,
        'shoot_interval':0.5,
        'reload_interval':0.05,
        'bullet_max_directX':0.2,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        
        },
      'machineGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':30,
        'shoot_interval':0.1,
        'reload_interval':0.05,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':2,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'shotGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':0.5,
        'bullet_max_directX':0.5,
        'number_of_bullets_in_one_fire':5,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'AssaultRifle':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':1,
        'bullet_max_directX':0.05,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':10,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'GrenadeLaucher':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'max_ammo':1,
        'shoot_interval':3,
        'reload_interval':3,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':100,
        'bullet_can_rebound_number':0
      }
    }

    # 载入各种武器的音效资源
    for i in range(1,8):
      self.weapons["pistol"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/pistol/Gun_Pistol_Shot{i}.ogg")))
    self.weapons["pistol"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/pistol/Gun_Reload_Weapon07.ogg")))
    self.weapons["pistol"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/pistol/Gun_DrawSelect_Pistol3.ogg")))
    
    self.weapons["machineGun"]['se_shot'].append(
      pygame.mixer.Sound(resource_path(r"voices/machineGun/K_MachineGun01.ogg")))
    self.weapons["machineGun"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/machineGun/Gun_Reload_Weapon03.ogg")))
    self.weapons["machineGun"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/machineGun/Gun_DrawSelect_Weapon08.ogg")))
    
    for i in range(1,8):
      self.weapons["shotGun"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/shotGun/Shotgun_Shot{i}.ogg")))
    self.weapons["shotGun"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/shotGun/Gun_Reload_Weapon02.ogg")))
    self.weapons["shotGun"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/shotGun/Gun_DrawSelect_Weapon02.ogg")))
    
    for i in range(1,3):
      self.weapons["AssaultRifle"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/AssaultRifle/Gun_AssaultRifle_PowerShot{i}.ogg")))
    self.weapons["AssaultRifle"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/AssaultRifle/Gun_Reload_Weapon19.ogg")))
    self.weapons["AssaultRifle"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/AssaultRifle/Gun_DrawSelect_Weapon06.ogg")))
    
    for i in range(1,9):
      self.weapons["GrenadeLaucher"]["se_shot"].append(
        pygame.mixer.Sound(resource_path(rf"voices/GrenadeLaucher/GrenadeLauncher_Shot{i}.ogg")))
    self.weapons["GrenadeLaucher"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/GrenadeLaucher/Gun_Reload_Weapon04.ogg")))
    self.weapons["GrenadeLaucher"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/GrenadeLaucher/Gun_DrawSelect_Weapon10.ogg")))
    print("ckp")

  def initialize_dynamic_settings(self):
    """重置武器的动态属性（用于重新开始游戏）。"""
    self.weapons={
      'pistol':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':True,
        'max_ammo':12,
        'shoot_interval':0.3,
        'reload_interval':0.03,
        'bullet_max_directX':0.15,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        
        },
      'machineGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':30,
        'shoot_interval':0.1,
        'reload_interval':0.05,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':2,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'shotGun':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':0.5,
        'bullet_max_directX':0.5,
        'number_of_bullets_in_one_fire':5,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'AssaultRifle':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':5,
        'shoot_interval':1,
        'reload_interval':1,
        'bullet_max_directX':0.05,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':20,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        },
      'GrenadeLaucher':{
        'se_select':[],
        'se_shot':[],
        'se_reload':[],
        'can_use':False,
        'max_ammo':3,
        'shoot_interval':1,
        'reload_interval':1,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':5,
        'bullet_can_rebound_number':1
      }
    }

    # 重新载入音效（与 __init__ 中逻辑类似）
    for i in range(1,8):
      self.weapons["pistol"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/pistol/Gun_Pistol_Shot{i}.ogg")))
    self.weapons["pistol"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/pistol/Gun_Reload_Weapon07.ogg")))
    self.weapons["pistol"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/pistol/Gun_DrawSelect_Pistol3.ogg")))
    
    self.weapons["machineGun"]['se_shot'].append(
      pygame.mixer.Sound(resource_path(r"voices/machineGun/K_MachineGun01.ogg")))
    self.weapons["machineGun"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/machineGun/Gun_Reload_Weapon03.ogg")))
    self.weapons["machineGun"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/machineGun/Gun_DrawSelect_Weapon08.ogg")))
    
    for i in range(1,8):
      self.weapons["shotGun"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/shotGun/Shotgun_Shot{i}.ogg")))
    self.weapons["shotGun"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/shotGun/Gun_Reload_Weapon02.ogg")))
    self.weapons["shotGun"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/shotGun/Gun_DrawSelect_Weapon02.ogg")))
    
    for i in range(1,3):
      self.weapons["AssaultRifle"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/AssaultRifle/Gun_AssaultRifle_PowerShot{i}.ogg")))
    self.weapons["AssaultRifle"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/AssaultRifle/Gun_Reload_Weapon19.ogg")))
    self.weapons["AssaultRifle"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/AssaultRifle/Gun_DrawSelect_Weapon06.ogg")))
    
    for i in range(1,9):
      self.weapons["GrenadeLaucher"]['se_shot'].append(
        pygame.mixer.Sound(resource_path(rf"voices/GrenadeLaucher/GrenadeLauncher_Shot{i}.ogg")))
    self.weapons["GrenadeLaucher"]['se_reload'].append(
      pygame.mixer.Sound(resource_path(r"voices/GrenadeLaucher/Gun_Reload_Weapon04.ogg")))
    self.weapons["GrenadeLaucher"]['se_select'].append(
      pygame.mixer.Sound(resource_path(r"voices/GrenadeLaucher/Gun_DrawSelect_Weapon10.ogg")))
    # 当前武器默认是 pistol
    self.current_gun=self.weapons['pistol']
    
  def weapon_level_up(self,weapon,key,value):
    """升级武器属性：直接修改 weapons 字典里的数值。"""
    self.weapons[weapon][key]=value

  def change_weapon(self,weapon):
    """切换当前使用的武器。
    
    行为：
        - 播放切枪音效；
        - 清空当前子弹 UI（ammo_left 设为 0，由换弹重新装填）。
    """
    self.current_gun=self.weapons[weapon]
    self.ai_game.channel1.play(self.current_gun['se_select'][0])
    
    self.settings.ammo_left=0
    self.sb.prep_ammo()
