import React from 'react';
import { Box, Typography, Paper, Avatar, useTheme } from '@mui/material';
import { styled } from '@mui/material/styles';

const MessageBubble = styled(Paper)(({ theme, isUser }) => ({
  maxWidth: '70%',
  padding: theme.spacing(1.5, 2),
  marginBottom: theme.spacing(1.5),
  borderRadius: '18px',
  backgroundColor: isUser 
    ? theme.palette.primary.main 
    : theme.palette.grey[100],
  color: isUser ? '#fff' : theme.palette.text.primary,
  alignSelf: isUser ? 'flex-end' : 'flex-start',
  borderTopRightRadius: isUser ? '4px' : '18px',
  borderTopLeftRadius: isUser ? '18px' : '4px',
  boxShadow: theme.shadows[1],
  position: 'relative',
  '&:hover': {
    boxShadow: theme.shadows[2],
  },
}));

const Message = ({ message, isUser }) => {
  const theme = useTheme();
  
  return (
    <Box 
      display="flex" 
      flexDirection="column"
      alignItems={isUser ? 'flex-end' : 'flex-start'}
      width="100%"
      mb={2}
    >
      <Box 
        display="flex" 
        alignItems="flex-start"
        maxWidth="85%"
      >
        {!isUser && (
          <Avatar 
            sx={{ 
              bgcolor: theme.palette.primary.main,
              width: 32, 
              height: 32,
              mr: 1,
              mt: 0.5
            }}
          >
            {message.sender ? message.sender.charAt(0).toUpperCase() : 'A'}
          </Avatar>
        )}
        <Box>
          {!isUser && (
            <Typography 
              variant="caption" 
              color="text.secondary"
              display="block"
              mb={0.5}
              ml={1}
            >
              {message.sender || 'AI Agent'}
            </Typography>
          )}
          <MessageBubble elevation={2} isUser={isUser}>
            <Typography variant="body1">
              {message.text}
            </Typography>
            <Typography 
              variant="caption" 
              sx={{
                display: 'block',
                textAlign: 'right',
                mt: 0.5,
                opacity: 0.7,
                color: isUser ? 'rgba(255,255,255,0.8)' : 'inherit'
              }}
            >
              {new Date(message.timestamp || new Date()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </Typography>
          </MessageBubble>
        </Box>
      </Box>
    </Box>
  );
};

export default Message;
