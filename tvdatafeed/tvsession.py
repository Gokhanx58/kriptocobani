tvsession.py
```python
class TVSession:
    def login(self, username, password):
        pass  # Dummy login

    def get_hist(self, symbol, exchange, interval, n_bars):
        import pandas as pd
        import numpy as np
        data = {
            "close": pd.Series(np.random.randn(n_bars).cumsum() + 80000)
        }
        return pd.DataFrame(data)
```
