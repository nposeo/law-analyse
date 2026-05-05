# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT open a public issue

Security vulnerabilities should not be disclosed publicly until a fix is available.

### 2. Report privately

Send an email to: **[your-email@example.com]** with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response timeline

- **24 hours:** Initial acknowledgment
- **7 days:** Preliminary assessment
- **30 days:** Fix or mitigation plan

### 4. Disclosure policy

- We will work with you to understand and fix the issue
- Once fixed, we will publicly disclose the vulnerability
- You will be credited (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

1. **Never commit `.env` files** with real credentials
2. **Use strong passwords** for database
3. **Keep dependencies updated**: `pip install -U -r requirements.txt`
4. **Use HTTPS** in production
5. **Limit API access** with rate limiting
6. **Regular backups** of database

### For Contributors

1. **Validate all inputs** (file uploads, API requests)
2. **Use parameterized queries** (SQLAlchemy ORM)
3. **Sanitize user data** before display
4. **Follow OWASP Top 10** guidelines
5. **Run security scanners**: `bandit -r backend/app`
6. **Review dependencies**: `safety check`

## Known Security Considerations

### 1. File Uploads

- **Risk:** Malicious PDF files
- **Mitigation:** 
  - Max file size: 50MB
  - File type validation
  - Virus scanning recommended for production

### 2. API Keys

- **Risk:** Exposed OpenAI API key
- **Mitigation:**
  - Never commit to git
  - Use environment variables
  - Rotate keys regularly
  - Monitor usage

### 3. Database Access

- **Risk:** SQL injection
- **Mitigation:**
  - Use SQLAlchemy ORM (parameterized queries)
  - No raw SQL
  - Principle of least privilege

### 4. CORS

- **Risk:** Unauthorized API access
- **Mitigation:**
  - Whitelist specific origins
  - Update `cors_origins` in production
  - Consider API authentication

### 5. Rate Limiting

- **Risk:** API abuse, DoS
- **Mitigation:**
  - Implement rate limiting (not in MVP)
  - Monitor API usage
  - Set up alerts

## Security Checklist for Production

- [ ] Change all default passwords
- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Enable database encryption at rest
- [ ] Set up firewall rules
- [ ] Implement rate limiting
- [ ] Add API authentication
- [ ] Enable logging and monitoring
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning
- [ ] Backup and disaster recovery plan

## Dependencies Security

We use:
- **Dependabot** for automated dependency updates
- **Safety** for Python vulnerability scanning
- **npm audit** for Node.js vulnerability scanning

Run security checks:

```bash
# Python
cd backend
pip install safety
safety check

# Node.js
cd frontend
npm audit
```

## Contact

For security concerns: **[your-email@example.com]**

For general issues: [GitHub Issues](https://github.com/YOUR-USERNAME/law-analyse/issues)
