# -- coding: utf-8 --
import asyncio
import random
import string
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
import re
import google.generativeai as genai
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS

# Ignore warnings
warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)
# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8000", "http://localhost:8080", "http://localhost:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Gemini API configuration
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# MongoDB connection details
MONGO_URI = "mongodb+srv://kanak:dh55cGP8AaYmglGK@edubot.m1egcwf.mongodb.net/" 
DATABASE_NAME = "edubot_data"
COLLECTION_NAME = "user_interactions"

# Initialize MongoDB client with error handling
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test connection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("EduBot: Connected to MongoDB successfully")
except Exception as e:
    print(f"EduBot: Failed to connect to MongoDB: {e}")
    client = None
    db = None
    collection = None

# Download NLTK data if not available
def ensure_nltk_data():
    try:
        nltk.data.find('corpora/wordnet')
        nltk.data.find('tokenizers/punkt')
        return True
    except LookupError:
        print("EduBot: Downloading required NLTK data...")
        try:
            nltk.download('wordnet', quiet=True)
            nltk.download('punkt', quiet=True)
            print("EduBot: NLTK data downloaded successfully.")
            return True
        except Exception as e:
            print(f"EduBot: Failed to download NLTK data: {e}")
            return False

# Check if NLTK data is available
def check_nltk_data():
    return ensure_nltk_data()

# Preprocessing setup
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    if not check_nltk_data():
        print("EduBot: Cannot lemmatize tokens due to missing NLTK data.")
        return tokens
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    if not check_nltk_data():
        print("EduBot: Cannot normalize text due to missing NLTK data.")
        return text.split()
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting setup
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "nods", "hi there", "hello", "I'm glad you're here!"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# College information
college_info = {
    "name": "IITM College of Engineering",
    "location": "Janakpuri, New Delhi",
    "contact_number": "011-28525882 / 28520239 / 28525051",
    "email": "director@iitmipu.ac.in",
    "semester_duration": "6 months",
    "courses": {
        "BCA": {
            "duration": "3 years (6 semesters)",
            "eligibility": "10+2 with at least 50% marks; must have studied Mathematics or Computer Science",
            "admission": "Through IPU CET conducted by GGSIPU",
            "total_fees": "₹2.59 lakh",
            "seat_intake": "240 students (120 in morning shift and 120 in evening shift)",
            "highlights": "Strong placement record with companies like Amazon, Wipro, and SAP; roles in front-end and back-end development."
        },
        "B.TECH": {
            "duration": "4 years (8 semesters)",
            "specializations": [
                "Computer Science & Engineering",
                "Electronics & Communication Engineering",
                "Civil Engineering",
                "Artificial Intelligence & Machine Learning",
                "Data Science"
            ],
            "eligibility": "10+2 with Physics, Chemistry, and Mathematics",
            "admission": "Through IPU CET or JEE Main scores",
            "total_fees": "₹4.55 lakh",
            "seat_intake": "Varies by specialization",
            "highlights": "Focus on developing sound knowledge in key areas of Computer Science and Engineering, Data Analytics, and Information Systems."
        },
        "MBA": {
            "duration": "2 years (4 semesters)",
            "eligibility": "Graduation with at least 50% marks",
            "admission": "Through CAT, CMAT, or IPU CET",
            "total_fees": "₹4.32 lakh",
            "highlights": "The program aims to impart participants with relevant knowledge, essential attributes, and necessary skills crucial for thriving in the corporate world."
        },
        "BBA": {
            "duration": "3 years (6 semesters)",
            "eligibility": "10+2 with at least 50% marks",
            "admission": "Through IPU CET",
            "total_fees": "₹2.64 lakh",
            "seat_intake": "360 students",
            "highlights": "Comprehensive curriculum covering various aspects of business administration."
        },
        "BJMC": {
            "duration": "3 years (6 semesters)",
            "eligibility": "10+2 with at least 45% marks",
            "admission": "Through IPU CET",
            "total_fees": "Approximately ₹2.6 lakh",
            "highlights": "Focuses on preparing students for careers in journalism and mass communication."
        },
        "MCA": {
            "duration": "3 years (6 semesters)",
            "eligibility": "Graduation with at least 50% marks and Mathematics as a subject",
            "admission": "Through IPU CET",
            "total_fees": "₹2.47 lakh",
            "highlights": "Emphasizes on advanced computer application concepts and practices."
        }
    }
}

# Function to display college details
def display_college_details():
    details = f"Here's information about {college_info['name']}:\n"
    details += f"Location: {college_info['location']}\n"
    details += f"Contact Number: {college_info['contact_number']}\n"
    details += f"Email: {college_info['email']}\n"
    details += f"Semester Duration: {college_info['semester_duration']}\n"
    details += "Courses Offered:\n"
    for course in college_info['courses']:
        details += f"- {course}\n"
    return details

# Function to display course details
def display_course_details(course_name):
    course = college_info['courses'].get(course_name.upper())
    if course:
        details = f"Here are the details for {course_name.upper()}:\n"
        for key, value in course.items():
            if isinstance(value, list):
                details += f"{key.capitalize()}:\n"
                for item in value:
                    details += f"  - {item}\n"
            else:
                details += f"{key.capitalize()}: {value}\n"
        return details
    else:
        return f"Sorry, I don't have information about the course '{course_name}'."

