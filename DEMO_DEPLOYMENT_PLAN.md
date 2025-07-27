# Demo Deployment Plan for AFFINITY

## Overview
Deploy AFFINITY as a password-protected demo with local storage, rate limiting, and automatic data resets to control costs and ensure security.

## Architecture
- **Frontend**: Next.js on Vercel (free tier)
- **Backend**: FastAPI on Railway (~$5/month)
- **Database**: SQLite (local file storage)
- **Auth**: Simple password gate
- **Limits**: 50 interactions/session, 10 concurrent users

## Implementation Phases

### Phase 1: Backend Modifications

#### 1.1 SQLite Support Enhancement
**File**: `backend/database/db_connection.py`
- [ ] Add `DEMO_MODE` environment variable
- [ ] Auto-create SQLite database if missing
- [ ] Add migration logic for demo schema
- [ ] Implement connection pooling for SQLite

#### 1.2 Demo Authentication Middleware
**File**: `backend/middleware/demo_auth.py` (new)
```python
# Pseudocode
- Check for DEMO_PASSWORD header
- Validate against environment variable
- Return 401 if invalid
- Pass through if valid or not in demo mode
```

#### 1.3 Rate Limiting System
**File**: `backend/middleware/rate_limit.py` (new)
- [ ] Session-based interaction counter
- [ ] Max 50 interactions per session
- [ ] Max 10 concurrent sessions
- [ ] 30-minute inactivity timeout
- [ ] Redis or in-memory storage for counters

#### 1.4 Demo-Specific Endpoints
**Files**: Update `backend/main.py`
- [ ] Add `/api/demo/status` - returns remaining interactions
- [ ] Add `/api/demo/reset` - manual reset (admin only)
- [ ] Modify existing endpoints to check rate limits

### Phase 2: Frontend Modifications

#### 2.1 Demo Authentication
**File**: `next/components/demo-auth.tsx` (new)
```tsx
// Components needed:
- DemoPasswordModal
- DemoAuthProvider
- useDemoAuth hook
```

#### 2.2 Demo Status Banner
**File**: `next/components/demo-banner.tsx` (new)
- [ ] "Demo Mode - Data resets daily" message
- [ ] Interaction counter (X/50 remaining)
- [ ] Session timer display
- [ ] Sticky positioning at top

#### 2.3 Environment Configuration
**Files**: 
- `next/.env.local` (development)
- `next/.env.production` (production)
```
NEXT_PUBLIC_API_URL=https://affinity-backend.railway.app
NEXT_PUBLIC_DEMO_MODE=true
NEXT_PUBLIC_DEMO_PASSWORD=AFFINITY2024
```

#### 2.4 API Client Updates
**File**: `next/hooks/use-authenticated-pet-state.ts`
- [ ] Add demo password to API headers
- [ ] Handle 401 responses (re-show password modal)
- [ ] Display rate limit warnings

### Phase 3: Database Schema for Demo

#### 3.1 Schema Modifications
**File**: `backend/database/schema_demo.sql` (new)
```sql
-- Simplified schema for demo
-- Remove user authentication tables
-- Add session_id as primary identifier
-- Add created_at for auto-cleanup
```

#### 3.2 Data Retention Policy
- [ ] Sessions expire after 30 minutes inactive
- [ ] Pets deleted after 24 hours
- [ ] Full database reset at 3am UTC daily

### Phase 4: Deployment Configuration

#### 4.1 Backend Deployment (Railway)

**File**: `railway.toml` (new)
```toml
[build]
builder = "DOCKERFILE"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "python -m backend.main"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

**Environment Variables**:
```
DEMO_MODE=true
DEMO_PASSWORD=<secure-password>
USE_SQLITE=true
MAX_SESSIONS=10
SESSION_TIMEOUT=1800
CORS_ORIGINS=https://demo.affinity-companion.com
```

#### 4.2 Frontend Deployment (Vercel)

**File**: `vercel.json` (new)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "app/api/*": {
      "maxDuration": 10
    }
  }
}
```

### Phase 5: Monitoring & Safety

#### 5.1 Usage Dashboard
**File**: `backend/api/admin.py` (new)
- [ ] `/api/admin/stats` - current usage statistics
- [ ] `/api/admin/sessions` - active session list
- [ ] `/api/admin/emergency-stop` - kill switch

#### 5.2 Automated Scripts
**File**: `backend/scripts/demo_maintenance.py` (new)
- [ ] Daily reset cron job
- [ ] Session cleanup (every hour)
- [ ] Usage report generation
- [ ] Cost alert triggers

### Phase 6: Testing & Launch

#### 6.1 Local Testing Checklist
- [ ] Test with `DEMO_MODE=true` locally
- [ ] Verify rate limiting works
- [ ] Test password authentication
- [ ] Confirm data resets properly
- [ ] Check all error states

#### 6.2 Staging Deployment
- [ ] Deploy to Railway staging
- [ ] Deploy to Vercel preview
- [ ] Test with 5 beta users
- [ ] Monitor for 24 hours
- [ ] Check costs and usage

#### 6.3 Production Launch
- [ ] Set up domain: demo.affinity-companion.com
- [ ] Configure SSL certificates
- [ ] Set up monitoring alerts
- [ ] Create usage documentation
- [ ] Prepare emergency procedures

## Cost Controls

### Automatic Shutoffs
1. **Daily cost limit**: $1/day
2. **Request limit**: 10,000/day
3. **Bandwidth limit**: 1GB/day
4. **CPU limit**: 1 core max

### Manual Controls
1. **Emergency stop**: Environment variable kill switch
2. **Password rotation**: Change weekly
3. **IP blocking**: For abuse
4. **Session purge**: Manual cleanup command

## Security Considerations

### What's Protected
- [x] API requires demo password
- [x] Rate limiting prevents abuse
- [x] No real user data stored
- [x] Daily resets prevent accumulation
- [x] Session timeout prevents camping

### What's Not Protected
- [ ] Demo password could be shared
- [ ] No individual user tracking
- [ ] Basic DDoS protection only
- [ ] No data encryption at rest

## Timeline

### Week 1: Backend Development
- Day 1-2: SQLite support and demo auth
- Day 3-4: Rate limiting implementation
- Day 5: Local testing and fixes

### Week 2: Frontend Development
- Day 1-2: Demo auth UI
- Day 3-4: Status banner and limits
- Day 5: Integration testing

### Week 3: Deployment
- Day 1: Railway backend setup
- Day 2: Vercel frontend setup
- Day 3: Domain and SSL
- Day 4-5: Beta testing and monitoring

## Success Metrics

1. **Performance**: <2s load time
2. **Availability**: 99% uptime
3. **Cost**: <$10/month
4. **Usage**: 50-100 demo sessions/week
5. **Feedback**: Positive user experience

## Rollback Plan

If issues arise:
1. **Immediate**: Set `EMERGENCY_STOP=true`
2. **Short-term**: Revert to password-only access
3. **Long-term**: Take down demo, fix issues
4. **Communication**: Email beta users about downtime

## Next Steps

1. Review this plan and approve
2. Create feature branch: `demo-deployment`
3. Start with Phase 1.1 (SQLite support)
4. Daily progress check-ins
5. Launch target: 2 weeks

---

**Questions to Address**:
- Preferred demo password?
- Domain name confirmed?
- Beta tester list?
- Cost ceiling if exceeded?