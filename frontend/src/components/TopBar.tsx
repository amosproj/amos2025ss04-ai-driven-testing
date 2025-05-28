import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tooltip,
  IconButton,
  Tooltip as MuiTooltip,
} from '@mui/material';
import { Model } from '../api';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import MenuIcon from '@mui/icons-material/Menu';

interface TopBarProps {
  models: Model[];
  selectedModel: string;
  onChangeModel: (id: string) => void;
  onShutdownModel: () => void;
}

const TopBar: React.FC<TopBarProps> = ({ models, selectedModel, onChangeModel, onShutdownModel }) => {
  const selected = models.find((m) => m.id === selectedModel);

  return (
    <AppBar position="static" sx={{ bgcolor: 'common.white' }} elevation={1}>
      <Toolbar sx={{ display: 'flex', alignItems: 'center', position: 'relative' }}>
        <MuiTooltip title="Alte Chat-Verläufe (Coming soon)" placement="bottom">
          <span>
            <IconButton color="default">
              <MenuIcon />
            </IconButton>
          </span>
        </MuiTooltip>

        <Box sx={{ flexGrow: 1 }} />

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Box minWidth={240}>
            <FormControl fullWidth size="small">
              <InputLabel id="topbar-model-select-label">Modell</InputLabel>
              <Select
                labelId="topbar-model-select-label"
                value={selectedModel}
                label="Modell"
                onChange={(e) => onChangeModel(e.target.value as string)}
              >
                {models.map((m) => (
                  <MenuItem key={m.id} value={m.id}>
                    {m.name} {m.running ? '(Läuft)' : ''}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          <Tooltip title="Modell stoppen" placement="bottom">
            <span>
              <IconButton
                color="error"
                aria-label="Modell stoppen"
                disabled={!selected?.running}
                onClick={onShutdownModel}
              >
                <PowerSettingsNewIcon />
              </IconButton>
            </span>
          </Tooltip>
        </Box>

        <Typography
          variant="h6"
          component="div"
          sx={{
            position: 'absolute',
            left: '50%',
            transform: 'translateX(-50%)',
            color: 'common.black',
            pointerEvents: 'none',
          }}
        >
          AMOS LLM
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar; 