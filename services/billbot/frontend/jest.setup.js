import '@testing-library/jest-dom/extend-expect';

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = WebSocket.OPEN;
  }

  addEventListener() {}
  removeEventListener() {}
  close() {}
  send() {}
}

global.WebSocket = MockWebSocket;
global.crypto = {
  randomUUID: () => 'test-uuid',
};

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
    };
  },
  useSearchParams() {
    return {
      get: jest.fn(),
    };
  },
}));

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://test-api.com';
process.env.NEXT_PUBLIC_WS_URL = 'ws://test-ws.com'; 