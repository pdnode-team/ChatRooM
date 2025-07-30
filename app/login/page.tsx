'use client'; //DO NOT TOUCH THIS OR THE WHOLE PROJECT WILL BE MESSED UP

import "../globals.css";
import * as React from 'react';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Image from 'next/image';
import IconButton from '@mui/material/IconButton';
import Link from 'next/link';
import LoginIcon from '@mui/icons-material/Login';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

//别管这是干啥的，把要添加的新颜色写在这里面就行
declare module '@mui/material/styles' {
  interface Palette {
    white: Palette['primary'];
  }

  interface PaletteOptions {
    white?: PaletteOptions['primary'];
  }
}

//更新组件的颜色选项来包括其他颜色
declare module '@mui/material/Button' {
  interface ButtonPropsColorOverrides {
    white: true;
  }
}

const theme = createTheme({
  palette: {
    white: {
      main: '#ffffffff',
    },
  },
});

export default function Home() {
  return (
    <ThemeProvider theme={theme}> {/*明确使用自定义主题*/}
      <title>ChatRooM V2</title>
      <div className='menu-home'>
        <Link href="/"><Image src="/icon.png" className='logo-icon' width="207" height="50" alt='ChatRooM Logo' priority/></Link>
        <div className='menu-home-ph-container'/>
        <Box sx={{display: 'flex', alignItems: 'flex-end', marginRight: '10px'}}>
          <SearchIcon sx={{color: "#ffffff", marginRight: '10px', marginBottom: '1.6vh', fontSize: '28px'}}/>
          <Tooltip title="Search in joined servers">
            <TextField color='white' id="joined-server-search" label="Search" variant="filled"/>
          </Tooltip>
        </Box>
        <Tooltip title="Add Servers">
          <IconButton><AddIcon sx={{color: "#ffffff"}}/></IconButton>
        </Tooltip>
        <Tooltip title="Account">
          <IconButton sx={{marginRight: '10px'}}><AccountCircleIcon sx={{color: "#ffffff"}}/></IconButton>
        </Tooltip>
      </div>
      <div className='login-container'>
        <LoginIcon/>
      </div>
    </ThemeProvider>
  );
}
