import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Define the fuzzy input variables
#    - health: 0 (dead) to 100 (full health)
#    - distance: 0 (very close) to 50 (far away, arbitrary units)
health = ctrl.Antecedent(np.arange(0, 101, 1), 'health')
distance = ctrl.Antecedent(np.arange(0, 51, 1), 'distance')

# 2. Define the fuzzy output variable
#    - aggressiveness: 0 (no aggression) to 100 (maximum aggression)
aggressiveness = ctrl.Consequent(np.arange(0, 101, 1), 'aggressiveness')

# 3. Define membership functions for each fuzzy set
#    Here we use trapezoidal membership functions (trapmf) as an example.
health['low'] = fuzz.trapmf(health.universe, [0, 0, 25, 35])
health['medium'] = fuzz.trapmf(health.universe, [25, 35, 65, 75])
health['high'] = fuzz.trapmf(health.universe, [65, 75, 100, 100])

distance['close'] = fuzz.trapmf(distance.universe, [0, 0, 10, 20])
distance['medium'] = fuzz.trapmf(distance.universe, [10, 20, 30, 40])
distance['far'] = fuzz.trapmf(distance.universe, [30, 40, 50, 50])

aggressiveness['low'] = fuzz.trapmf(aggressiveness.universe, [0, 0, 25, 40])
aggressiveness['medium'] = fuzz.trapmf(aggressiveness.universe, [25, 40, 60, 75])
aggressiveness['high'] = fuzz.trapmf(aggressiveness.universe, [60, 75, 100, 100])

# 4. Define fuzzy rules
#    These rules determine the output (aggressiveness) given the fuzzy inputs.
#    You can add more rules or adjust these based on desired game logic.

# If health is low and distance is close, we set aggressiveness to low
# (NPC might try to avoid combat if it's wounded).
rule1 = ctrl.Rule(health['low'] & distance['close'], aggressiveness['low'])
rule2 = ctrl.Rule(health['low'] & distance['medium'], aggressiveness['low'])
rule3 = ctrl.Rule(health['low'] & distance['far'], aggressiveness['medium'])

rule4 = ctrl.Rule(health['medium'] & distance['close'], aggressiveness['medium'])
rule5 = ctrl.Rule(health['medium'] & distance['medium'], aggressiveness['medium'])
rule6 = ctrl.Rule(health['medium'] & distance['far'], aggressiveness['high'])

rule7 = ctrl.Rule(health['high'] & distance['close'], aggressiveness['high'])
rule8 = ctrl.Rule(health['high'] & distance['medium'], aggressiveness['high'])
rule9 = ctrl.Rule(health['high'] & distance['far'], aggressiveness['high'])

# 5. Build and simulate the fuzzy control system
aggressiveness_control = ctrl.ControlSystem([rule1, rule2, rule3,
                                             rule4, rule5, rule6,
                                             rule7, rule8, rule9])
fuzzy_ai = ctrl.ControlSystemSimulation(aggressiveness_control)

# 6. Provide crisp (real-number) inputs to the system
#    Example: Health = 30%, distance = 10 (NPC is fairly close, somewhat low health)
fuzzy_ai.input['health'] = 30
fuzzy_ai.input['distance'] = 10

# 7. Run the fuzzy inference
fuzzy_ai.compute()

# 8. Get the fuzzy output, which can be used in your game logic
npc_aggressiveness = fuzzy_ai.output['aggressiveness']
print(f"NPC aggressiveness level: {npc_aggressiveness:.2f} (out of 100)")
