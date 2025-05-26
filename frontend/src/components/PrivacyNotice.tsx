import React from 'react';
import { Box, Typography, styled } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import GavelIcon from '@mui/icons-material/Gavel';

const Container = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: theme.spacing(1),
  padding: theme.spacing(1),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.mode === 'light' ? theme.palette.grey[300] : theme.palette.grey[700],
}));

interface InfoBarProps {
  licence: string;
  licenceLink: string;
}

const InfoBar: React.FC<InfoBarProps> = ({ licence, licenceLink }) => (
  <Container>
    <LockIcon fontSize="small" />
    <Typography variant="body2" fontWeight={700} whiteSpace="nowrap">
      Privacy: Hosted locally
    </Typography>
    <Typography variant="body2" color="text.secondary">
      |
    </Typography>
    <GavelIcon fontSize="small" />
    <Typography
      variant="body2"
      component="a"
      href={licenceLink}
      target="_blank"
      rel="noopener"
      sx={{ textDecoration: 'none', fontWeight: 700, ml: 0.5 }}
      whiteSpace="nowrap"
    >
      {licence}
    </Typography>
  </Container>
);

export default InfoBar; 