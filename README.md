# CV Ranking Tool 📄✨

Welcome to the CV Ranking Tool! This Flask application helps you evaluate resumes against job descriptions, providing a ranked list based on relevance.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)

## Features 🎉
- Upload multiple CVs in PDF or DOCX format.
- Input a job description for context.
- Receive a ranked list of CVs based on their relevance to the job description.

## Prerequisites 📋
Before you begin, ensure you have the following:
- Python 3.x installed
- Flask library
- `PyPDF2`, `docx`, and `groq` libraries
- An API key from [Groq](https://chat.groq.com/)

## Installation ⚙️
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cv-ranking-tool.git
   cd cv-ranking-tool
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install Flask PyPDF2 python-docx groq
   ```

4. **Set your Groq API key:**
   - On Windows:
     ```bash
     set GROQ_API_KEY=your_api_key
     ```
   - On Mac/Linux:
     ```bash
     export GROQ_API_KEY=your_api_key
     ```

## Usage 🚀
1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Upload your CVs and provide a job description.

4. Click "Rank CVs" to see the results!

## API Integration 🔗
This application uses the Groq API to rank CV sections based on their relevance to the provided job description.

### How to Get an API Key:
1. Go to [Groq](https://chat.groq.com/).
2. Sign up or log in.
3. Create a new API key from the dashboard.
4. Copy the API key and set it as an environment variable as described in the Installation section.

## Contributing 🤝
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License 📜
This project is licensed under the MIT License. See the LICENSE file for details.

