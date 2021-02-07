# Atari Gauntlet
OpenAI Gym environment that picks random Atari games. Powered by [Retro](https://github.com/openai/retro).

## Installation
See https://retro.readthedocs.io/en/latest/getting_started.html#importing-roms
```
python3 -m retro.import /path/to/your/ROMs/directory
```

## Configuration
```python
AtariGauntlet(
  step_limit=1000, #number of steps to run each environment; defaults to None (infinite)
  obs_type="image", #observation type (image or ram); defaults to "image"
  allowed_games=None #list of games to play (without "-Atari2600") or None for all
)
```

## Usage
```python
from atari_gauntlet import AtariGauntlet
env = AtariGauntlet(step_limit=1000)
env.reset()

while True:
  action = np.random.randint(18)
  _, _, done, _ = env.step(action)
  if done:
    env.reset()
  env.render()
```
