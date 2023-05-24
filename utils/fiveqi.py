"""fiveqi

Copyright (c) 2023 - S2N Lab (https://s2n.cnit.it/)
"""
fiveqiTable= [
    # value: int
    # packetDelayBudget: int (ms)
    ##### GBR
    {"value":  1, "packetDelayBudget": 100},
    {"value":  2, "packetDelayBudget": 150},
    {"value":  3, "packetDelayBudget":  50},
    {"value":  4, "packetDelayBudget": 300},
    {"value": 65, "packetDelayBudget":  75},
    {"value": 66, "packetDelayBudget": 100},
    {"value": 67, "packetDelayBudget": 100},
    {"value": 75, "packetDelayBudget": 100}, # defined but not used by the standard (see official documentations)
    {"value": 71, "packetDelayBudget": 150},
    {"value": 72, "packetDelayBudget": 300},
    {"value": 73, "packetDelayBudget": 300},
    {"value": 74, "packetDelayBudget": 500},
    {"value": 76, "packetDelayBudget": 500},
    #### Non-GBR
    {"value":  5, "packetDelayBudget": 100},
    {"value":  6, "packetDelayBudget": 300},
    {"value":  7, "packetDelayBudget": 100},
    {"value":  8, "packetDelayBudget": 300},
    {"value":  9, "packetDelayBudget": 300},
    {"value": 69, "packetDelayBudget":  60},
    {"value": 70, "packetDelayBudget": 200},
    {"value": 79, "packetDelayBudget":  50},
    {"value": 80, "packetDelayBudget":  10},
    #### Delay-critical GBR
    {"value": 82, "packetDelayBudget":  10},
    {"value": 83, "packetDelayBudget":  10},
    {"value": 84, "packetDelayBudget":  30},
    {"value": 85, "packetDelayBudget":   5},
    {"value": 86, "packetDelayBudget":   5}
]