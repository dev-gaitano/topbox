<div align="center">
    <img src="https://res.cloudinary.com/diwkfbsgv/image/upload/v1775206748/logo_u4sz9t.svg" alt="banner_img">
    <h1>TopBox Studio</h1>
</div>

<br />

TopBox is an AI powered content management system that helps teams create, organize, update, and publish digital content across multiple platforms.

## Tech stack

- React + TypeScript + CSS + Vite Front-end
- Python + Flask Back-end API
- PostreSQL Database
- OpenAI API

## Features

- **Company Management**: Select existing companies or create new ones
- **Brand Guidelines**: Upload or generate brand guidelines
- **Content Creation**: Create content posts with topics, platform selection, and reference images
- **Content Review**: Review and edit generated content prompts and captions

## Getting Started

### Installation

```bash
# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

- API calls are configured to proxy to `http://localhost:5000`

```bash
# Setup frontend
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

### Build

```bash
cd frontend
npm run build
```

## API Endpoints

The frontend expects the following Flask backend endpoints:

### Companies

- `GET /api/companies` - Fetch all companies
- `POST /api/companies` - Create a new company
- `DELETE /api/companies/<int:company_id>` - Delete selected company
- `GET /api/companies/<int:company_id>` - Fetch selected company
- `PATCH /api/companies/<int:company_id>` - Update selected company

### Brand Guidelines

- `POST /api/brand-guidelines/upload` - Upload brand guidelines file
- `POST /api/brand-guidelines/generate` - Generate brand guidelines
- `POST /api/brand-guidelines/save` - Save generated guidelines
- `GET /api/brand-guidelines/<int:company_id>` - Get brand guidelines for selected company

### Content

- `POST /api/content/create` - Create new content post
- `GET /api/content/latest` - Get latest content for a company
- `GET /api/content/list` - Get latest 20 content for a company
- `POST /api/content/save` - Save content with prompt and caption

## Project Structure

```
.
├── README.md                           # Project documentation
├── backend/                            # Flask Backend
│   ├── app.py                          # Application entry point
│   ├── Dockerfile                      # Backend container config
│   ├── requirements.txt                # Python dependencies
│   ├── .env                            # Environment variables (local)
│   ├── app/                            # Application package
│   │   ├── __init__.py                 # Application factory (create_app)
│   │   ├── config.py                   # App configuration
│   │   ├── errors.py                   # Error handlers
│   │   ├── extensions.py               # Flask extensions
│   │   ├── agents/                     # AI Agent logic (OpenAI)
│   │   │   ├── brandAgent.py           # Brand guidelines agent
│   │   │   ├── contentAgent.py         # Content generation agent
│   │   │   ├── responseModels.py       # Pydantic response models
│   │   │   └── setup.py                # Shared AI agent setup
│   │   ├── api/                        # API Blueprints & Modular Routes
│   │   │   ├── auth/                   # Auth (routes, service, repository)
│   │   │   ├── companies/              # Companies (routes, service, repository)
│   │   │   ├── content/                # Content (routes, service, repository)
│   │   │   └── guidelines/             # Brand guidelines (routes, service, repository)
│   │   ├── database/                   # Database connection setup
│   │   ├── models/                     # Domain data models
│   │   └── utils/                      # Helper utilities
│   └── sql/                            # Database SQL schemas
├── frontend/                           # React + TypeScript Frontend
│   ├── index.html                      # HTML entry point
│   ├── package.json                    # Frontend dependencies and scripts
│   ├── tsconfig.json                   # TypeScript configuration
│   ├── vite.config.ts                  # Vite configuration
│   └── src/                            # Frontend source code
│       ├── App.tsx                     # Main React application component
│       ├── main.tsx                    # React entry point
│       ├── index.css                   # Global styles
│       ├── components/                 # UI components
│       └── props/                      # Type definitions & props interfaces
```

## Notes

- Selected company state is managed at "Main.tsx"
- repository.py files - Handle everything that talks to the SQL database
- service.py files - Handle all the business logic
- routes.py - files - Handle only HTTP related code
