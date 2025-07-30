# Demo Deployment Guide

## Quick Start

### 1. Backend Deployment (Railway)

1. **Create Railway Project**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and create project
   railway login
   railway create affinity-demo-backend
   ```

2. **Set Environment Variables** (⚠️ SECURITY: Use secure values!)
   ```bash
   # Demo configuration
   railway variables set DEMO_MODE=true
   railway variables set USE_SQLITE=true
   railway variables set SQLITE_DB_PATH=/app/data/demo_pets.db
   railway variables set MAX_INTERACTIONS=50
   railway variables set SESSION_TIMEOUT=1800
   railway variables set MAX_SESSIONS=100
   railway variables set MAX_PETS_PER_IP=5
   
   # SECURITY: Generate secure passwords and keys
   railway variables set DEMO_PASSWORD=$(openssl rand -base64 20)
   railway variables set SESSION_SECRET_KEY=$(openssl rand -base64 32)
   railway variables set ADMIN_API_KEY=$(openssl rand -base64 32)
   railway variables set JWT_SECRET_KEY=$(openssl rand -base64 32)
   
   # CORS (update with your actual domain)
   railway variables set CORS_ORIGINS=https://your-demo-domain.com
   railway variables set CORS_ALLOW_CREDENTIALS=true
   
   # Security settings
   railway variables set ENVIRONMENT=production
   railway variables set LOG_LEVEL=WARNING
   railway variables set ENFORCE_HTTPS=true
   ```

3. **Deploy**
   ```bash
   # From project root
   railway deploy
   ```

4. **Get URL**
   ```bash
   railway status
   # Note the URL (e.g., https://affinity-demo-backend.railway.app)
   ```

### 2. Frontend Deployment (Vercel)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy from next/ directory**
   ```bash
   cd next
   vercel --prod
   ```

3. **Set Environment Variables in Vercel Dashboard**
   - `NEXT_PUBLIC_DEMO_MODE=true`
   - `NEXT_PUBLIC_DEMO_PASSWORD=AFFINITY2024`
   - `NEXT_PUBLIC_API_URL=https://affinity-demo-backend.railway.app`

### 3. Domain Setup (Optional)

1. **Add custom domain in Vercel**
   - Go to project settings
   - Add `demo.affinity-companion.com`

2. **Update CORS in Railway**
   ```bash
   railway variables set CORS_ORIGINS=https://demo.affinity-companion.com,http://localhost:3000
   ```

## Testing Deployment

### 1. Test Backend Health
```bash
curl https://affinity-demo-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "demo_mode": true,
  "database": "sqlite",
  "timestamp": 1234567890
}
```

### 2. Test Demo Authentication
```bash
# Should fail without password
curl https://affinity-demo-backend.railway.app/api/demo/status

# Should work with password
curl -H "X-Demo-Password: AFFINITY2024" \
     https://affinity-demo-backend.railway.app/api/demo/status
```

### 3. Test Frontend
1. Visit https://demo.affinity-companion.com
2. Enter password: `AFFINITY2024`
3. Try emoji interactions
4. Check demo banner shows limits

## Daily Reset Setup

### Automatic Reset (Railway Cron)

1. **Add to Railway environment**
   ```bash
   railway variables set RESET_SCHEDULE="0 3 * * *"
   ```

2. **Create reset service** (separate Railway service)
   ```bash
   # Create new service for cron job
   railway create affinity-demo-reset
   
   # Deploy cron script
   railway deploy --service affinity-demo-reset
   ```

### Manual Reset

```bash
# SSH into Railway container or run locally
DEMO_MODE=true python backend/scripts/demo_reset.py
```

## Monitoring

### Check Active Sessions
```bash
curl -H "X-Demo-Password: AFFINITY2024" \
     https://affinity-demo-backend.railway.app/api/demo/status
```

### View Logs
```bash
# Railway logs
railway logs

# Vercel logs
vercel logs
```

## Security Considerations

### Environment Variables
- Never commit real passwords to git
- Use Railway/Vercel environment variable systems
- Rotate demo password weekly

### Rate Limiting
- Monitor API usage in Railway dashboard
- Set up alerts for unusual traffic
- Consider IP-based blocking for abuse

### Cost Control
- Set spending limits in Railway
- Monitor bandwidth usage
- Review logs for bot activity

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `CORS_ORIGINS` includes your domain
   - Verify HTTPS vs HTTP

2. **Password Not Working**
   - Check `DEMO_PASSWORD` environment variable
   - Verify header name is `X-Demo-Password`

3. **Rate Limiting Not Working**
   - Check `DEMO_MODE=true` in backend
   - Verify middleware is loaded

4. **Database Issues**
   - Check SQLite file permissions
   - Verify `USE_SQLITE=true`

### Emergency Shutdown

1. **Disable demo access**
   ```bash
   railway variables set DEMO_MODE=false
   ```

2. **Or change password**
   ```bash
   railway variables set DEMO_PASSWORD=EMERGENCY_DISABLED
   ```

3. **Scale down**
   ```bash
   railway scale --replicas 0
   ```

## Cost Estimates

### Railway (Backend)
- Free tier: 500 hours/month
- Paid: ~$5-20/month depending on usage

### Vercel (Frontend)
- Free tier: Generous for demos
- Bandwidth: Monitor if high traffic

### Total: $0-25/month for typical demo usage

## Success Metrics

Track these metrics:
- Daily active sessions
- Average session duration
- Interaction completion rate
- Error rates
- Cost per session

## Next Steps

After successful demo deployment:
1. Share demo URL with select users
2. Collect feedback
3. Monitor usage patterns
4. Plan v2 features (memes!)
5. Consider scaling to production