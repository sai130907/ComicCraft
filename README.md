# 🎨 ComicCraft

## AI-Powered Comic Story and Image Generator

ComicCraft is a Generative AI web application that transforms a user's story idea into a five-panel comic.

The application uses AI to generate comic scenes and Hugging Face image generation to create visual artwork for each panel. The generated panels can then be viewed and downloaded as a PDF comic.

---

## ✨ Features

- 📝 Enter your own comic story
- 👤 Define the main character
- 🏫 Choose the setting
- 🎭 Select the tone of the story
- 🎨 Select an art style
- 🤖 AI-powered story and scene generation
- 🖼️ Generate five AI comic panels
- 📖 Preview the generated comic
- 📄 Export the comic as a PDF
- 📥 Download the completed comic
- 🔐 API keys stored securely using environment variables

---

## 🧠 Technologies Used

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- FastAPI
- Uvicorn

### Generative AI

- Google Gemini API
- Hugging Face Inference API
- FLUX image generation model

### Other Technologies

- Python-dotenv
- Git
- GitHub

---

## 🏗️ Application Architecture

```text
                    COMICCRAFT
                         │
                         ▼
                ┌─────────────────┐
                │    Frontend     │
                │   HTML / CSS    │
                │   JavaScript    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     FastAPI     │
                │     Backend     │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      ┌────────────────┐    ┌─────────────────┐
      │  Gemini API    │    │ Hugging Face    │
      │                │    │ Inference API   │
      └───────┬────────┘    └────────┬────────┘
              │                      │
              ▼                      ▼
       Comic Scenes            AI Comic Images
              │                      │
              └──────────┬───────────┘
                         ▼
                  ┌──────────────┐
                  │ PDF Generator│
                  └──────┬───────┘
                         ▼
                  Download Comic