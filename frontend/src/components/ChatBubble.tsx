import React from 'react';

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ role, content }) => {
  return (
    <div className={`chat-bubble-wrapper ${role}`}>
      <div className={`chat-bubble ${role}`}>
        {content}
      </div>
    </div>
  );
};

export default ChatBubble;
