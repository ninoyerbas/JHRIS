# Production Deployment Guide

This guide covers security hardening and production deployment best practices for JHRIS.

## Security Hardening

### 1. Rate Limiting

Install and configure express-rate-limit:

```bash
npm install express-rate-limit
```

Add to `backend/src/index.js`:

```javascript
const rateLimit = require('express-rate-limit');

// General API rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

// Auth rate limiter (stricter for login/register)
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5 // limit each IP to 5 requests per windowMs
});

app.use('/api/', apiLimiter);
app.use('/api/auth/', authLimiter);
```

### 2. Environment Configuration

Update `.env` with production values:

```env
PORT=3001
JWT_SECRET=<generate-strong-random-secret-here>
NODE_ENV=production
DATABASE_PATH=/var/lib/jhris/hris.db
ALLOWED_ORIGINS=https://yourdomain.com
```

Generate a strong JWT secret:
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

### 3. CORS Configuration

Update `backend/src/index.js`:

```javascript
const cors = require('cors');

const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:8000'],
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

### 4. HTTPS/SSL

Use a reverse proxy like Nginx or Apache:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /api {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location / {
        root /var/www/jhris/frontend/public;
        try_files $uri $uri/ /index.html;
    }
}
```

### 5. Database Migration to PostgreSQL

For production, migrate from SQLite to PostgreSQL:

```bash
npm install pg
```

Update database configuration to use PostgreSQL connection string.

### 6. Helmet.js for Security Headers

```bash
npm install helmet
```

Add to `backend/src/index.js`:

```javascript
const helmet = require('helmet');
app.use(helmet());
```

### 7. Input Validation

Install and use express-validator:

```bash
npm install express-validator
```

Add validation middleware to routes:

```javascript
const { body, validationResult } = require('express-validator');

router.post('/register',
  body('username').isLength({ min: 3 }).trim().escape(),
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
  authController.register
);
```

### 8. Logging and Monitoring

Install winston for logging:

```bash
npm install winston
```

Configure structured logging:

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

### 9. API Documentation with Swagger

```bash
npm install swagger-ui-express swagger-jsdoc
```

Add API documentation endpoint.

### 10. Database Backups

Set up automated backups:

```bash
# For PostgreSQL
0 2 * * * pg_dump jhris_db > /backups/jhris_$(date +\%Y\%m\%d).sql

# For SQLite
0 2 * * * cp /var/lib/jhris/hris.db /backups/hris_$(date +\%Y\%m\%d).db
```

## Deployment Options

### Option 1: Traditional VPS (Ubuntu/Debian)

1. Install Node.js:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

2. Install PM2 for process management:
```bash
sudo npm install -g pm2
```

3. Deploy application:
```bash
git clone <repo-url>
cd JHRIS/backend
npm install --production
pm2 start src/index.js --name jhris-api
pm2 startup
pm2 save
```

4. Configure Nginx (see HTTPS section above)

### Option 2: Docker

Create `Dockerfile` in backend directory:

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3001

CMD ["node", "src/index.js"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  api:
    build: ./backend
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  web:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend/public:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: Cloud Platforms

#### Heroku
```bash
heroku create jhris-app
git push heroku main
heroku config:set JWT_SECRET=<your-secret>
```

#### AWS/Azure/GCP
Use their respective app services with environment variable configuration.

## Monitoring and Maintenance

### Health Checks

The API includes a health check endpoint at `/api/health`. Set up monitoring:

```bash
# Using a monitoring service like UptimeRobot or Pingdom
# Or create a simple cron job:
*/5 * * * * curl -f http://localhost:3001/api/health || systemctl restart jhris
```

### Performance Monitoring

Consider using:
- New Relic
- DataDog
- Application Insights

### User Activity Audit Log

Implement audit logging for critical operations:
- User login/logout
- Employee creation/modification
- Leave request approvals
- Attendance modifications

## Initial Admin User Setup

Since public registration creates only 'employee' users, manually create the first admin:

```bash
# Connect to database
sqlite3 /path/to/hris.db

# Update a user to admin
UPDATE users SET role = 'admin' WHERE username = 'your_username';
```

Or create a one-time setup script.

## Backup and Recovery

### Regular Backups
- Database: Daily automated backups
- Application code: Version controlled with Git
- Configuration: Secure storage of .env files

### Recovery Plan
1. Restore database from backup
2. Deploy application from Git
3. Restore environment configuration
4. Verify system health

## Security Checklist

- [ ] Change default JWT_SECRET
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for specific origins
- [ ] Implement rate limiting
- [ ] Add input validation on all endpoints
- [ ] Set up logging and monitoring
- [ ] Configure automated backups
- [ ] Review and restrict file permissions
- [ ] Implement session timeout
- [ ] Add two-factor authentication (future enhancement)
- [ ] Regular security audits and updates
- [ ] Keep dependencies updated

## Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Caching**: Implement Redis for session storage and caching
3. **CDN**: Use CDN for static assets
4. **Compression**: Enable gzip compression in Nginx
5. **Minification**: Minify CSS and JS files

## Compliance Considerations

Depending on your region and industry:
- GDPR (EU): Data protection and privacy
- HIPAA (US Healthcare): If storing health information
- SOC 2: For handling sensitive customer data
- Local labor laws: Ensure HR data handling compliance

## Support and Updates

- Regularly update dependencies: `npm audit fix`
- Monitor security advisories
- Keep documentation updated
- Plan for feature enhancements
