import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  ThemeProvider, 
  CssBaseline, 
  Container, 
  Grid, 
  Paper, 
  TextField, 
  Button, 
  Typography, 
  Box, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Tooltip,
  Tabs,
  Tab,
  CircularProgress,
  Divider,
  Card,
  CardContent,
  CardHeader,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Badge,
  useTheme,
  useMediaQuery,
  Drawer,
  ListItemIcon,
  Grow,
  Alert,
  Snackbar,
  createTheme,
  ThemeProvider as MuiThemeProvider,
  alpha,
  Fab,
  Slide,
  Fade,
  Zoom
} from '@mui/material';
import {
  Send as SendIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon,
  Code as CodeIcon,
  Storage as StorageIcon,
  Api as ApiIcon,
  Build as BuildIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Chat as ChatIcon,
  Settings as SettingsIcon,
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon,
  Add as AddIcon,
  Close as CloseIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Refresh as RefreshIcon,
  Description as DescriptionIcon
} from '@mui/icons-material';

// Custom theme with light/dark mode support
const getDesignTokens = (mode) => ({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
          primary: {
            main: '#1976d2',
            light: '#42a5f5',
            dark: '#1565c0',
            contrastText: '#fff',
          },
          secondary: {
            main: '#9c27b0',
            light: '#ba68c8',
            dark: '#7b1fa2',
            contrastText: '#fff',
          },
          background: {
            default: '#f5f5f5',
            paper: '#ffffff',
          },
          text: {
            primary: 'rgba(0, 0, 0, 0.87)',
            secondary: 'rgba(0, 0, 0, 0.6)',
            disabled: 'rgba(0, 0, 0, 0.38)',
          },
        }
      : {
          primary: {
            main: '#90caf9',
            light: '#e3f2fd',
            dark: '#42a5f5',
            contrastText: 'rgba(0, 0, 0, 0.87)',
          },
          secondary: {
            main: '#ce93d8',
            light: '#f3e5f5',
            dark: '#ab47bc',
            contrastText: 'rgba(0, 0, 0, 0.87)',
          },
          background: {
            default: '#121212',
            paper: '#1e1e1e',
          },
          text: {
            primary: '#fff',
            secondary: 'rgba(255, 255, 255, 0.7)',
            disabled: 'rgba(255, 255, 255, 0.5)',
          },
        }),
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontWeight: 700, fontSize: '2.5rem' },
    h2: { fontWeight: 600, fontSize: '2rem' },
    h3: { fontWeight: 500, fontSize: '1.75rem' },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
          padding: '8px 16px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0px 2px 4px -1px rgba(0,0,0,0.2), 0px 4px 5px 0px rgba(0,0,0,0.14), 0px 1px 10px 0px rgba(0,0,0,0.12)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(45deg, #1976d2 0%, #2196f3 100%)',
          boxShadow: '0 4px 20px 0 rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
});

// Create theme instance
const theme = (mode) => createTheme(getDesignTokens(mode));

// Custom hook for scroll to bottom
function useScrollToBottom(deps = []) {
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [scrollToBottom, ...deps]);

  return { messagesEndRef, scrollToBottom };
}

// Custom component for animated messages
const AnimatedMessage = ({ children, index }) => (
  <Grow in={true} timeout={200 + (index * 100)}>
    <Box>{children}</Box>
  </Grow>
);

