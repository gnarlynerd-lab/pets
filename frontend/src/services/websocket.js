// WebSocket service for real-time communication with DKS backend

let websocket = null;
let messageHandlers = [];

export const connectWebSocket = (url) => {
  if (websocket) {
    websocket.close();
  }

  websocket = new WebSocket(url);
  
  websocket.onopen = (event) => {
    console.log('WebSocket connected to:', url);
  };

  websocket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      messageHandlers.forEach(handler => handler(data));
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  };

  websocket.onclose = (event) => {
    console.log('WebSocket disconnected:', event.reason);
  };

  websocket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  return websocket;
};

export const sendMessage = (message) => {
  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(message));
  } else {
    console.warn('WebSocket not connected, cannot send message:', message);
  }
};

export const addMessageHandler = (handler) => {
  messageHandlers.push(handler);
};

export const removeMessageHandler = (handler) => {
  messageHandlers = messageHandlers.filter(h => h !== handler);
};

export const closeWebSocket = () => {
  if (websocket) {
    websocket.close();
    websocket = null;
  }
};
