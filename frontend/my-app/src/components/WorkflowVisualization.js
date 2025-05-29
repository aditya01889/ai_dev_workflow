import React from 'react';
import { Box, Typography, Paper, Stepper, Step, StepLabel, StepContent, useTheme } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledStepIcon = styled('div')(({ theme, active, completed }) => ({
  width: 24,
  height: 24,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  borderRadius: '50%',
  backgroundColor: completed 
    ? theme.palette.primary.main 
    : active 
      ? theme.palette.primary.light 
      : theme.palette.grey[300],
  color: completed || active ? '#fff' : theme.palette.text.secondary,
  fontWeight: 'bold',
  fontSize: '0.75rem',
}));

const WorkflowStep = (props) => {
  const { active, completed, icon, label, description, status } = props;
  
  const getStatusColor = (status) => {
    if (!status) return 'inherit';
    switch (status.toLowerCase()) {
      case 'completed': return 'success.main';
      case 'in-progress': return 'warning.main';
      case 'error': return 'error.main';
      case 'pending': return 'text.secondary';
      default: return 'inherit';
    }
  };

  return (
    <Step active={active} completed={completed}>
      <StepLabel 
        StepIconComponent={({ active, completed, className }) => (
          <StyledStepIcon active={active} completed={completed}>
            {completed ? '✓' : icon}
          </StyledStepIcon>
        )}
      >
        <Box>
          <Typography variant="subtitle2">{label}</Typography>
          {status && (
            <Typography 
              variant="caption" 
              sx={{ 
                color: getStatusColor(status),
                fontWeight: 'bold',
                ml: 1
              }}
            >
              {status}
            </Typography>
          )}
        </Box>
      </StepLabel>
      <StepContent>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </StepContent>
    </Step>
  );
};

const WorkflowVisualization = ({ currentStep = 0, steps = [] }) => {
  const theme = useTheme();
  
  // Default steps if none provided
  const defaultSteps = [
    {
      label: 'Requirements Gathering',
      description: 'Collecting and analyzing project requirements',
      status: currentStep >= 0 ? (currentStep === 0 ? 'In Progress' : 'Completed') : 'Pending',
      icon: '1'
    },
    {
      label: 'Sprint Planning',
      description: 'Planning development sprints based on requirements',
      status: currentStep > 0 ? (currentStep === 1 ? 'In Progress' : 'Completed') : 'Pending',
      icon: '2'
    },
    {
      label: 'Development',
      description: 'Implementing features and components',
      status: currentStep > 1 ? (currentStep === 2 ? 'In Progress' : 'Completed') : 'Pending',
      icon: '3'
    },
    {
      label: 'Testing',
      description: 'Running unit and integration tests',
      status: currentStep > 2 ? (currentStep === 3 ? 'In Progress' : 'Completed') : 'Pending',
      icon: '4'
    },
    {
      label: 'Deployment',
      description: 'Deploying the application',
      status: currentStep > 3 ? (currentStep === 4 ? 'In Progress' : 'Completed') : 'Pending',
      icon: '5'
    }
  ];

  const displaySteps = steps.length > 0 ? steps : defaultSteps;

  return (
    <Paper 
      elevation={0} 
      sx={{ 
        p: 3, 
        borderRadius: 2,
        backgroundColor: theme.palette.background.paper,
        border: `1px solid ${theme.palette.divider}`
      }}
    >
      <Typography variant="h6" gutterBottom>
        Development Workflow
      </Typography>
      <Stepper orientation="vertical" activeStep={currentStep}>
        {displaySteps.map((step, index) => (
          <WorkflowStep
            key={index}
            label={step.label}
            description={step.description}
            status={step.status}
            icon={step.icon || (index + 1).toString()}
            active={index === currentStep}
            completed={index < currentStep}
          />
        ))}
      </Stepper>
    </Paper>
  );
};

export default WorkflowVisualization;
