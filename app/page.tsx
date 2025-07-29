'use client'; //DO NOT TOUCH THIS OR THE WHOLE PROJECT WILL BE MESSED UP
import * as React from 'react';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import Box from '@mui/material/Box';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import Image from 'next/image';
import IconButton from '@mui/material/IconButton';
import Link from 'next/link';

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
    <ThemeProvider theme={theme}>
      <title>ChatRooM V2</title>
      <div className='menu-home'>
        <Link href="/"><Image src="/icon.png" className='logo-icon' width="207" height="50" alt='ChatRooM Logo' priority/></Link>
        <Box sx={{display: 'flex', alignItems: 'flex-end'}}>
          <SearchIcon sx={{color: "#ffffff", marginRight: '10px', marginBottom: '1.6vh'}}/>
          <TextField color='white' id="joined-server-search" label="Search" variant="filled"/>
        </Box>
        <IconButton><AccountCircleIcon sx={{color: "#ffffff"}}/></IconButton>
      </div>
    </ThemeProvider>
  );
}
