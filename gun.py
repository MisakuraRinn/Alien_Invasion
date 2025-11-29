#coding=GBK
class Gun:
  def __init__(self,ai_game):
    self.settings=ai_game.settings
    self.stats=ai_game.stats
    self.initialize_dynamic_settings()
  def initialize_dynamic_settings(self):
    self.weapons={
      'pistol':{
        'can_use':True,
        'max_ammo':12,
        'shoot_interval':0.5,
        'reload_interval':0.25,
        'bullet_max_directX':0.2,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':0,
        'bullet_can_rebound_number':0
        
        },
      'machineGun':{
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
        'max_ammo':1,
        'shoot_interval':3,
        'reload_interval':3,
        'bullet_max_directX':0.1,
        'number_of_bullets_in_one_fire':1,
        'bullet_can_through_aliens_number':1,
        'bullet_can_explode_number':15,
        'bullet_can_rebound_number':0
      }
    }
    self.current_gun=self.weapons['AssaultRifle']
  def weapon_level_up(self,weapon,key,value):
    """升级武器，升级武器属性，升级数值"""
    # self.settings.ammo_left=0
  def change_weapon(self,weapon):
    pass