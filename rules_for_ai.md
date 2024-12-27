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

## Mobile Sidebar Design Rules

### Layout Structure
- Use `main-layout` as root container with `:class="{ 'sidebar-open': isSidebarOpen }"`
- `AppSidebar` should be fixed positioned, controlled by `transform`
- Include a separate `sidebar-overlay` element for mobile mask effect

### Responsive Design
Desktop (> 768px):
- Fixed sidebar width: 240px
- Main content margin-left: 240px
- No overlay mask

Mobile (≤ 768px):
- Sidebar hidden by default (transform: translateX(-100%))
- Main content margin-left: 0
- Show menu button
- Show overlay mask when open

### Interaction
- Control sidebar via top menu button on mobile
- Click overlay to close sidebar
- Check and adapt layout on window resize

### Transitions
- Use transform transition for sidebar sliding
- Use opacity and visibility transition for overlay
- Transition margin-left for main content

### State Management
- Use `isMobile` to control mobile view
- Use `isSidebarOpen` to control sidebar state
- Handle window resize in `onMounted` and `onUnmounted` 

## Production Deployment Best Practices

### 1. Infrastructure Setup
- Use cloud provider (e.g., Alibaba Cloud, AWS) for better scalability
- Implement CDN for static assets
- Set up load balancer for traffic distribution
- Use container orchestration (Docker + Kubernetes)
- Configure auto-scaling based on load

### 2. Security Measures
- SSL/TLS certification (HTTPS) mandatory
- Web Application Firewall (WAF) protection
- DDoS protection enabled
- Regular security patches and updates
- IP whitelisting for admin access
- Sensitive data encryption at rest and in transit

### 3. Performance Optimization
- Enable Gzip compression
- Implement browser caching
- Minify and bundle static assets
- Use lazy loading for images and components
- Database query optimization
- Redis caching for frequent queries

### 4. Monitoring & Logging
- Set up centralized logging (ELK Stack)
- Configure real-time monitoring (Prometheus + Grafana)
- Error tracking system (Sentry)
- Performance monitoring (New Relic/DataDog)
- Set up alerts for critical metrics
- Regular performance audits

### 5. Deployment Process
- Implement CI/CD pipeline
- Use blue-green deployment strategy
- Automated testing before deployment
- Automated backup before deployment
- Rollback plan for each deployment
- Deployment during low-traffic periods

### 6. High Availability
- Multi-zone deployment
- Database replication
- Redis cluster configuration
- Regular failover testing
- Automated recovery procedures
- Load balancing across zones

### 7. Backup Strategy
- Automated daily database backups
- Regular configuration backups
- System state snapshots
- Cross-region backup storage
- Regular restore testing
- Retention policy enforcement

### 8. Environment Configuration
```env
# Production Environment Variables
NODE_ENV=production
VITE_MODE=production

# API Configuration
VITE_API_BASE_URL=https://api.example.com
VITE_API_TIMEOUT=10000
VITE_API_RETRY_COUNT=3

# Cache Configuration
VITE_CACHE_DURATION=3600
VITE_STATIC_CACHE_DURATION=604800

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_REPORTING=true

# Security
VITE_CSP_ENABLED=true
VITE_HSTS_ENABLED=true
```

### 9. Nginx Configuration
```nginx
# Production Nginx Configuration
server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip Configuration
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_comp_level 6;
    gzip_min_length 1000;

    # Static File Caching
    location /assets/ {
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }

    # API Proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # SPA Configuration
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        expires -1;
        add_header Cache-Control "no-store, no-cache, must-revalidate";
    }
}
```

### 10. Docker Production Configuration
```dockerfile
# Frontend Dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 11. Performance Requirements
- Page load time < 2s
- Time to interactive < 3s
- First contentful paint < 1s
- API response time < 300ms
- Error rate < 0.1%
- Uptime > 99.9%

### 12. Maintenance Procedures
- Regular dependency updates
- Database optimization
- Log rotation and cleanup
- SSL certificate renewal
- Security patch application
- Performance optimization
