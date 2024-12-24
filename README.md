# Key Analysis System

A web-based system for analyzing and visualizing cryptographic key generation statistics.

## Features

- Real-time key generation monitoring
- Statistical analysis and visualization
  - Score distribution analysis
  - Correlation matrix of different scoring factors
  - Time-series trend analysis
- High-score key tracking
- Recent key monitoring
- User authentication and authorization
- Responsive design for different screen sizes

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Pandas & NumPy (Data analysis)
- JWT Authentication
- CORS support

### Frontend
- Vue 3 (Composition API)
- TypeScript
- Naive UI (Component library)
- ECharts (Data visualization)
- Axios (HTTP client)
- Day.js (Date handling)

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup
1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure database:
```bash
cp config.example.json config.json
# Edit config.json with your database credentials
```

4. Create initial user:
```bash
python -m app.cli create-user <username> <password>
```

5. Start development server:
```bash
./start.sh
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

## API Documentation

### Authentication
- POST `/token` - Get access token
- POST `/auth/register` - Register new user

### Key Analysis
- GET `/keys/recent` - Get recently generated keys
- GET `/keys/high-score` - Get high scoring keys
- GET `/statistics` - Get statistical analysis

## Development

### Environment Variables
- `ENV`: development/production
- `SECRET_KEY`: JWT secret key
- Database configuration in `config.json`

### Code Style
- Backend: Black formatter
- Frontend: ESLint + Prettier

## Production Deployment

1. Set environment to production:
```bash
export ENV=production
```

2. Build frontend:
```bash
cd frontend
npm run build
```

3. Configure production server:
- Set up proper CORS origins
- Use secure JWT secret
- Configure database connection

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
