# Math Crossword Game 🎮 ➕ ➗

A fun educational game that combines crossword puzzles with basic math operations! Perfect for kids to practice their arithmetic skills while having fun.

## What is it? 🤔

This is a hobby project that creates math puzzles in a crossword format. Kids can:
- Solve simple math equations (addition, subtraction, multiplication)
- Fill in missing numbers to complete equations
- Get instant feedback with color-coded answers
- Challenge themselves with different difficulty levels

## How it works? 🎯

- Each puzzle is randomly generated
- Fill in the missing numbers to complete equations
- All equations are simple: `X op Y = Z` (where op is +, -, or *)
- Only positive whole numbers are used
- Green means correct, red means try again!
- Numbers can be shared between equations for extra challenge

## Setup and Running 🚀

### Prerequisites
- Python 3.13 or higher
- Node.js 18 or higher
- Git

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd game

# Create and activate virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

The server will start at `http://localhost:5000`

### Frontend Setup
```bash
# In a new terminal, from the project root
cd terka-math

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Running Tests 🧪

#### Backend Tests
```bash
# From the backend directory with venv activated
python -m pytest -v

# To see test coverage
python -m pytest --cov=app tests/
```

#### Frontend Tests (Coming Soon)
```bash
# From the terka-math directory
npm run test:unit
```

## Development Status 📊

Currently implemented:
- ✅ Puzzle generation with interconnected equations
- ✅ Real-time validation with visual feedback
- ✅ Multiple difficulty levels
- ✅ Responsive design
- ✅ Comprehensive backend test suite

Coming soon:
- 🔄 Frontend tests
- 🔄 Mobile optimizations
- 🔄 Multiplayer support

## Why? 💡

I created this game to make math practice more engaging and fun for kids. It combines the familiar format of crossword puzzles with basic arithmetic, helping children develop their math skills through play.

---
*This is a hobby project created with ❤️ for young math learners* 