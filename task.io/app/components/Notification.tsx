// components/Notification.tsx
import React from 'react';

interface NotificationProps {
  message: string;
  error?: boolean;
}

const Notification: React.FC<NotificationProps> = ({ message, error }) => {
  return (
    <div className={`fixed bottom-4 right-4 p-4 rounded-md shadow-md ${error ? 'bg-red-500' : 'bg-green-500'}`}>
      <p className="text-white">{message}</p>
    </div>
  );
};

export default Notification;