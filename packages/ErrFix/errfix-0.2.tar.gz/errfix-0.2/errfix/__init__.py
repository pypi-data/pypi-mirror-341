# Importowanie funkcji
from .errfix import Naprawa, Analiza, OnOff

# Automatyczny import wszystkich funkcji
__all__ = ["Naprawa", "Analiza", "OnOff"]

# Powitanie przy imporcie
print("ErrFix | Moduł załadowano poprawnie.")
