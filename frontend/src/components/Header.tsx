import { useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';

const tabs = [
  'Runs',
  'Pull requests',
  'Issues',
  'History',
  'Service log',
  'Repositories',
  'Agents & prompts',
];

function Header() {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <AppBar
      component="header"
      position="static"
      elevation={0}
      sx={{
        bgcolor: '#1B1B1D',
        borderBottom: '3px solid #A3122B',
        padding: '0 24px',
        flexDirection: 'row',
        alignItems: 'center',
        gap: '28px',
        minHeight: '55px', // 52px bar + 3px red line, as in the mockup
      }}
    >
      <Typography
        component="span"
        sx={{ color: '#FFFFFF', fontSize: '17px', fontWeight: 700, lineHeight: 'normal' }}
      >
        AI PR Reviewer
      </Typography>

      <Tabs
        component="nav"
        aria-label="Pages"
        value={activeTab}
        onChange={(_event, newValue: number) => setActiveTab(newValue)}
        sx={{
          minHeight: 0,
          '& .MuiTabs-list': { gap: '22px' },
          '& .MuiTabs-indicator': { backgroundColor: '#A3122B', height: '2px' },
        }}
      >
        {tabs.map((label) => (
          <Tab
            key={label}
            label={label}
            disableRipple
            sx={{
              minWidth: 0,
              minHeight: 0,
              maxWidth: 'none',
              padding: '14px 0',
              fontSize: '14px',
              fontWeight: 400,
              lineHeight: 'normal',
              letterSpacing: 'normal',
              textTransform: 'none',
              color: '#C9C9CC',
              opacity: 1,
              '&.Mui-selected': { color: '#FFFFFF', fontWeight: 600 },
            }}
          />
        ))}
      </Tabs>

      <Typography
        component="span"
        sx={{ marginLeft: 'auto', color: '#C9C9CC', fontSize: '13px', lineHeight: 'normal' }}
      >
        4 repos · 7 agents
      </Typography>
    </AppBar>
  );
}

export default Header;
