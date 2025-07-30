# Testing Demo Mode

## Setup

1. Create `.env.local` file:
```bash
cp .env.local.example .env.local
```

2. Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEMO_MODE=true
NEXT_PUBLIC_DEMO_PASSWORD=TEST123
```

3. Start the dev server:
```bash
npm run dev
```

## Test Cases

### 1. Password Gate
- [ ] Visit http://localhost:3000
- [ ] Should see password modal
- [ ] Wrong password shows error
- [ ] Correct password (TEST123) allows entry
- [ ] Refresh page - should remember authentication

### 2. Demo Banner
- [ ] Banner shows at top with "DEMO MODE"
- [ ] Shows interaction count (X/50)
- [ ] Shows session timer counting down from 30:00
- [ ] Progress bar changes color as interactions increase

### 3. Rate Limiting (Backend)
- [ ] Can send up to 50 interactions
- [ ] After 50, should get rate limit error
- [ ] Session expires after 30 minutes

### 4. API Headers
Check Network tab in browser:
- [ ] All API calls include `X-Demo-Password` header
- [ ] Value matches environment variable

## Disable Demo Mode

Change `.env.local`:
```
NEXT_PUBLIC_DEMO_MODE=false
```

- [ ] No password modal
- [ ] No demo banner
- [ ] No rate limiting