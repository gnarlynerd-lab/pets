import React from 'react';

const ControlPanel = ({ onStart, onStop, onReset, systemStatus, isConnected }) => {
  const canStart = isConnected && (systemStatus === 'ready' || systemStatus === 'stopped');
  const canStop = isConnected && systemStatus === 'running';
  const canReset = isConnected;

  return (
    <div className="control-panel">
      <div className="control-header">
        <h2>Simulation Control</h2>
        <div className="status-badge">Status: {systemStatus}</div>
      </div>
      
      <div className="control-buttons">
        <button 
          className={`control-btn start-btn ${canStart ? '' : 'disabled'}`}
          onClick={onStart}
          disabled={!canStart}
        >
          ▶️ Start Simulation
        </button>
        
        <button 
          className={`control-btn stop-btn ${canStop ? '' : 'disabled'}`}
          onClick={onStop}
          disabled={!canStop}
        >
          ⏸️ Stop Simulation
        </button>
        
        <button 
          className={`control-btn reset-btn ${canReset ? '' : 'disabled'}`}
          onClick={onReset}
          disabled={!canReset}
        >
          🔄 Reset System
        </button>
      </div>

      <div className="control-info">
        <p><strong>DKS Agent System</strong> - Hospital Resource Management</p>
        <p>Watch as agents self-organize and develop emergent behaviors through local interactions.</p>
      </div>

      <style jsx>{`
        .control-panel {
          background: white;
          border-radius: 12px;
          padding: 25px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.1);
          text-align: center;
        }

        .control-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 25px;
          padding-bottom: 15px;
          border-bottom: 2px solid #eee;
        }

        .control-header h2 {
          margin: 0;
          color: #333;
          font-weight: 500;
        }

        .status-badge {
          background: #e9ecef;
          color: #495057;
          padding: 8px 16px;
          border-radius: 20px;
          font-size: 14px;
          font-weight: 600;
          text-transform: capitalize;
        }

        .control-buttons {
          display: flex;
          justify-content: center;
          gap: 15px;
          margin-bottom: 25px;
          flex-wrap: wrap;
        }

        .control-btn {
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          min-width: 140px;
        }

        .start-btn {
          background: linear-gradient(135deg, #28a745, #20c997);
          color: white;
        }

        .start-btn:hover:not(.disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }

        .stop-btn {
          background: linear-gradient(135deg, #dc3545, #c82333);
          color: white;
        }

        .stop-btn:hover:not(.disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        }

        .reset-btn {
          background: linear-gradient(135deg, #6c757d, #5a6268);
          color: white;
        }

        .reset-btn:hover:not(.disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
        }

        .control-btn.disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none !important;
          box-shadow: none !important;
        }

        .control-info {
          background: #f8f9fa;
          border-radius: 8px;
          padding: 20px;
          border-left: 4px solid #667eea;
        }

        .control-info p {
          margin: 8px 0;
          color: #495057;
        }

        .control-info p:first-child {
          font-weight: 600;
          color: #333;
        }

        @media (max-width: 600px) {
          .control-header {
            flex-direction: column;
            gap: 10px;
            text-align: center;
          }
          
          .control-buttons {
            flex-direction: column;
            align-items: center;
          }
          
          .control-btn {
            width: 100%;
            max-width: 200px;
          }
        }
      `}</style>
    </div>
  );
};

export default ControlPanel;
