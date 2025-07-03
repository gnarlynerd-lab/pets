import React from 'react';
import './PetDetail.css';

const PetDetail = ({ pet }) => {
  if (!pet) return <div className="pet-detail">No pet selected</div>;
  
  // Check if pet data is properly loaded
  if (pet.mood === undefined || pet.health === undefined || pet.energy === undefined) {
    return <div className="pet-detail">Loading pet data...</div>;
  }
  
  // Ensure all required properties exist with defaults
  const safePet = {
    mood: pet.mood || 0,
    health: pet.health || 0,
    energy: pet.energy || 0,
    attention: pet.attention || 0,
    traits: pet.traits || {},
    needs: pet.needs || {},
    behavior_patterns: pet.behavior_patterns || {},
    behavior_history: pet.behavior_history || [],
    ...pet
  };

  // Helper to render trait network
  const renderTraits = () => {
    return Object.entries(safePet.traits).map(([trait, value]) => (
      <div key={trait} className="trait-item">
        <div className="trait-name">{trait}</div>
        <div className="trait-bar-container">
          <div 
            className="trait-bar" 
            style={{ width: `${value * 100}%` }}
          ></div>
          <span className="trait-value">{(value * 100).toFixed(0)}%</span>
        </div>
      </div>
    ));
  };

  // Helper to render needs status
  const renderNeeds = () => {
    return Object.entries(safePet.needs).map(([need, value]) => (
      <div key={need} className="need-item">
        <div className="need-name">{formatNeedName(need)}</div>
        <div className="need-bar-container">
          <div 
            className="need-bar" 
            style={{ 
              width: `${value}%`,
              backgroundColor: getNeedColor(need, value)
            }}
          ></div>
          <span className="need-value">{value.toFixed(0)}%</span>
        </div>
      </div>
    ));
  };

  // Format need name for display
  const formatNeedName = (name) => {
    return name.charAt(0).toUpperCase() + name.slice(1);
  };

  // Get color for need based on level
  const getNeedColor = (need, value) => {
    // For needs, higher is worse (more hungry, more thirsty)
    if (value < 30) return '#4CAF50';
    if (value < 70) return '#FFC107';
    return '#F44336';
  };

  // Helper to render behavior patterns
  const renderBehaviorPatterns = () => {
    // Sort by activation threshold descending
    const sortedBehaviors = Object.entries(safePet.behavior_patterns)
      .sort(([, valueA], [, valueB]) => valueB - valueA)
      .slice(0, 5); // Show top 5

    return sortedBehaviors.map(([behavior, threshold]) => (
      <div key={behavior} className="behavior-item">
        <div className="behavior-name">{formatBehaviorName(behavior)}</div>
        <div className="behavior-threshold">{threshold.toFixed(2)}</div>
      </div>
    ));
  };

  // Format behavior name for display
  const formatBehaviorName = (name) => {
    return name
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Helper to render recent behavior history
  const renderBehaviorHistory = () => {
    if (!safePet.behavior_history || safePet.behavior_history.length === 0) {
      return <div className="empty-state">No recent behaviors</div>;
    }

    return (
      <ul className="behavior-history-list">
        {safePet.behavior_history.map((behavior, index) => (
          <li key={index} className="behavior-history-item">
            {formatBehaviorName(behavior.behavior)}
          </li>
        ))}
      </ul>
    );
  };

  // Helper to render vital stats
  const getVitalColor = (value) => {
    if (value > 70) return '#4CAF50';
    if (value > 30) return '#FFC107';
    return '#F44336';
  };

  return (
    <div className="pet-detail">
      <div className="pet-vitals">
        <div className="vital-stat">
          <span className="vital-label">Health</span>
          <div className="vital-bar-container">
            <div 
              className="vital-bar" 
              style={{ width: `${safePet.health}%`, backgroundColor: getVitalColor(safePet.health) }}
            ></div>
            <span className="vital-value">{safePet.health.toFixed(0)}%</span>
          </div>
        </div>
        
        <div className="vital-stat">
          <span className="vital-label">Energy</span>
          <div className="vital-bar-container">
            <div 
              className="vital-bar" 
              style={{ width: `${safePet.energy}%`, backgroundColor: getVitalColor(safePet.energy) }}
            ></div>
            <span className="vital-value">{safePet.energy.toFixed(0)}%</span>
          </div>
        </div>
        
        <div className="vital-stat">
          <span className="vital-label">Mood</span>
          <div className="vital-bar-container">
            <div 
              className="vital-bar" 
              style={{ width: `${safePet.mood}%`, backgroundColor: getVitalColor(safePet.mood) }}
            ></div>
            <span className="vital-value">{safePet.mood.toFixed(0)}%</span>
          </div>
        </div>
        
        <div className="vital-stat">
          <span className="vital-label">Attention</span>
          <div className="vital-bar-container">
            <div 
              className="vital-bar" 
              style={{ width: `${safePet.attention}%`, backgroundColor: getVitalColor(safePet.attention) }}
            ></div>
            <span className="vital-value">{safePet.attention.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      <div className="pet-stats">
        <div className="stat-item">
          <span className="stat-label">Age:</span> 
          <span className="stat-value">{pet.age.toFixed(1)} days</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Stage:</span> 
          <span className="stat-value">{pet.stage}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Interactions:</span> 
          <span className="stat-value">{pet.interaction_count}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Lifetime Attention:</span> 
          <span className="stat-value">{pet.lifetime_attention.toFixed(0)}</span>
        </div>
      </div>

      <div className="detail-section">
        <h3>Personality Traits</h3>
        <div className="traits-container">
          {renderTraits()}
        </div>
      </div>

      <div className="detail-section">
        <h3>Current Needs</h3>
        <div className="needs-container">
          {renderNeeds()}
        </div>
      </div>

      <div className="detail-section">
        <h3>Common Behaviors</h3>
        <div className="behaviors-container">
          {renderBehaviorPatterns()}
        </div>
      </div>

      <div className="detail-section">
        <h3>Recent Behaviors</h3>
        <div className="behavior-history-container">
          {renderBehaviorHistory()}
        </div>
      </div>
    </div>
  );
};

export default PetDetail;
