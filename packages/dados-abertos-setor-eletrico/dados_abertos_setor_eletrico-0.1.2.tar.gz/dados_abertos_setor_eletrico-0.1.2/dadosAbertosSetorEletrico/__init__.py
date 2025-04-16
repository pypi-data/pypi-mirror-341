from .dadosAbertosSetorEletrico import dadosAbertosSetorEletrico as _Classe

__all__ = ["_Classe"]

# Isso permite fazer:
# import dadosAbertosSetorEletrico
# cliente = dadosAbertosSetorEletrico("ccee")

def __getattr__(name):
    if name == "dadosAbertosSetorEletrico":
        return _Classe
    elif name == "__all__":
        return __all__
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
