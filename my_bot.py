from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType
import time
import random

class Bot:
  def get_name(self):
      return "MAGLEVA uden hop"
  
  def get_current_hand(obs: Observation):
     return obs.get_my_hand_type()

  def act(self, obs: Observation):

    print("my player info", obs.get_my_player_info())
    print("my hand type", obs.get_my_hand_type())
    my_money = obs.get_my_player_info().stack
    hand_val = obs.get_my_hand_type()
    actions = obs.get_actions_this_round() 
    print("actions this round", actions)
    min_raise = obs.get_min_raise()
    print("min raise", min_raise)
    
    did_anyone_raise = False
    pocketpairs = False

    if obs.current_round == 0 and hand_val == 2:
      pocketpairs = True

    for actioninfo in actions:
       print("actioninfo", actioninfo)
       if actioninfo.action != 1 or actioninfo.action != 0:
          did_anyone_raise = True


    are_we_big_blind = obs.my_index == 1
    are_we_small_blind = obs.my_index == 0
    free_check = obs.get_call_size() == 0

    match obs.current_round:
      case 0: # preflop
        if are_we_big_blind: #We are big blind
          if free_check:
            return 1

        if are_we_small_blind: #We are small blind
          if free_check:
            return 1

        if pocketpairs:
          if did_anyone_raise and obs.get_call_size() < my_money:
            return 1 # call 
          return min_raise
        
        if hand_val == 1 and did_anyone_raise:
          return 0
      case 1:
        if not did_anyone_raise and obs.can_raise():
          return min_raise
      case 2:
        print("turn")
      case 3:
        if hand_val == 1 and did_anyone_raise:
          return 0
      case _:
        pass
      
    return 1 # check / call

