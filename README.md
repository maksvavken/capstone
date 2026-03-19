# MathTutor AI

A math tutoring app powered by a fine-tuned LLaMA 3 model with RAG support. Users can input math questions and choose an explanation style.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- Angular CLI (`npm install -g @angular/cli`)

## Project Structure
```
capstone/
├── backend/         # Flask API + RAG system
│   ├── app.py
│   └── requirements.txt
├── frontend/        # Angular app
│   └── ...
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/maksvavken/capstone.git
cd capstone
```

### 2. Backend setup
```bash
cd backend
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

pip install -r requirements.txt

### 3. Frontend setup
```bash
cd ../frontend
npm install
```

## Running the project

### Option A — Run both together (from the `frontend/` folder)
```bash
cd frontend
npm start
```

### Option B — Run separately

**Backend** (from `backend/` folder with venv activated):
```bash
cd backend
source venv/bin/activate  # Mac/Linux
python app.py
```

**Frontend** (from `frontend/` folder):
```bash
cd frontend
ng serve
```

## Access

| Service  | URL                   |
|----------|-----------------------|
| Frontend | http://localhost:4200 |
| Backend  | http://localhost:5000 |

## API Endpoints

| Method | Endpoint        | Description           |
|--------|-----------------|-----------------------|
| GET    | /api/health     | Health check          |
| POST   | /api/getResponse | Send a message       |

### POST /api/getResponse

Request:
```json
{
  "chatId": "abc123",
  "message": "Solve lim(x->0) sin(3x)/x",
  "preference": "step_by_step",
  "lastMessage": "What is a derivative?"
}
```

Response:
```json
{
  "chatId": "abc123",
  "llmResponse": "..."
}
```

Available styles: `simple`, `detailed`, `step_by_step`, `visual`, `formal` - TODO
