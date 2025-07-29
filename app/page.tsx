import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import Image from 'next/image';

export default function Home() {
  return (
    <div>
      <title>ChatRooM V2</title>
      <AppBar position="static" className='appbar-home' sx={{background: "#1976d2", height: '8vh', width: '100vw'}}>
        <Image src="/icon.png" width="207" height="50" alt='ChatRooM Logo' priority style={{position: 'absolute', left: '1vw', top: '0.9vh'}}/>
        <Box sx={{ display: 'flex', alignItems: 'flex-end', position: 'absolute', right: '1%', top: '0.9vh'}}>
          <SearchIcon sx={{ color: 'action.active', mr: 1, my: 0.5 }} />
        <TextField id="search-owned-server" label="Search" variant="standard" />
      </Box>
      </AppBar>
    </div>
  );
}
