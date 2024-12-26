# Key Analysis System - Rules for AI

## Core System Features

### 1. Key Analysis Metrics
- **Score Components**:
  - `repeat_letter_score`: Evaluates letter repetition patterns
  - `increasing_letter_score`: Evaluates ascending letter sequences
  - `decreasing_letter_score`: Evaluates descending letter sequences
  - `magic_letter_score`: Evaluates special letter combinations
  - `unique_letters_count`: Counts unique letters
  - `score`: Comprehensive score (threshold: 400 for high score)

### 2. System Architecture
- Frontend: Vue 3 + TypeScript + Naive UI (Apple-style design)
- Backend: FastAPI + SQLAlchemy + Python
- Database: PostgreSQL
- Cache: Redis
- Load Balancer: Nginx

### 3. Performance Requirements
- **Caching Strategy**:
  - Default cache expiry: 5 minutes
  - Statistics data: 5 minutes
  - User sessions: 24 hours
  - System config: 1 hour

- **Database Optimization**:
  - Connection pooling enabled
  - Regular VACUUM
  - Proper indexing
  - Default limit: 10 records per query

### 4. Security Rules
- **Authentication**:
  - JWT-based authentication required
  - Password hashing mandatory
  - Session management via Redis

- **API Security**:
  - CORS configuration required
  - Rate limiting enabled
  - SQL injection protection
  - XSS/CSRF protection
  - Request encryption
  - Sensitive data protection

### 5. Time Handling
- Default timezone: Asia/Shanghai
- All timestamps must be handled in UTC internally
- Time range queries must support millisecond timestamps
- Frontend display format: "YYYY-MM-DD HH:mm"

### 6. Data Processing
- Use Pandas for data analysis
- Handle all edge cases and invalid data
- Support time series analysis
- Implement data aggregation
- Cap results appropriately

### 7. Frontend Requirements
- Responsive design
- Apple-style UI components
- Lazy loading for routes and components
- Local caching strategy
- Image lazy loading

### 8. Error Handling
- Proper error messages in Chinese
- English documentation and comments
- Debug logging enabled in development
- Structured error responses

### 9. API Response Format
```json
{
  "success": boolean,
  "data": any,
  "message": string,
  "error_code": number (optional)
}
```

### 10. Code Style
- Python: Black formatter with line length 88
- TypeScript: Prettier
- Use type hints in Python
- Async/await pattern for database operations

### 11. Documentation
- API documentation in English
- Code comments in English
- User-facing messages in Chinese
- Markdown format for documentation

### 12. Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- Resource usage monitoring

### 13. Development Workflow
- Docker-based development environment
- Environment-specific configurations
- Automated testing required
- Code review process

### 14. Backup Strategy
- Regular database backups
- Configuration backup
- Disaster recovery plan

## Implementation Guidelines

### 1. Key Analysis Service
```python
class KeyAnalyzer:
    CACHE_EXPIRY = 300  # 5 minutes
    HIGH_SCORE_THRESHOLD = 400
    DEFAULT_LIMIT = 10
```

### 2. Database Models
```python
class KeyInfo:
    id: int
    created_at: datetime
    fingerprint: str
    repeat_letter_score: float
    increasing_letter_score: float
    decreasing_letter_score: float
    magic_letter_score: float
    score: float
    unique_letters_count: int
```

### 3. Required API Endpoints
- `/api/keys/recent`
- `/api/keys/high-score`
- `/api/statistics`
- `/api/auth`
- `/api/users`

### 4. Environment Variables
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=key_analysis
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

BACKEND_SECRET_KEY=your_secret_key
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
BACKEND_PORT=8000

VITE_API_BASE_URL=http://localhost:8000
```

## Maintenance Rules

### 1. System Updates
- Regular dependency updates
- Security patch application
- Performance optimization
- Feature enhancement

### 2. Monitoring Rules
- CPU usage < 80%
- Memory usage < 80%
- Response time < 500ms
- Error rate < 1%

### 3. Backup Rules
- Daily database backups
- Weekly configuration backups
- Monthly system backups
- Retention period: 30 days

### 4. Security Audit
- Weekly security scans
- Monthly penetration testing
- Quarterly security review
- Annual security audit

## Development Rules

### 1. Code Quality
- Test coverage > 80%
- No critical security issues
- No critical bugs
- Documentation required

### 2. Review Process
- Code review required
- Security review for sensitive changes
- Performance review for critical paths
- Documentation review

### 3. Deployment Process
- Staging environment testing
- Production deployment approval
- Rollback plan required
- Monitoring setup

### 4. Testing Requirements
- Unit tests required
- Integration tests required
- Performance tests required
- Security tests required 
