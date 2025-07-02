import React from 'react';
import { Box, Typography, Paper, LinearProgress, Chip } from '@mui/material';
import { green, orange, red } from '@mui/material/colors';

interface CodeCoverageProps {
  coverage: {
    coverage_percentage?: number;
    lines_covered?: number;
    lines_total?: number;
    branch_coverage?: number;
    uncovered_lines?: number[];
    coverage_data?: any;
    error?: string;
    status?: string;
  };
}

const CodeCoverageDisplay: React.FC<CodeCoverageProps> = ({ coverage }) => {
  if (coverage.error) {
    return (
      <Paper variant="outlined" sx={{ p: 2, mt: 1, bgcolor: red[50] }}>
        <Typography variant="subtitle2" color="error" sx={{ fontWeight: 'bold', mb: 1 }}>
          Code Coverage Analysis Failed
        </Typography>
        <Typography variant="body2" color="error">
          {coverage.error}
        </Typography>
      </Paper>
    );
  }

  if (!coverage.coverage_percentage) {
    return null;
  }

  const getCoverageColor = (percentage: number) => {
    if (percentage >= 80) return green[500];
    if (percentage >= 60) return orange[500];
    return red[500];
  };

  const coveragePercentage = coverage.coverage_percentage || 0;
  const coverageColor = getCoverageColor(coveragePercentage);

  return (
    <Paper variant="outlined" sx={{ p: 2, mt: 1, bgcolor: 'background.paper' }}>
      <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
        🔍 Code Coverage Analysis
      </Typography>
      
      <Box sx={{ mb: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="body2">Coverage</Typography>
          <Typography variant="body2" sx={{ fontWeight: 'bold', color: coverageColor }}>
            {coveragePercentage.toFixed(1)}%
          </Typography>
        </Box>
        <LinearProgress
          variant="determinate"
          value={coveragePercentage}
          sx={{
            height: 8,
            borderRadius: 4,
            '& .MuiLinearProgress-bar': {
              backgroundColor: coverageColor,
            },
          }}
        />
      </Box>

      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 1 }}>
        {coverage.lines_covered && coverage.lines_total && (
          <Chip
            label={`${coverage.lines_covered}/${coverage.lines_total} lines`}
            size="small"
            variant="outlined"
          />
        )}
        
        {coverage.branch_coverage && (
          <Chip
            label={`${coverage.branch_coverage.toFixed(1)}% branches`}
            size="small"
            variant="outlined"
          />
        )}
        
        {coverage.uncovered_lines && coverage.uncovered_lines.length > 0 && (
          <Chip
            label={`${coverage.uncovered_lines.length} uncovered lines`}
            size="small"
            color="warning"
            variant="outlined"
          />
        )}
      </Box>

      {coverage.uncovered_lines && coverage.uncovered_lines.length > 0 && (
        <Box sx={{ mt: 1 }}>
          <Typography variant="caption" color="text.secondary">
            Uncovered lines: {coverage.uncovered_lines.slice(0, 10).join(', ')}
            {coverage.uncovered_lines.length > 10 && '...'}
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default CodeCoverageDisplay;
