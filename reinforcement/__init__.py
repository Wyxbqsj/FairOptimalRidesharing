from setting import *
if algorithm == "model":
    from .LearningBased import stateValueInit, stateValueSave, assess, reward2discount
elif algorithm == "incomeRate":
    from .incomeRate import stateValueInit, stateValueSave, assess, reward2discount
elif algorithm == "tabular":
    from .tabular import stateValueInit, stateValueSave, assess, reward2discount