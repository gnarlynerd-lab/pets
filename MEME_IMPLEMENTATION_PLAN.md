# Meme-Based Companion Response System (v2)

## Overview
Enhance the companion's communication by replacing or augmenting emoji responses with contextual memes, GIFs, and reaction images. This creates richer expression while maintaining visual simplicity.

## Why Memes?
- **Richer emotional range** - convey complex feelings/situations
- **Cultural connection** - shared references create bonding
- **Personality display** - meme choices reveal companion character
- **Intelligence demonstration** - appropriate selection shows understanding

## Technical Architecture

### Option 1: Giphy Integration (Recommended)
```typescript
// next/lib/giphy-client.ts
const GIPHY_API_KEY = process.env.NEXT_PUBLIC_GIPHY_KEY

export async function searchMeme(
  mood: string, 
  energy: number,
  context?: string
): Promise<string> {
  // Build intelligent search query
  const searchTerms = []
  
  if (energy > 70) searchTerms.push('excited', 'hyper')
  else if (energy < 30) searchTerms.push('tired', 'sleepy')
  
  searchTerms.push(mood)
  if (context) searchTerms.push(context)
  
  const query = searchTerms.join(' ')
  
  const response = await fetch(
    `https://api.giphy.com/v1/gifs/search?` +
    `api_key=${GIPHY_API_KEY}&` +
    `q=${query}&` +
    `limit=10&` +
    `rating=g&` +
    `lang=en`
  )
  
  const data = await response.json()
  
  // Select based on companion personality
  const gif = selectBestGif(data.data, companionPersonality)
  
  return gif.images.fixed_height.url
}
```

### Option 2: Curated Library + Giphy Fallback
```typescript
// next/lib/meme-library.ts
const CURATED_RESPONSES = {
  greeting: {
    high_energy: ['excited-wave.gif', 'hello-there-kenobi.gif'],
    low_energy: ['sleepy-wave.gif', 'tired-hello.gif']
  },
  happy: {
    high_energy: ['dancing-cat.gif', 'success-kid.jpg'],
    low_energy: ['content-cat.jpg', 'gentle-smile.gif']
  },
  confused: {
    any: ['confused-travolta.gif', 'math-lady.gif', 'wtf-cat.jpg']
  },
  love: {
    high_energy: ['heart-eyes.gif', 'kermit-hearts.gif'],
    low_energy: ['shy-love.gif', 'blushing.gif']
  }
}

export async function getMemeResponse(
  emotion: string,
  energy: number,
  relationship_depth: number
): Promise<MemeResponse> {
  // Try curated first for consistency
  const curated = getCuratedMeme(emotion, energy)
  
  if (curated && Math.random() > 0.3) {
    return { url: curated, source: 'curated' }
  }
  
  // Use Giphy for variety
  try {
    const gif = await searchMeme(emotion, energy)
    return { url: gif, source: 'giphy' }
  } catch {
    // Fallback to curated
    return { url: curated || DEFAULT_MEME, source: 'fallback' }
  }
}
```

## Backend Integration

### Enhanced FEP Response
```python
# backend/agents/digital_pet.py

def generate_meme_response(self, emoji_input, current_state):
    """Generate meme response based on FEP processing"""
    
    # Process emoji input through FEP
    fep_response = self.process_interaction(emoji_input)
    
    # Map internal state to meme categories
    meme_context = {
        'primary_emotion': self._map_state_to_emotion(),
        'energy_level': self.energy,
        'mood_valence': self.mood,
        'relationship_stage': self._calculate_relationship_depth(),
        'recent_context': self._get_interaction_context()
    }
    
    # Generate search terms
    search_strategy = self._build_search_strategy(meme_context)
    
    return {
        'emoji': fep_response,  # Keep emoji as fallback
        'meme_search': search_strategy,
        'personality_weights': self._get_personality_preferences()
    }
```

### Meme Selection Logic
```python
def _build_search_strategy(self, context):
    """Build intelligent search terms based on state"""
    
    strategies = []
    
    # Base emotion
    strategies.append({
        'terms': [context['primary_emotion']],
        'weight': 1.0
    })
    
    # Energy modifier
    if context['energy_level'] > 80:
        strategies.append({
            'terms': ['excited', 'hyper', context['primary_emotion']],
            'weight': 0.8
        })
    elif context['energy_level'] < 20:
        strategies.append({
            'terms': ['sleepy', 'tired', context['primary_emotion']],
            'weight': 0.8
        })
    
    # Relationship depth influences meme selection
    if context['relationship_stage'] > 0.7:
        strategies.append({
            'terms': ['inside joke', 'best friend'],
            'weight': 0.5
        })
    
    return strategies
```

## Frontend UI Changes

### Companion Display Update
```tsx
// next/app/page.tsx

{/* Large Meme/Emoji Display */}
<div className="text-center">
  {isLoading ? (
    <div className="text-8xl animate-pulse">💭</div>
  ) : companionMeme ? (
    <div className="relative w-full h-48">
      <img 
        src={companionMeme}
        alt="Companion response"
        className="max-h-full max-w-full mx-auto object-contain rounded"
        style={{
          animation: 'fadeIn 0.5s ease-in'
        }}
      />
      {/* Fallback emoji overlay for loading */}
      {!memeLoaded && (
        <div className="absolute inset-0 flex items-center justify-center text-6xl">
          {petResponse}
        </div>
      )}
    </div>
  ) : (
    <div className="text-8xl animate-pulse">
      {petResponse || '😊'}
    </div>
  )}