// Main App component
function App() {
  // Theme and UI state
  const [darkMode, setDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('darkMode');
    if (savedTheme !== null) return savedTheme === 'true';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  
  // App state
  const [mobileOpen, setMobileOpen] = useState(false);
  const [input, setInput] = useState('');
  const [activeTab, setActiveTab] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotification] = useState({ 
    open: false, 
    message: '', 
    severity: 'info' 
  });
  
  // Messages state
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'Hello! I\'m your AI development assistant. How can I help you today?',
      sender: 'ai',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  
  // Agents state
  const [agents, setAgents] = useState([
    { 
      id: 'requirement', 
      name: 'Requirement Gathering', 
      status: 'idle', 
      progress: 0,
      description: 'Gathers and analyzes project requirements',
      lastActive: 'Just now',
      icon: <DescriptionIcon />
    },
    { 
      id: 'codegen', 
      name: 'Code Generation', 
      status: 'idle', 
      progress: 0,
      description: 'Generates code based on requirements',
      lastActive: '2 minutes ago',
      icon: <CodeIcon />
    },
    { 
      id: 'testing', 
      name: 'Testing', 
      status: 'idle', 
      progress: 0,
      description: 'Runs tests and validates code',
      lastActive: '5 minutes ago',
      icon: <CheckCircleIcon />
    },
  ]);
  
  // Refs and hooks
  const themeMUI = useTheme();
  const isMobile = useMediaQuery(themeMUI.breakpoints.down('md'));
  const inputRef = useRef(null);
  const { messagesEndRef, scrollToBottom } = useScrollToBottom([messages]);
  
  // Apply theme and save preference
  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    document.body.style.backgroundColor = darkMode ? '#121212' : '#f5f5f5';
  }, [darkMode]);
  
  // Show notification
  const showNotification = useCallback((message, severity = 'info') => {
    setNotification({
      open: true,
      message,
      severity
    });
  }, []);
  
  // Close notification
  const handleCloseNotification = useCallback(() => {
    setNotification(prev => ({ ...prev, open: false }));
  }, []);
  
  // Toggle theme
  const toggleTheme = useCallback(() => {
    setDarkMode(prev => {
      const newMode = !prev;
      showNotification(`Switched to ${newMode ? 'dark' : 'light'} mode`);
      return newMode;
    });
  }, [showNotification]);
  
  // Toggle mobile drawer
  const toggleDrawer = useCallback(() => {
    setMobileOpen(prev => !prev);
  }, []);
  
  // Handle sending a message
  const handleSendMessage = useCallback(async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { 
      id: Date.now(),
      text: input, 
      sender: 'user', 
      timestamp: new Date(),
      type: 'text'
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const botResponse = {
        id: Date.now() + 1,
        text: `I received: "${input}"`,
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      };
      
      setMessages(prev => [...prev, botResponse]);
      showNotification('Message sent successfully', 'success');
      
      // Update agent status
      const updatedAgents = [...agents];
      const activeAgent = updatedAgents[Math.floor(Math.random() * updatedAgents.length)];
      if (activeAgent) {
        activeAgent.status = 'active';
        activeAgent.progress = Math.min(100, activeAgent.progress + 25);
        setAgents(updatedAgents);
      }
      
    } catch (error) {
      console.error('Error sending message:', error);
      showNotification('Failed to send message', 'error');
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, agents, showNotification]);
  
  // Handle tab change
  const handleTabChange = useCallback((event, newValue) => {
    setActiveTab(newValue);
  }, []);
  
  // Render message component
  const renderMessage = (message, index) => (
    <AnimatedMessage key={message.id} index={index}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
          mb: 2,
          px: 2
        }}
      >
        <Paper
          sx={{
            p: 2,
            maxWidth: '80%',
            bgcolor: message.sender === 'user' 
              ? 'primary.main' 
              : 'background.paper',
            color: message.sender === 'user' 
              ? 'primary.contrastText' 
              : 'text.primary',
            borderRadius: 2,
            boxShadow: 1
          }}
        >
          <Typography variant="body1">{message.text}</Typography>
          <Typography 
            variant="caption" 
            sx={{
              display: 'block',
              textAlign: 'right',
              mt: 1,
              opacity: 0.7,
              color: message.sender === 'user' 
                ? 'rgba(255, 255, 255, 0.7)' 
                : 'text.secondary'
            }}
          >
            {new Date(message.timestamp).toLocaleTimeString()}
          </Typography>
        </Paper>
      </Box>
    </AnimatedMessage>
  );
  
  // Render agent card
  const renderAgentCard = (agent) => (
    <Grid item xs={12} sm={6} md={4} key={agent.id}>
      <Card>
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: agent.status === 'active' ? 'success.main' : 'grey.500' }}>
              {agent.icon}
            </Avatar>
          }
          title={agent.name}
          subheader={`Status: ${agent.status}`}
          action={
            <IconButton>
              {agent.status === 'active' ? <PauseIcon /> : <PlayArrowIcon />}
            </IconButton>
          }
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            {agent.description}
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Progress
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={agent.progress} 
              sx={{ mt: 1, height: 8, borderRadius: 4 }}
            />
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
              Last active: {agent.lastActive}
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Grid>
  );
  
  // Render tab content
  const renderTabContent = () => {
    switch (activeTab) {
      case 0: // Chat
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Box sx={{ flex: 1, overflowY: 'auto', p: 2 }}>
              {messages.map((message, index) => renderMessage(message, index))}
              <div ref={messagesEndRef} />
            </Box>
            <Box component="form" onSubmit={handleSendMessage} sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Type your message..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  inputRef={inputRef}
                  disabled={isLoading}
                  InputProps={{
                    endAdornment: (
                      <IconButton 
                        type="submit" 
                        color="primary"
                        disabled={!input.trim() || isLoading}
                      >
                        {isLoading ? <CircularProgress size={24} /> : <SendIcon />}
                      </IconButton>
                    ),
                  }}
                />
              </Box>
            </Box>
          </Box>
        );
      
      case 1: // Agents
        return (
          <Grid container spacing={3} sx={{ p: 2 }}>
            {agents.map(renderAgentCard)}
          </Grid>
        );
      
      case 2: // Settings
        return (
          <Box sx={{ p: 3 }}>
            <Card>
              <CardHeader title="Appearance" />
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Typography>Theme:</Typography>
                  <Button 
                    variant="contained" 
                    onClick={toggleTheme}
                    startIcon={darkMode ? <LightModeIcon /> : <DarkModeIcon />}
                  >
                    {darkMode ? 'Light Mode' : 'Dark Mode'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>
        );
      
      default:
        return null;
    }
  };

  return (
    <MuiThemeProvider theme={theme(darkMode ? 'dark' : 'light')}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        {/* App Bar */}
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <IconButton
              color="inherit"
              edge="start"
              onClick={toggleDrawer}
              sx={{ mr: 2, display: { md: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
            <CodeIcon sx={{ mr: 1 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              AI Development Workflow
            </Typography>
            <IconButton color="inherit" onClick={toggleTheme}>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
            <IconButton color="inherit">
              <Badge badgeContent={4} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
            <IconButton color="inherit">
              <AccountCircleIcon />
            </IconButton>
          </Toolbar>
        </AppBar>

        {/* Sidebar */}
        <Drawer
          variant={isMobile ? 'temporary' : 'permanent'}
          open={isMobile ? mobileOpen : true}
          onClose={toggleDrawer}
          sx={{
            width: 240,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: 240,
              boxSizing: 'border-box',
              borderRight: 'none',
              bgcolor: 'background.paper',
              boxShadow: 1
            },
          }}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
        >
          <Toolbar /> {/* For proper spacing below app bar */}
          <Box sx={{ overflow: 'auto' }}>
            <List>
              {['Dashboard', 'Agents', 'Workflows', 'Analytics', 'Settings'].map((text, index) => (
                <ListItem 
                  key={text} 
                  disablePadding
                  selected={activeTab === index}
                  onClick={() => {
                    setActiveTab(index);
                    if (isMobile) setMobileOpen(false);
                  }}
                >
                  <ListItemButton>
                    <ListItemIcon>
                      {index === 0 && <DashboardIcon />}
                      {index === 1 && <PeopleIcon />}
                      {index === 2 && <BuildIcon />}
                      {index === 3 && <AssessmentIcon />}
                      {index === 4 && <SettingsIcon />}
                    </ListItemIcon>
                    <ListItemText primary={text} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>

        {/* Main content */}
        <Box component="main" sx={{ flexGrow: 1, p: 3, pt: 8 }}>
          {renderTabContent()}
        </Box>
      </Box>

      {/* Notification Snackbar */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </MuiThemeProvider>
  );
}

export default App;
