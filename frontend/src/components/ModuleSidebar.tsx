import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  Typography,
  Box,
  Switch,
  FormControlLabel,
  Tooltip,
  IconButton,
  styled,
} from '@mui/material';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { Module } from '../api';

interface ModuleSidebarProps {
  open: boolean;
  onClose: () => void;
  modules: Module[];
  selectedModules: string[];
  onModuleToggle: (moduleId: string) => void;
}

const SidebarHeader = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: theme.spacing(2),
  borderBottom: `1px solid ${theme.palette.divider}`,
}));

const LogoContainer = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
});

const Logo = styled('img')({
  width: '32px',
  height: '32px',
  borderRadius: '4px',
});

const ButtonGroup = styled(Box)({
  display: 'flex',
  gap: '8px',
});

const ModuleSidebar: React.FC<ModuleSidebarProps> = ({
  open,
  onClose,
  modules,
  selectedModules,
  onModuleToggle,
}) => {
  return (
    <Drawer anchor="left" open={open} onClose={onClose}>
      <SidebarHeader>
        <LogoContainer>
          <Logo
            src="https://avatars.githubusercontent.com/u/80108293?s=200&v=4"
            alt="AMOS Logo"
          />
          <Typography variant="h6">AI-Tester</Typography>
        </LogoContainer>
        <ButtonGroup>
          <Tooltip title="Schließen X">
            <IconButton size="small" onClick={onClose}>
              <ChevronLeftIcon />
            </IconButton>
          </Tooltip>
        </ButtonGroup>
      </SidebarHeader>

      <Box sx={{ p: 2 }}>
        <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 'bold' }}>
          Module
        </Typography>
        <List>
          {modules.map((module) => (
            <ListItem
              key={module.id}
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-start',
                mb: 2,
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={selectedModules.includes(module.id)}
                      onChange={() => onModuleToggle(module.id)}
                    />
                  }
                  label={<Typography variant="subtitle2">{module.name}</Typography>}
                />
                <Tooltip
                  title={
                    <Box>
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        {module.description}
                      </Typography>
                      <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                        {module.applies_before
                          ? '✅ Aktiv vor Prompt'
                          : '❌ Inaktiv vor Prompt'}
                      </Typography>
                      <Typography variant="caption" display="block">
                        {module.applies_after
                          ? '✅ Aktiv nach Prompt'
                          : '❌ Inaktiv nach Prompt'}
                      </Typography>

                      {/* Show dependencies in tooltip */}
                      {module.dependencies.length > 0 && (
                        <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                          <strong>Dependencies:</strong> {module.dependencies.join(', ')}
                        </Typography>
                      )}
                    </Box>
                  }
                >
                  <IconButton size="small">
                    <InfoOutlinedIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              </Box>

              {/* Optional: show dependencies below the switch */}
              {module.dependencies.length > 0 && (
                <Box sx={{ ml: 4, mt: 0.5 }}>
                  <Typography variant="caption" color="text.secondary">
                    Benötigt folgende Module: {module.dependencies.join(', ')}
                  </Typography>
                </Box>
              )}
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default ModuleSidebar;
