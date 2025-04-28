GPT Food Simulator

**GPT Food Simulator** is a Django-based API that simulates conversations between two AI agents about their **top 3 favorite foods**.  
The system uses **OpenAI GPT models** to create these conversations dynamically and **filters vegan or vegetarian users** based on their food choices.

The app provides secure user registration, login, and profile management with **JWT authentication**, and a clean **Swagger UI** for API documentation.

- Fully Dockerized  
- PostgreSQL Database  
- Modern Natural Language Processing (NLP)  

## How Natural Language Processing (NLP) is used

To automatically **extract food names** from GPT's free-text answers, the project uses **spaCy**, a powerful NLP library.

Instead of relying on simple keyword searches, the app:
- Parses the GPT response into **linguistic structures** (noun chunks, tokens)
- **Understands** and identifies relevant **food items** like "avocado toast", "chickpea curry", or "vegan pad thai"
- **Ignores irrelevant words** like "a sprinkle" or "flavor" for clean results

Thanks to this approach:
- GPT answers can be **free-form** (sentences, lists, paragraphs)  
- **Food names are extracted reliably** without manual hardcoding  
- It adapts automatically even if GPT's phrasing changes

---

##  Features

- Simulate 100 GPT-to-GPT food conversations
- Detect if a user follows a vegan or vegetarian diet automatically
- Extract top 3 favorite foods per user
- User Authentication (Signup, Login, JWT Tokens)
- Protected API endpoints with Bearer authentication
- Fully documented via Swagger/OpenAPI
- Dockerized setup (PostgreSQL + Django)

---

## ⚙ Tech Stack

- **Backend:** Django 5, Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **NLP:** spaCy (en_core_web_sm)
- **Database:** PostgreSQL 15
- **API Docs:** Swagger (drf-yasg)
- **Deployment:** Docker & Docker Compose

---

##  How to Run the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/GPT-Food-Simulator.git
   cd GPT-Food-Simulator
   ```

2. **Create your environment variables**
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` file and set your:
   - Database credentials
   - Django superuser credentials
   - OpenAI API key

3. **Run the app via Docker Compose**
   ```bash
   docker-compose up --build

 When you run Docker Compose, it will automatically:
  - Apply database migrations
  - Create the superuser (if it doesn't exist)
  - Simulate GPT-to-GPT conversations
  - Start the Django server
 
4. Access:
   - API Docs (Swagger): [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
   - Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

##  Credits

This project uses:
- [OpenAI API](https://platform.openai.com/)
- [spaCy NLP](https://spacy.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-yasg for Swagger](https://drf-yasg.readthedocs.io/)

