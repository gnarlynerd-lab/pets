import React, { useState } from 'react';
import './InteractionPanel.css';

const InteractionPanel = ({ onInteract, petEnergy, petMood }) => {
  const [selectedInteraction, setSelectedInteraction] = useState('feed');
  const [interactionIntensity, setInteractionIntensity] = useState(1.0);
  const [interactionContent, setInteractionContent] = useState({});

  const handleInteractionTypeChange = (e) => {
    setSelectedInteraction(e.target.value);
    // Reset content when changing interaction type
    setInteractionContent({});
  };

  const handleIntensityChange = (e) => {
    setInteractionIntensity(parseFloat(e.target.value));
  };

  const handleContentChange = (key, value) => {
    setInteractionContent({
      ...interactionContent,
      [key]: value
    });
  };

  const handleSubmit = () => {
    // Prepare final content with intensity
    const content = {
      ...interactionContent,
      intensity: interactionIntensity,
    };
    
    // Add duration if not explicitly set
    if (!content.duration) {
      content.duration = interactionIntensity;
    }
    
    onInteract(selectedInteraction, content);
  };

  // Determine if interaction is available based on pet state
  const isInteractionDisabled = (type) => {
    if (petEnergy < 10 && type === 'play') {
      return true; // Too tired to play
    }
    return false;
  };

  // Get help text based on pet state
  const getHelpText = () => {
    if (petEnergy < 10) {
      return "Pet is too tired for active interactions";
    }
    if (petMood < 20) {
      return "Pet is in a bad mood, gentle interactions recommended";
    }
    return "";
  };

  // Render specific form fields based on interaction type
  const renderInteractionFields = () => {
    switch(selectedInteraction) {
      case 'feed':
        return (
          <>
            <div className="form-group">
              <label>Food Type</label>
              <select 
                onChange={(e) => handleContentChange('food_type', e.target.value)}
                value={interactionContent.food_type || 'basic'}
              >
                <option value="basic">Basic Food</option>
                <option value="premium">Premium Food</option>
                <option value="treat">Treat</option>
              </select>
            </div>
            <div className="form-group">
              <label>Amount</label>
              <input 
                type="range" 
                min="0.5" 
                max="2.0" 
                step="0.1" 
                value={interactionContent.amount || 1.0}
                onChange={(e) => handleContentChange('amount', parseFloat(e.target.value))}
              />
              <span>{(interactionContent.amount || 1.0).toFixed(1)}</span>
            </div>
          </>
        );
        
      case 'play':
        return (
          <>
            <div className="form-group">
              <label>Play Type</label>
              <select 
                onChange={(e) => handleContentChange('play_type', e.target.value)}
                value={interactionContent.play_type || 'basic'}
                disabled={isInteractionDisabled('play')}
              >
                <option value="basic">Basic Play</option>
                <option value="fetch">Fetch</option>
                <option value="chase">Chase</option>
                <option value="puzzle">Puzzle</option>
              </select>
            </div>
            <div className="form-group">
              <label>Duration</label>
              <input 
                type="range" 
                min="0.5" 
                max="3.0" 
                step="0.1" 
                value={interactionContent.duration || 1.0}
                onChange={(e) => handleContentChange('duration', parseFloat(e.target.value))}
                disabled={isInteractionDisabled('play')}
              />
              <span>{(interactionContent.duration || 1.0).toFixed(1)} min</span>
            </div>
          </>
        );
        
      case 'pet':
        return (
          <>
            <div className="form-group">
              <label>Where to Pet</label>
              <select 
                onChange={(e) => handleContentChange('location', e.target.value)}
                value={interactionContent.location || 'head'}
              >
                <option value="head">Head</option>
                <option value="back">Back</option>
                <option value="belly">Belly</option>
              </select>
            </div>
            <div className="form-group">
              <label>Duration</label>
              <input 
                type="range" 
                min="0.2" 
                max="2.0" 
                step="0.1" 
                value={interactionContent.duration || 1.0}
                onChange={(e) => handleContentChange('duration', parseFloat(e.target.value))}
              />
              <span>{(interactionContent.duration || 1.0).toFixed(1)} min</span>
            </div>
          </>
        );
        
      case 'train':
        return (
          <>
            <div className="form-group">
              <label>Skill to Train</label>
              <select 
                onChange={(e) => handleContentChange('skill', e.target.value)}
                value={interactionContent.skill || 'sit'}
              >
                <option value="sit">Sit</option>
                <option value="come">Come</option>
                <option value="stay">Stay</option>
                <option value="trick">Trick</option>
              </select>
            </div>
            <div className="form-group">
              <label>Difficulty</label>
              <input 
                type="range" 
                min="0.5" 
                max="2.0" 
                step="0.1" 
                value={interactionContent.difficulty || 1.0}
                onChange={(e) => handleContentChange('difficulty', parseFloat(e.target.value))}
              />
              <span>{(interactionContent.difficulty || 1.0).toFixed(1)}</span>
            </div>
          </>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="interaction-panel">
      <div className="form-group">
        <label>Interaction Type</label>
        <select 
          value={selectedInteraction} 
          onChange={handleInteractionTypeChange}
        >
          <option value="feed">Feed</option>
          <option value="play" disabled={isInteractionDisabled('play')}>Play</option>
          <option value="pet">Pet</option>
          <option value="train">Train</option>
          <option value="check">Check</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Interaction Intensity</label>
        <input 
          type="range" 
          min="0.5" 
          max="2.0" 
          step="0.1" 
          value={interactionIntensity}
          onChange={handleIntensityChange}
        />
        <span>{interactionIntensity.toFixed(1)}</span>
      </div>
      
      {renderInteractionFields()}
      
      <div className="help-text">
        {getHelpText()}
      </div>
      
      <button 
        className="interact-button" 
        onClick={handleSubmit}
        disabled={isInteractionDisabled(selectedInteraction)}
      >
        Interact with Pet
      </button>
    </div>
  );
};

export default InteractionPanel;
