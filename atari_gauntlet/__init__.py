import gym
from gym import spaces
import retro
import random
import numpy as np

#python3 -m retro.import /path/to/your/ROMs/directory

class AtariGauntlet(gym.Env):
  def __init__(self, step_limit=None, obs_type="image", allowed_games=None, debug=False):
    """allowed_games should be a list of games with "-Atari2600" removed or None for all games"""
    super().__init__()
    self.step_limit = step_limit
    self.steps = 0
    self.obs_type = retro.Observations.IMAGE if obs_type == "image" else retro.Observations.RAM
    self.game = None
    self.debug = debug
    #TODO: hardcoded scale (to match 0-1 obs space)
    self.obs_scale = lambda x: x / 255.0

    self.low = 0
    self.high = 1

    self.games = AtariGauntlet.get_games()
    if allowed_games is not None:
      allowed_games = [g.strip().lower() for g in allowed_games]
      self.games = [g for g in self.games if g.replace("-Atari2600", "").strip().lower() in allowed_games]

    if self.obs_type == retro.Observations.IMAGE:
      self.observation_space = spaces.Box(shape=[250, 160, 3], low=self.low, high=self.high)
    else:
      self.observation_space = spaces.Box(shape=[128], low=self.low, high=self.high)

    #multidiscrete 3 3 2 = 18
    #some environments may not use all 18 actions, and therefore,
    # some actions may not represent the same button combinations in all environments
    #TODO: create mapping so all 18 actions are consistent (requires filtering)
    self.action_space = spaces.Discrete(18)

  def step(self, action):
    #step atari game
    state, reward, done, info = self.game.step(action)

    #fill to max size atari window to maintain consistent obs space
    if self.obs_type == retro.Observations.IMAGE:
      new_state = np.zeros([250, 160, 3])
      new_state[:state.shape[0], :state.shape[1]] = state
      state = new_state

    #transform state
    state = self.obs_scale(state)

    self.steps += 1

    if self.step_limit is not None and self.steps >= self.step_limit:
      if self.debug:
        print("Game over (step limit reached)")
      done = True
    elif done and self.debug:
        print("Game over ({} steps)".format(self.steps))

    return state, reward, done, info

  def render(self, **kwargs):
    self.game.render(**kwargs)

  def get_games():
    games = retro.data.list_games()
    games = list(filter(lambda x: "atari2600" in x.lower(), games))
    return games

  def reset(self):
    #close old emulator
    if self.game is not None:
      self.game.render(close=True) #close window?
      self.game.close()

    self.game_name = random.choice(self.games)
    if self.debug:
      print("Starting game:", self.game_name)

    self.game = retro.make(
      self.game_name,
      obs_type=self.obs_type,
      use_restricted_actions=retro.Actions.DISCRETE)

    # print(self.game.data.valid_actions())
    # print(self.game.action_space)

    self.steps = 0

    obs = self.game.reset()
    obs = self.obs_scale(obs)
    return obs

#print list of atari games
if __name__ == "__main__":
  games = AtariGauntlet.get_games()

  for game in games:
    env = retro.make(game, obs_type=retro.Observations.IMAGE,
      use_restricted_actions=retro.Actions.DISCRETE)
    print(game)
    print(env.observation_space, "->", env.action_space)
    print()
    env.close()
