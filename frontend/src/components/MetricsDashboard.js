import React from 'react';

const MetricsDashboard = ({ metrics, isConnected }) => {
  if (!isConnected || !metrics) {
    return (
      <div className="metrics-placeholder">
        <p>Waiting for metrics data...</p>
      </div>
    );
  }

  const formatNumber = (num) => {
    if (typeof num !== 'number') return '0';
    return num.toFixed(2);
  };

  const formatPercentage = (num) => {
    if (typeof num !== 'number') return '0%';
    return (num * 100).toFixed(1) + '%';
  };

  return (
    <div className="metrics-dashboard">
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>System Status</h3>
          <div className="metric-value">{metrics.step || 0}</div>
          <div className="metric-label">Steps</div>
        </div>

        <div className="metric-card">
          <h3>Agents</h3>
          <div className="metric-value">{metrics.agent_count || 0}</div>
          <div className="metric-label">Total Active</div>
        </div>

        <div className="metric-card">
          <h3>Wait Time</h3>
          <div className="metric-value">{formatNumber(metrics.avg_wait_time)}</div>
          <div className="metric-label">Average (min)</div>
        </div>

        <div className="metric-card">
          <h3>Resource Usage</h3>
          <div className="metric-value">{formatPercentage(metrics.resource_utilization)}</div>
          <div className="metric-label">Utilization</div>
        </div>

        <div className="metric-card">
          <h3>Satisfaction</h3>
          <div className="metric-value">{formatNumber(metrics.patient_satisfaction)}</div>
          <div className="metric-label">Patient Score</div>
        </div>

        <div className="metric-card">
          <h3>Adaptation</h3>
          <div className="metric-value">{formatPercentage(metrics.avg_adaptation_score)}</div>
          <div className="metric-label">System Learning</div>
        </div>
      </div>

      {metrics.performance_metrics && (
        <div className="performance-section">
          <h3>Performance Metrics</h3>
          <div className="performance-grid">
            <div className="performance-item">
              <span className="performance-label">System Efficiency</span>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{width: `${metrics.performance_metrics.system_efficiency * 100}%`}}
                ></div>
              </div>
              <span className="performance-value">
                {formatPercentage(metrics.performance_metrics.system_efficiency)}
              </span>
            </div>

            <div className="performance-item">
              <span className="performance-label">Emergence Score</span>
              <div className="progress-bar">
                <div 
                  className="progress-fill emergence"
                  style={{width: `${metrics.performance_metrics.emergence_score * 100}%`}}
                ></div>
              </div>
              <span className="performance-value">
                {formatPercentage(metrics.performance_metrics.emergence_score)}
              </span>
            </div>

            <div className="performance-item">
              <span className="performance-label">Stability Score</span>
              <div className="progress-bar">
                <div 
                  className="progress-fill stability"
                  style={{width: `${metrics.performance_metrics.stability_score * 100}%`}}
                ></div>
              </div>
              <span className="performance-value">
                {formatPercentage(metrics.performance_metrics.stability_score)}
              </span>
            </div>
          </div>
        </div>
      )}

      {metrics.detected_patterns && Object.keys(metrics.detected_patterns).length > 0 && (
        <div className="patterns-section">
          <h3>Detected Patterns</h3>
          <div className="patterns-list">
            {Object.entries(metrics.detected_patterns).map(([key, pattern]) => (
              <div key={key} className="pattern-item">
                <div className="pattern-type">{pattern.type}</div>
                <div className="pattern-description">{pattern.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <style jsx>{`
        .metrics-dashboard {
          height: 100%;
        }

        .metrics-placeholder {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 400px;
          color: #666;
          font-style: italic;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 15px;
          margin-bottom: 25px;
        }

        .metric-card {
          background: #f8f9fa;
          border-radius: 8px;
          padding: 15px;
          text-align: center;
          border: 1px solid #e9ecef;
        }

        .metric-card h3 {
          margin: 0 0 10px 0;
          font-size: 12px;
          color: #666;
          text-transform: uppercase;
          font-weight: 600;
        }

        .metric-value {
          font-size: 24px;
          font-weight: bold;
          color: #333;
          margin-bottom: 5px;
        }

        .metric-label {
          font-size: 11px;
          color: #888;
        }

        .performance-section,
        .patterns-section {
          margin-top: 25px;
          padding-top: 20px;
          border-top: 1px solid #eee;
        }

        .performance-section h3,
        .patterns-section h3 {
          margin: 0 0 15px 0;
          font-size: 16px;
          color: #333;
        }

        .performance-grid {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .performance-item {
          display: grid;
          grid-template-columns: 100px 1fr 60px;
          align-items: center;
          gap: 10px;
        }

        .performance-label {
          font-size: 12px;
          color: #666;
        }

        .progress-bar {
          height: 8px;
          background-color: #e9ecef;
          border-radius: 4px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #28a745, #20c997);
          transition: width 0.3s ease;
        }

        .progress-fill.emergence {
          background: linear-gradient(90deg, #007bff, #6610f2);
        }

        .progress-fill.stability {
          background: linear-gradient(90deg, #fd7e14, #dc3545);
        }

        .performance-value {
          font-size: 12px;
          font-weight: 600;
          text-align: right;
        }

        .patterns-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .pattern-item {
          background: #fff3cd;
          border: 1px solid #ffeaa7;
          border-radius: 6px;
          padding: 10px;
        }

        .pattern-type {
          font-size: 11px;
          color: #856404;
          text-transform: uppercase;
          font-weight: 600;
          margin-bottom: 4px;
        }

        .pattern-description {
          font-size: 12px;
          color: #856404;
        }
      `}</style>
    </div>
  );
};

export default MetricsDashboard;
