import { describe, expect, it, jest, beforeEach } from '@jest/globals';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Notifications from '../Notifications';
import { wsClient } from '@/lib/websocket';

// Mock the WebSocket client
jest.mock('@/lib/websocket', () => ({
  wsClient: {
    connect: jest.fn(),
    disconnect: jest.fn(),
    addMessageHandler: jest.fn(),
    removeMessageHandler: jest.fn(),
  },
}));

describe('Notifications', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders notification bell button', () => {
    render(<Notifications />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('shows no notifications message when empty', () => {
    render(<Notifications />);
    fireEvent.click(screen.getByRole('button'));
    expect(screen.getByText('No notifications yet')).toBeInTheDocument();
  });

  it('connects to WebSocket on mount and disconnects on unmount', () => {
    const { unmount } = render(<Notifications />);
    expect(wsClient.connect).toHaveBeenCalled();
    
    unmount();
    expect(wsClient.disconnect).toHaveBeenCalled();
  });
}); 