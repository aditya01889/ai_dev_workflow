import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme, status }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  borderLeft: `4px solid ${
    status === 'running' ? theme.palette.success.main :
    status === 'idle' ? theme.palette.warning.main :
    status === 'error' ? theme.palette.error.main :
    theme.palette.grey[500]
  }`,
}));

const AgentCard = ({ agent }) => {
  const { name, status, description, progress, lastActive } = agent;

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'running': return 'success.main';
      case 'idle': return 'warning.main';
      case 'error': return 'error.main';
      default: return 'grey.500';
    }
  };

  return (
    <StyledCard status={status.toLowerCase()}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6" component="div">
            {name}
          </Typography>
          <Chip 
            label={status} 
            size="small" 
            sx={{ 
              backgroundColor: getStatusColor(status),
              color: 'white',
              fontWeight: 'bold',
              textTransform: 'capitalize'
            }} 
          />
        </Box>
        
        <Typography variant="body2" color="text.secondary" mb={2}>
          {description}
        </Typography>
        
        {progress !== undefined && (
          <Box sx={{ width: '100%', mb: 1 }}>
            <Box display="flex" justifyContent="space-between" mb={0.5}>
              <Typography variant="caption" color="text.secondary">
                Progress
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {progress}%
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={progress} 
              sx={{ height: 6, borderRadius: 3 }}
            />
          </Box>
        )}
        
        {lastActive && (
          <Typography variant="caption" color="text.secondary" display="block" mt={1}>
            Last active: {new Date(lastActive).toLocaleString()}
          </Typography>
        )}
      </CardContent>
    </StyledCard>
  );
};

export default AgentCard;
