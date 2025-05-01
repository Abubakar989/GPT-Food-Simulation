
### GPT Food Simulator

**GPT Food Simulator** is a Django-based API that simulates conversations between two AI agents about their **top 3 favorite foods**.  
The system uses **OpenAI GPT models** to create these conversations dynamically and **filters vegan or vegetarian users** based on their food choices.

**Powered by:** Hugging Face Transformers, and a custom ML classifier.

The app provides secure user registration, login, and profile management with **JWT authentication**, and a clean **Swagger UI** for API documentation.

**Try it live:** [http://16.170.234.158/swagger/](http://16.170.234.158/swagger/)

---

## Key Features

-  Simulates 100 GPT-to-GPT food conversations using OpenAI
-  Extracts food names using `roberta-base-food-ner` (NER model)
-  Classifies dishes into vegan, vegetarian, or non-vegetarian via scikit-learn model
-  JWT-secured user auth (signup/login with tokens)
-  Interactive Swagger API documentation
-  Fully Dockerized with PostgreSQL + Gunicorn + Nginx

---

## How NLP & AI Are Used

Unlike traditional keyword filtering, this app uses **NLP + ML-based techniques**:

### Food Name Extraction
- Uses Hugging Face's [`carolanderson/roberta-base-food-ner`](https://huggingface.co/carolanderson/roberta-base-food-ner)

### Food Classification
- Uses a trained `scikit-learn` classifier (`food_classifier.pkl`)
- Predicts if a dish is **vegan**, **vegetarian**, or **non-vegetarian**
- Falls back to keyword hints (like “My favorite vegan dish is...”) when classification is ambiguous
---

### Future Improvements
| Area           | Ideas                      |
|----------------|----------------------------|
| NLP Accuracy   | Use ensemble of models for entity extraction |
| Classifier     | Replace with a fine-tuned transformer |
| Performance    | Add async task queue (Celery) |
| UI             | Build frontend dashboard with filters |
| Feedback Loop  | User correction of dish classification |

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


