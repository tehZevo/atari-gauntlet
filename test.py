import numpy as np
import matplotlib.pyplot as plt
from atari_gauntlet import AtariGauntlet

env = AtariGauntlet(step_limit=1000)

env.reset()

rewards = []

for _ in range(10000):
    action = np.random.randint(18)
    s, r, d, i = env.step(action)
    if d:
        s = env.reset()
    rewards.append(r)
    env.render()

env.game.close()

plt.plot(rewards)
plt.show()
