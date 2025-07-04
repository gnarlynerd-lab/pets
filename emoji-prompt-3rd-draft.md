# Next.js Digital Pet Application - "Blobby Friends"

## Project Overview

Create a playful, visually engaging Next.js application featuring evolving digital pets represented as cute blob creatures. The interface should focus on emoji-based communication between users and their pets, with a fun, whimsical aesthetic that appeals to users of all ages.

## Core UI Requirements

### 1. Main Pet Display Area

Create a large, prominent container for the pet with the following characteristics:
- Soft, gradient background in pink/purple pastels (from pink-100 to purple-100)
- Rounded corners (rounded-3xl) with a subtle shadow and pink border
- Semi-transparent bubble animations that float upward throughout the container
- SVG-based blob pet that responds to user interaction with gentle movements

### 2. Blob Pet Visualization

Implement an SVG-based blob pet with the following features:
- Pink, gradient-filled amorphous blob shape that "breathes" and wiggles
- Progressive evolution features that appear as the pet develops:
  - Initial stage: Simple pink blob with minimal features
  - Second stage (~25%): Adds eyes that follow movement
  - Third stage (~50%): Adds facial expressions (smile)
  - Fourth stage (~75%): Adds simple appendages (arm-like extensions)
  - Final stage (~100%): Adds more humanoid characteristics while maintaining blob aesthetic

### 3. Emoji Communication Interface

Create a two-part emoji communication system:
- Chat history panel with:
  - Rounded message bubbles (purple for user, pink for pet)
  - Scrollable history that maintains conversation context
  - Clear visual distinction between user and pet messages
- Emoji selection interface with:
  - Quick-access emoji row with commonly used options
  - Expandable emoji picker with categorized options
  - Clean, minimal design with subtle animations on interaction

### 4. Evolution Progress Display

Include a progress indicator showing the pet's development:
- Playful evolution stage name (e.g., "Tiny Blobling" → "Super Blobbington")
- Percentage display of overall progress
- Animated progress bar with gradient fill
- Positioned at the bottom of the pet display area

## Visual Style Guide

### Colors
- Primary backgrounds: Gradient from pink-50 to purple-50
- Pet container: Gradient from pink-100 to purple-100
- Pet base color: #FF9AA2 (soft pink) with gradient variations
- User messages: purple-100
- Pet messages: pink-100
- Accent colors: pink-300, pink-500, purple-100
- Borders: pink-100, pink-200

### Typography
- Use a playful, rounded sans-serif font for all text
- Evolution stage names: text-sm, text-pink-700, font-medium
- Message bubbles: text-2xl for emojis
- Category headers: text-xs, text-pink-500

### Animations
- Blob "breathing": Gentle pulsing animation
- Blob "wiggling": Subtle, random movements that make the pet feel alive
- Floating bubbles: Continuous upward animation at varying speeds
- Button hover states: Subtle background color transitions
- Progress bar: Smooth width transitions when progress changes

## Technical Requirements

### Framework & Libraries
- Next.js 14+ with React 18+
- Tailwind CSS for styling
- SVG manipulation for the pet visualization

### Component Structure
- Main layout component that manages the overall UI
- Pet visualization component that handles the SVG rendering and animations
- Chat interface component that manages message history and display
- Emoji picker component with expandable categories
- Evolution progress component

### State Management
- Local React state for UI interactions and animations
- (Placeholder for your backend integration - not needed for initial UI implementation)

### Responsive Design
- Mobile-first approach
- Adjustable layout that works well on phones, tablets, and desktops
- Touch-friendly interaction elements

## Nice-to-Have Features
- Subtle sound effects for interactions
- Confetti animation when evolution milestones are reached
- Dark mode toggle with appropriate color adjustments
- Accessibility features for screen readers

## Specific Implementation Notes

1. The blob SVG should use bezier curves to create a smooth, organic shape
2. Animation timing should be gentle and natural-feeling
3. UI elements should have playful hover/active states
4. Bubble animations should be randomized for a more natural feel
5. The pet should respond visually to emoji interactions (subtle movements or expressions)

## Implementation Priority
1. Basic layout and UI components
2. Pet visualization with basic animation
3. Emoji communication interface
4. Evolution progress display
5. Refined animations and interactions

Please develop this interface with a focus on playfulness, visual appeal, and smooth animations that make the digital pet feel alive and engaging.
