# SyntaxSultansV1 - StudyCompanion 🤖  
_Final Project Submission – COT6930 – Spring 2025_

![OwlMind Framework](docs/images/owlmind-banner.png)

---

### [Understand](#project-overview) | [Get Started](#getting-started) | [Extend](#extending-the-bot) | [Contribute](#contributing)

---

# 📖 Project Overview

**SyntaxSultansV1 - StudyCompanion** is an intelligent, student-friendly Discord-based educational assistant developed by **Syntax Sultans** as part of the **Final Project for the course COT6930 – Advanced Topics in Artificial Intelligence** at **Florida Atlantic University (Spring 2025)**.

It leverages a **rule-based engine** (**SimpleBrain**) for structured, rapid responses and integrates **Generative AI (HuggingFace GPT-2)** as a fallback, ensuring broad coverage for student questions in **AI, Machine Learning, and Data Science**.

---

# 🛠 Tech Stack

- **Python** (`discord.py`, `requests`)
- **Generative AI**: HuggingFace GPT-2 Model API
- **OwlMind Framework**: Modular Agentic Core built with Belief-Desire-Intention (BDI) architecture

---

# 📌 Architecture Overview

![Architecture](docs/images/owlmind-arch.png)

This project builds upon the [OwlMind Framework](https://github.com/GenILab-FAU/owlmind), which features:

- **Bot Runner:** Handles Discord-based interactions.
- **Agentic Core:** Implements BDI cognitive model (Beliefs, Desires, Intentions).
- **SimpleBrain Engine:** Manages rule-based matching from CSVs.
- **Generative AI Fallback:** Ensures flexible handling of non-matching queries via HuggingFace GPT-2.

---

# 📂 Project Structure


---

# ⚙️ Getting Started

## Prerequisites

- [Python 3.x installed](https://www.python.org/downloads/)
- [Git installed](https://git-scm.com/)
- A configured [Discord bot application](docs/discord.md)

---

## 🔧 Step 1: Clone the Repository

```bash
git clone https://github.com/VamsiNamballa/SyntaxSultansV1-StudyCompanion.git
cd SyntaxSultansV1-StudyCompanion

🔧 Step 2: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
(Or if needed:)

bash
Copy
Edit
python3 -m pip install --break-system-packages -r requirements.txt
🔧 Step 3: Setup Environment Variables
Create your .env file based on .env.example:

env
Copy
Edit
# .env
TOKEN=Your_Discord_Bot_Token
HUGGINGFACE_API_KEY=Your_HuggingFace_API_Key


🔧 Step 4: Run the Bot
bash
Copy
Edit
python bot-1.py
You should see a successful connection message similar to:



Your Discord bot is now live and ready to assist:



🧩 Extending the Bot
Expand rule-based responses: update the CSV files under rules/.

Customize fallback logic: modify genai.py.

Integrate external APIs: enhance artifacts connections.

🤝 Contributing
We welcome contributions to improve and extend this project!

Fork the repository

Create your feature branch (git checkout -b feature/NewFeature)

Commit your changes (git commit -m 'Add new feature')

Push to your branch (git push origin feature/NewFeature)

Open a Pull Request

📜 License
This project is licensed under the MIT License. See LICENSE for more information.

📚 Academic Context
Syntax Sultans developed SyntaxSultansV1 - StudyCompanion as the Final Project for COT6930 – Advanced Topics in AI at Florida Atlantic University (Spring 2025).

It builds upon the OwlMind Framework by the Generative Intelligence Lab (GenILab) at FAU to showcase practical educational applications of Generative AI and Agentic System Design.

📫 Links and Resources
OwlMind Framework: https://github.com/GenILab-FAU/owlmind

Florida Atlantic University: FAU Main Website

🎓 Created by Syntax Sultans | COT6930 | Spring 2025 | Florida Atlantic University
