import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';

export default function Home() {
  return (
    <div>
      <title>ChatRooM V2</title>
      <AppBar position="static">
        <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
          <SearchIcon sx={{ color: 'action.active', mr: 1, my: 0.5 }} />
        <TextField id="search-owned-server" label="Search" variant="standard" />
      </Box>
      </AppBar>
    </div>
  );
}