</div>
```

### Conversation History Update
```tsx
// Show memes in chat history
<div className="flex gap-2">
  <span className="font-bold">{companionName}:</span>
  {interaction.memeUrl ? (
    <img 
      src={interaction.memeUrl} 
      alt="Response" 
      className="h-16 rounded"
    />
  ) : (
    <span>{interaction.petResponse}</span>
  )}
</div>
```

## Progressive Enhancement Strategy

### Phase 1: Simple Meme Responses
- Basic emotion → meme mapping
- 5-10 curated memes per emotion
- Fallback to emoji if meme fails

### Phase 2: Contextual Selection
- Consider conversation history
- Time-of-day appropriate memes
- Energy level influences selection

### Phase 3: Personality Development
- Companion develops meme preferences
- Learns user's humor style
- Creates "inside jokes" with repeated favorites

### Phase 4: Advanced Features
- Custom text on meme templates
- Combine multiple reaction images
- Generate novel combinations

## Implementation Steps

### 1. Backend Updates (4 hours)
- [ ] Add meme_response field to interaction model
- [ ] Implement search strategy builder
- [ ] Add personality-based selection weights
- [ ] Create meme caching system

### 2. API Integration (2 hours)
- [ ] Sign up for Giphy API key
- [ ] Implement Giphy client with rate limiting
- [ ] Add error handling and fallbacks
- [ ] Cache popular searches

### 3. Frontend Updates (3 hours)
- [ ] Update companion display for images
- [ ] Add loading states for memes
- [ ] Update conversation history
- [ ] Handle image load errors gracefully

### 4. Curated Library (2 hours)
- [ ] Select 50-100 reaction images
- [ ] Organize by emotion and energy
- [ ] Host on CDN or include in build
- [ ] Create selection algorithm

### 5. Testing & Tuning (2 hours)
- [ ] Test inappropriate content filtering
- [ ] Verify mobile responsiveness
- [ ] Check loading performance
- [ ] Tune selection algorithms

## Content Moderation

### Safety Measures
```typescript
const filterInappropriate = (gifs: GiphyGif[]): GiphyGif[] => {
  return gifs.filter(gif => {
    // Giphy G-rating
    if (gif.rating !== 'g') return false
    
    // Additional keyword filters
    const blocked = ['violent', 'nsfw', 'inappropriate']
    const title = gif.title.toLowerCase()
    
    return !blocked.some(word => title.includes(word))
  })
}
```

## Performance Considerations

### Caching Strategy
```typescript
// next/lib/meme-cache.ts
const memeCache = new Map<string, CachedMeme>()

const getCachedOrFetch = async (searchKey: string) => {
  const cached = memeCache.get(searchKey)
  
  if (cached && cached.timestamp > Date.now() - CACHE_TTL) {
    return cached.url
  }
  
  const fresh = await fetchNewMeme(searchKey)
  memeCache.set(searchKey, {
    url: fresh,
    timestamp: Date.now()
  })
  
  return fresh
}
```

### Preloading
```typescript
// Preload next likely memes based on state
const preloadNextMemes = (currentMood: string, energy: number) => {
  const likelyTransitions = predictNextMoods(currentMood, energy)
  
  likelyTransitions.forEach(mood => {
    const img = new Image()
    img.src = getMemeUrl(mood)
  })
}
```

## Success Metrics

### Engagement
- Response time selection < 200ms
- Meme load time < 1s
- Fallback rate < 5%

### Quality
- User "lol" reactions tracked
- Meme → emoji fallback rate
- Inappropriate content = 0

### Technical
- Giphy API usage < 80% of limit
- Cache hit rate > 60%
- CDN bandwidth < budget

## Migration Path

### From Emoji → Memes
1. **Soft Launch**: 10% of responses include memes
2. **A/B Test**: Compare engagement rates
3. **Gradual Increase**: Raise to 50% if positive
4. **Full Launch**: Memes as primary, emoji fallback

### Database Migration
```sql
-- Add meme support to interactions
ALTER TABLE pet_interactions ADD COLUMN meme_url VARCHAR(500);
ALTER TABLE pet_interactions ADD COLUMN meme_source VARCHAR(50);
ALTER TABLE pet_interactions ADD COLUMN meme_search_terms JSON;
```

## Future Possibilities

### Advanced Features
- **Meme Templates**: Companion adds custom text
- **Meme Chains**: Multi-panel responses
- **User Memes**: Learn from user's shared memes
- **Meme Moods**: Morning vs evening meme styles

### Personality Through Memes
- Nerdy companion → programming memes
- Artistic companion → aesthetic memes
- Playful companion → animal memes
- Intellectual → philosophy memes

## Cost Estimates

### API Costs
- Giphy Free: 1000 requests/day = $0
- Giphy Pro: 10000 requests/day = $99/month
- Tenor: 1M requests/month = $0

### CDN/Storage
- Curated library: ~50MB = $5/month
- Cache storage: ~500MB = $10/month

### Total Monthly Cost
- Demo/Beta: $0-15/month
- Production: $50-150/month

---

## Quick Start Checklist

When ready to implement:

1. **Get API Key** (10 min)
   - [ ] Sign up at developers.giphy.com
   - [ ] Create app, copy API key
   - [ ] Add to .env.local

2. **Backend Prep** (1 hour)
   - [ ] Add meme fields to model
   - [ ] Update response endpoint
   - [ ] Deploy changes

3. **Minimal Frontend** (2 hours)
   - [ ] Add image display to companion
   - [ ] Update conversation history
   - [ ] Test with 5 memes

4. **Launch** (30 min)
   - [ ] Announce "Meme Mode" feature
   - [ ] Monitor API usage
   - [ ] Collect feedback

Ready when you are! 🚀