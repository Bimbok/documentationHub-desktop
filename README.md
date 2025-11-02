# Bimbok Docs

A modern, dark-themed documentation viewer built with Python and Flet. Browse, search, and view your MongoDB-stored documentation with a beautiful UI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flet](https://img.shields.io/badge/flet-latest-purple.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)

## Features

- 🎨 Modern dark theme interface
- 🔍 Real-time search across titles, categories, and content
- 📱 Responsive grid layout
- 📝 Markdown and code syntax highlighting
- 🗄️ MongoDB integration for document storage
- ⚡ Fast and lightweight

## Screenshots

The app displays documentation cards in a responsive grid. Click any card to view the full document with syntax-highlighted code examples.

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account or local MongoDB instance
- pip (Python package manager)

## Installation

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd bimbokdocs
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
flet
pymongo
python-dotenv
```

### 4. Set Up MongoDB

#### Option A: MongoDB Atlas (Cloud)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Create a database named `bdoci`
4. Create a collection named `docs`
5. Get your connection string

#### Option B: Local MongoDB
```bash
# Install MongoDB locally
# Create database: bdoci
# Create collection: docs
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

Replace with your actual MongoDB connection string.

## MongoDB Document Structure

Documents in the `docs` collection should follow this structure:

```json
{
  "title": "Document Title",
  "category": "Category Name",
  "document": "Markdown formatted content here...",
  "code": "print('Python code here')"
}
```

### Example Document:

```json
{
  "title": "Python Lists",
  "category": "Python Basics",
  "document": "# Lists in Python\n\nLists are ordered, mutable collections...",
  "code": "my_list = [1, 2, 3]\nprint(my_list)"
}
```

## Usage

### Running the Application

```bash
# Make sure your virtual environment is activated
python main.py
```

The application will:
1. Connect to MongoDB
2. Fetch all documents from the `docs` collection
3. Display them in a responsive grid
4. Allow you to search and view documents

### Using the Interface

1. **Search**: Type in the search bar to filter documents by title, category, or content
2. **View Document**: Click any card to open the full document in a bottom sheet
3. **Close Document**: Click the X button or swipe down to close the document view

## Project Structure

```
bimbokdocs/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Configuration

### Database Settings

Edit these constants in `main.py` if needed:

```python
DATABASE_NAME = "bdoci"        # MongoDB database name
COLLECTION_NAME = "docs"       # MongoDB collection name
```

### Theme Customization

Colors can be modified in `main.py`:

```python
page.bgcolor = "#1a1a1a"           # Background color
card_color = "#2a2a2a"             # Card background
accent_color = "#00ff00"           # Green accent color
```

## Troubleshooting

### MongoDB Connection Issues

**Error:** `MongoDB connection error`

**Solutions:**
- Check your internet connection
- Verify your MongoDB URI in `.env`
- Ensure your IP is whitelisted in MongoDB Atlas
- Check if MongoDB service is running (local installation)

### Module Not Found Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

Flet uses port 8550 by default. If it's in use:

```python
# In main.py, at the bottom:
ft.app(target=main, port=8551)
```

## Development

### Adding New Documents via Python

```python
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()
client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client["bdoci"]
collection = db["docs"]

new_doc = {
    "title": "New Document",
    "category": "Tutorial",
    "document": "# Content here",
    "code": "print('Hello World')"
}

collection.insert_one(new_doc)
print("Document added!")
```

### Running in Debug Mode

```bash
# Add verbose logging
python main.py --verbose
```

## Security Notes

⚠️ **Important:**
- Never commit your `.env` file to version control
- Add `.env` to `.gitignore`
- Use environment variables for sensitive data
- Restrict MongoDB user permissions appropriately

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## Acknowledgments

- Built with [Flet](https://flet.dev/) - Flutter apps in Python
- Database: [MongoDB](https://www.mongodb.com/)
- Icons: [Material Icons](https://fonts.google.com/icons)

---

**Made with ❤️ for developers who love documentation**