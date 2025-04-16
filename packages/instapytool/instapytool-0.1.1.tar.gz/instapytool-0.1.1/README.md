# InstaPy-DM

InstaPy is a lightweight Python package that allows you to **send Instagram DMs using session-based login** and Selenium automation.

> ⚠️ This project is intended for **educational and research purposes** only. Use responsibly and in compliance with Instagram's terms of service.

---

## 🚀 Features

- 🔐 Login via Instagram session cookies (no password required)
- ✉️ Send direct messages to Instagram users
- 🧱 Modular design with FastAPI and Pydantic support
- 🧪 Ready for integration into larger automation pipelines

---

## 📦 Installation

```bash
pip install instapy-dm
```

---

## 🧠 Usage

### 1. Create a `DMRequest` and use `send_dm`

```python
from instapy import send_dm, DMRequest

data = DMRequest(
    username="your_instagram_username",
    session_id="your_session_id",
    target_username="target_user",
    message="Hello from InstaPy!"
)

response = send_dm(data)
print(response)
```

---

## 📁 Project Structure

```
instapy/
├── __init__.py         # Package exports
├── credentials.py      # BaseModel for session credentials
├── login.py            # Handles browser session login
└── dm.py               # Function to send a DM using credentials
```

---

## 🛠️ Requirements

- Python 3.7+
- Google Chrome installed
- ChromeDriver matching your browser version

### Optional ChromeDriver setup

You can download ChromeDriver manually from:
👉 https://chromedriver.chromium.org/downloads

Or install it via a manager like:

```bash
pip install webdriver-manager
```

---

## 💡 Example Use Cases

- Sending event invites to creators
- Networking outreach with verified session IDs
- Research in automation & bot development

---

## ⚠️ Important Notes

- This package uses session cookie-based authentication — you must extract a valid `sessionid` and `ds_user` cookie from an authenticated Instagram session.
- Do **not** use on accounts that risk violating Instagram’s automation policy.
- Login is headless by default but can be configured for debugging.

---

## 🔗 Useful Links

- [GitHub Repository](https://github.com/prajjwalnag/InstaPy)
- [Submit Issues](https://github.com/prajjwalnag/InstaPy/issues)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤖 Disclaimer

This tool automates browser actions on Instagram. Use it **only for educational or authorized purposes**. Automation may violate Instagram's terms — **use at your own risk**.
