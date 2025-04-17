# ExpertOption API V2

join the discord: [Discord](https://discord.gg/kaZ8uV9b6k)

This project demonstrates a simple usage of the `ExpertOptionApiV2` from the `ExpertOptionApiV2.stable_api` package. It connects to the ExpertOption server, authenticates with a token, and retrieves the account balance.

## 🚀 Getting Started

### Requirements

- Python 3.7+
- `ExpertOptionApiV2` package installed
- A valid ExpertOption **token**

### 📦 Installation

```bash
pip install ExpertOptionApiV2
```

Or, if you're installing from source, clone the repository and run:

```bash
pip install .
```

### 🧠 Usage

Edit the script and replace `TOKEN = ""` with your actual token:

```python
TOKEN = "your_token_here"
```

Then run the script:

```bash
python script.py
```

### 🧪 Example

```python
import asyncio
from ExpertOptionApiV2.stable_api import ExpertOptionApiV2

TOKEN = ""

async def main():
    api = ExpertOptionApiV2(TOKEN, server_region="wss://fr24g1eu.expertoption.finance/ws/v40")
    await api.connect()

    print(await api.GetBalance()) 
    # print(await api.PlaceOrder(amount=1, type="call", assetid=240, exptime=60, isdemo=1)) 
    # print(await api.GetSingleCandles()) 

if __name__ == '__main__':
    asyncio.run(main())
```

### 📚 Available Methods

- `GetBalance()`: Returns current account balance.
- `PlaceOrder(...)`: Places a trade order (uncomment to use).
- `GetSingleCandles()`: Fetches single candle data (uncomment to use).

> 📝 **Note:** Ensure you are connected and authenticated before calling these methods.

### 🔐 Disclaimer

Use this code responsibly and ensure you comply with the ExpertOption Terms of Use. This is a simplified example and should not be used in production without further error handling and security checks.

---

Happy coding! 🚀
