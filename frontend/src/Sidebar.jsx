import React, { useState } from 'react';
import { 
  Drawer, 
  List, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText, 
  useTheme, 
  IconButton,
  Box,
  useMediaQuery,
  Tooltip,
  Divider,
  Typography
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import TableChartIcon from '@mui/icons-material/TableChart';
import BarChartIcon from '@mui/icons-material/BarChart';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import DownloadIcon from '@mui/icons-material/Download';
import SettingsIcon from '@mui/icons-material/Settings';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import WorkIcon from '@mui/icons-material/Work';
import VisibilityIcon from '@mui/icons-material/Visibility';

const DRAWER_WIDTH = 240;
const COLLAPSED_WIDTH = 65;

const navItems = [
  { key: 'dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
  { key: 'applications', label: 'Applications', icon: <TableChartIcon /> },
  { key: 'show-all', label: 'Show All', icon: <VisibilityIcon />, action: true },
  { key: 'visualizations', label: 'Visualizations', icon: <BarChartIcon /> },
  { divider: true },
  { key: 'calendar', label: 'Calendar', icon: <CalendarMonthIcon /> },
  { key: 'export', label: 'Export CSV', icon: <DownloadIcon /> },
  { key: 'settings', label: 'Settings', icon: <SettingsIcon /> },
];

const Sidebar = ({ onNavigate, activePage, onShowAll }) => {
  const theme = useTheme();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const drawerWidth = isCollapsed ? COLLAPSED_WIDTH : DRAWER_WIDTH;

  const handleItemClick = (item) => {
    if (item.action && item.key === 'show-all') {
      onShowAll();
    } else {
      onNavigate(item.key);
    }
  };

  return (
    <Drawer
      variant="permanent"
      anchor="left"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        transition: theme.transitions.create(['width'], {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.enteringScreen,
        }),
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: `1px solid ${theme.palette.divider}`,
          transition: theme.transitions.create(['width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
          }),
          overflowX: 'hidden',
          backgroundColor: theme.palette.background.default,
        },
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: isCollapsed ? 'center' : 'space-between',
          padding: theme.spacing(2),
          minHeight: 64,
        }}
      >
        {!isCollapsed && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <WorkIcon color="primary" />
            <Typography variant="h6" color="primary">Job Tracker</Typography>
          </Box>
        )}
        {isCollapsed && <WorkIcon color="primary" />}
        <IconButton 
          onClick={() => setIsCollapsed(!isCollapsed)}
          sx={{
            ...(!isCollapsed && {
              marginLeft: 1,
            }),
          }}
        >
          {isCollapsed ? <ChevronRightIcon /> : <ChevronLeftIcon />}
        </IconButton>
      </Box>

      <Divider />

      {/* Navigation List */}
      <List sx={{ pt: 1 }}>
        {navItems.map((item, index) => {
          if (item.divider) {
            return <Divider key={`divider-${index}`} sx={{ my: 1 }} />;
          }

          const isActive = activePage === item.key;
          const listItem = (
            <ListItemButton
              key={item.key}
              onClick={() => handleItemClick(item)}
              selected={isActive}
              sx={{
                minHeight: 48,
                px: 2.5,
                ...(isCollapsed && {
                  justifyContent: 'center',
                  px: 2,
                }),
                ...(isActive && {
                  bgcolor: `${theme.palette.primary.main}15 !important`,
                  borderRight: `3px solid ${theme.palette.primary.main}`,
                }),
                '&:hover': {
                  bgcolor: `${theme.palette.primary.main}08`,
                },
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: isCollapsed ? 0 : 2,
                  justifyContent: 'center',
                  color: isActive ? theme.palette.primary.main : theme.palette.text.secondary,
                }}
              >
                {item.icon}
              </ListItemIcon>
              {!isCollapsed && (
                <ListItemText
                  primary={item.label}
                  sx={{
                    opacity: isCollapsed ? 0 : 1,
                    color: isActive ? theme.palette.primary.main : theme.palette.text.primary,
                  }}
                />
              )}
            </ListItemButton>
          );

          return isCollapsed ? (
            <Tooltip key={item.key} title={item.label} placement="right">
              {listItem}
            </Tooltip>
          ) : (
            listItem
          );
        })}
      </List>
    </Drawer>
  );
};

export default Sidebar;
