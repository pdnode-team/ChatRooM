'use client'; //DO NOT TOUCH THIS OR THE WHOLE PROJECT WILL BE MESSED UP
import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import TextField from '@mui/material/TextField';
import Image from 'next/image';
import Link from 'next/link';

//别管这是干啥的，把要添加的新颜色写在这里面就行
declare module '@mui/material/styles' {
  interface Palette {
    ochre: Palette['primary'];
  }

  interface PaletteOptions {
    ochre?: PaletteOptions['primary'];
  }
}

//更新组件的颜色选项来包括其他颜色
declare module '@mui/material/Button' {
  interface ButtonPropsColorOverrides {
    ochre: true;
  }
}

const theme = createTheme({
  palette: {
    ochre: {
      main: '#E3D026',
      light: '#E9DB5D',
      dark: '#A29415',
      contrastText: '#242105',
    },
  },
});

export default function Home() {
  return (
    <ThemeProvider theme={theme}>
      <div>
        <title>ChatRooM V2</title>
        <AppBar position="static" className='appbar-home'>
          <Link href="/"><Image src="/icon.png" className='logo-icon' width="207" height="50" alt='ChatRooM Logo' priority/></Link>
          <Box sx={{ display: 'flex', alignItems: 'flex-end', position: 'absolute', right: '1%', top: '0.9vh'}}>
            <SearchIcon sx={{color: 'action.active', mr: 1, my: 0.5}} />
          <TextField color='ochre' id="joined-server-search" label="Search" variant="standard"/>
        </Box>
        </AppBar>
      </div>
    </ThemeProvider>
  );
}
