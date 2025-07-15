
# EduBot 🎓🤖
**AI-Powered Chatbot for Smart College Inquiries**

EduBot is a smart, AI-driven chatbot designed to assist prospective students with college-related queries such as course details, fees, admission procedures, and comparison with other institutions. Built using Flask, MongoDB, and the Gemini (Google Generative AI) API, EduBot delivers real-time, intelligent, and context-aware responses via a web interface.

---

## 📌 Project Objective

The primary goal of EduBot is to enhance user interaction on the college website by:
- Managing student consultations efficiently.
- Providing instant answers about courses, eligibility, fees, and admissions.
- Storing user details in MongoDB for session tracking.
- Offering comparison features to highlight the college's unique benefits.
- Enabling seamless handover to human support when needed.

---

## 🚀 Features

- 👋 Welcomes users and stores their **name**, **phone number**, and **preferred course**.
- 🧠 Uses NLP (via Gemini/ChatGPT API) to understand and respond intelligently.
- 📚 Provides accurate details about available programs (B.Tech, BCA, BBA, MBA, BJMC, MCA).
- ⚖️ Compares the institution with other colleges on placements, faculty, infrastructure, and more.
- 🧾 Maintains user interaction history for personalized experiences.
- ☎️ Shares human contact info for queries beyond the bot's scope.

---

## 🛠️ Technologies Used

**Frontend:**
- HTML5
- CSS3
- Bootstrap

**Backend:**
- Python
- Flask
- Flask-CORS

**Database:**
- MongoDB
- PyMongo

**AI/NLP:**
- Gemini API (Google Generative AI)
- NLTK (Natural Language Toolkit)

**Other Libraries:**
- `openai`
- `requests`
- `beautifulsoup4`
- `scrapy`
- `selenium`
- `pandas`
- `flask-restful`
- `jwt (PyJWT)`
- `spacy`
- `json`

---

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/edubot.git
   cd edubot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server**:
   ```bash
   python edubot.py
   ```

4. **Access the chatbot** via:
   ```
   http://localhost:5000
   ```

---

## 🗂️ Folder Structure

```
edubot/
├── edubot.py             # Main Flask backend with API endpoints
├── requirements.txt      # Python dependencies
├── README.md             # Project description and instructions
└── frontend/             # HTML/CSS frontend (optional integration)
```

---

## ⚠️ Limitations

- Performance may degrade under complex or domain-specific queries.
- Requires continuous internet access and working API key.
- Dependent on Gemini API availability and accuracy.
- Chatbot may not always transfer seamlessly to human support.
- Security and data privacy measures are recommended for MongoDB.

---

## 🔮 Future Scope

- 🎙️ Voice-based interaction using speech recognition.
- 💡 Recommendation system for course and career guidance.
- 🌐 Cloud deployment for global access and scalability.
- 🛡️ Advanced security using blockchain or encryption.
- 🧠 Sentiment detection and emotional intelligence.
- 🌍 Multilingual support for diverse users.
- 🔁 Backup, recovery, and continuous monitoring system.

---

## 👨‍💻 Authors

- **Kanak Kaushik**  

> IITM College of Engineering, B.Tech CSE (Batch 2022–26)

---

## 📚 References

- [OpenAI](https://platform.openai.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB PyMongo Docs](https://pymongo.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- Research papers via [IEEE](https://ieeexplore.ieee.org/) and [SSRN](https://papers.ssrn.com/)

---

## 📄 License

This project is for academic and educational use only. Contact the authors for reproduction or adaptation.
