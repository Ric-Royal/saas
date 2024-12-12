import { Server } from 'socket.io';

export const setupWebSocket = (io: Server) => {
  io.on('connection', (socket) => {
    console.log('Client connected');

    socket.on('joinPost', (postId: string) => {
      socket.join(`post-${postId}`);
    });

    socket.on('leavePost', (postId: string) => {
      socket.leave(`post-${postId}`);
    });

    socket.on('disconnect', () => {
      console.log('Client disconnected');
    });
  });
}; 