# Function to handle college comparison questions
def handle_college_comparison(user_response):
    comparison_keywords = ["better than", "why choose", "why should i choose", "advantages of", "stand out", "over", "vs", "versus"]
    if any(keyword in user_response for keyword in comparison_keywords):
        other_college = None
        for keyword in comparison_keywords:
            if keyword in user_response:
                parts = user_response.split(keyword)
                if len(parts) > 1:
                    other_college = parts[1].strip().split()[0].upper() # Get the first word after the keyword
                    break
        if other_college:
            responses = ("That's a fair question!, I can highlight what makes IITM College of Engineering a strong choice.Here’s why you should choose IITM:\n"
                         "1. Excellent placement records with top companies visiting campus every year.\n"
                         "2. Highly qualified and experienced faculty who focus on industry-relevant teaching.\n"
                         "3. Strong emphasis on technical skills, internships, and certifications.\n"
                         "4. Active student communities, technical clubs, and events to boost your growth.\n"
                         "5. Affordable fees compared to many private universities with premium education quality.\n"
                         "6. Located in Delhi, providing immense exposure and networking opportunities")
            print("EduBot:", responses.format(other_college=other_college))
        else:
            response = (
                "That's a really important question when you're considering your future! Here are a few reasons why IITM College of Engineering stands out:\n\n"
                "* IITM offers a perfect blend of academic excellence and practical exposure.\n"
                "1. Regular workshops, seminars, and industry interactions to keep you updated.\n"
                "2. Excellent infrastructure with modern labs, libraries, and tech-enabled classrooms.\n"
                "3. Strong alumni network helping students with mentorship and job opportunities.\n"
                "4. Focus on holistic development: sports, cultural events, fests, and leadership roles.\n"
                "5. Ranked among the top institutes for management and IT education in Delhi.\n"
                "Academic Foundation: We pride ourselves on our rigorous curriculum...\n"
            )
            print("EduBot:", response)
    else:
        response = (
            "Here Why IITM stands out from other colleges:\n"
            "1. Curriculum is updated regularly as per industry needs (AI, Data Science, Blockchain).\n"
            "2. Real-world projects, case studies, and internship programs make you industry-ready.\n"
            "3. Value-added certification programs in latest technologies.\n"
            "4. Scholarships and awards for meritorious and deserving students.\n"
            "5. Placement assistance with mock interviews, resume building, and aptitude training.\n"
            "6. Vibrant student life with regular tech, cultural, and management events"
        )
        print("EduBot:", response)

# Store user details in MongoDB
@app.route('/store_user', methods=['POST', 'OPTIONS'])
async def store_user():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    try:
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')

        print(f"EduBot: Received store_user request with name: {name}, phone: {phone}, payload: {data}")

        if not name or not phone:
            print("EduBot: Missing name or phone in request")
            return jsonify({'error': 'Name and phone are required'}), 400

        if collection is not None:
            user_data = {
                'name': name,
                'phone': phone,
                'timestamp': asyncio.get_event_loop().time()
            }
            print(f"EduBot: Attempting to insert user_data: {user_data}")
            result = collection.insert_one(user_data)
            if result.inserted_id:
                print(f"EduBot: Successfully inserted user with ID: {result.inserted_id}")
                response = jsonify({'message': 'You may ask your query now!'})
                response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
                return response, 200
            else:
                print("EduBot: Insert operation failed, no ID returned")
                return jsonify({'error': 'Failed to save user details'}), 500
        else:
            print("EduBot: MongoDB collection is None, connection not established")
            return jsonify({'error': 'MongoDB connection not established'}), 500

    except Exception as e:
        print(f"EduBot: Error storing user details: {str(e)}")
        return jsonify({'error': f'Failed to store user details: {str(e)}'}), 500

# Chat endpoint
@app.route('/chat', methods=['POST', 'OPTIONS'])
async def chat():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        user_name = data.get('name', 'Unknown')
        user_phone = data.get('phone', 'Unknown')

        print(f"EduBot: Received chat request with message: {message}, name: {user_name}, phone: {user_phone}, payload: {data}")

        if not message:
            print("EduBot: No message provided in chat request")
            return jsonify({'error': 'No message provided'}), 400

        # Check for greetings
        greet = greeting(message)
        if greet:
            response = jsonify({'response': greet})
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            return response

        # Check for college-related queries
        if re.search(r'\bcollege\b|\bcampus\b|\binstitute\b|\biitm\b', message, re.IGNORECASE):
            response = jsonify({'response': display_college_details()})
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            return response

        # Check for course-related queries
        courses = ['BCA', 'B.TECH', 'MBA', 'BBA', 'BJMC', 'MCA']
        for course in courses:
            if re.search(rf'\b{course}\b', message, re.IGNORECASE):
                response = jsonify({'response': display_course_details(course)})
                response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
                return response

        # Check for comparison queries
        if re.search(r'\bcompare\b|\bcomparison\b|\bvs\b|\bversus\b', message, re.IGNORECASE):
            response = jsonify({'response': handle_college_comparison(message.lower())})
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            return response

        # Default to Gemini API for other queries
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message)
            if response and response.text:
                flask_response = jsonify({'response': response.text})
                flask_response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
                return flask_response
            else:
                response = jsonify({'response': "Sorry, I couldn't generate a response. Please try again."})
                response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
                return response
        except Exception as e:
            print(f"EduBot: Gemini API error: {e}")
            response = jsonify({'response': f"Sorry, I encountered an error: {str(e)}"})
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            return response

    except Exception as e:
        print(f"EduBot: General error: {e}")
        response = jsonify({'error': f'Something went wrong: {str(e)}'})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        return response, 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)