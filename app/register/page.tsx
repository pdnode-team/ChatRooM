'use client'; //DO NOT TOUCH THIS OR THE WHOLE PROJECT WILL BE MESSED UP

import "../globals.css";
import * as React from 'react';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Image from 'next/image';
import IconButton from '@mui/material/IconButton';
import Link from 'next/link';
import RegIcon from '@mui/icons-material/HowToReg';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { Typography } from "@mui/material";

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
        <div className='menu-home-ph-container' style={{width: '83.5vw'}}/>
        <Tooltip title="Account">
          <IconButton href="/login" sx={{marginRight: '10px'}}><AccountCircleIcon sx={{color: "#ffffff"}}/></IconButton>
        </Tooltip>
      </div>
      <Box className="back-box">
        <Tooltip title="Back to Login">
          <IconButton href="/login"><ArrowBackIcon sx={{fontSize: '35px'}}/></IconButton>
        </Tooltip>
        <Typography fontSize={'20px'}>Login</Typography>
      </Box>
      <div className="reg-container">
        <div className='reg-content'>
          <Box className="reg-header">
            <RegIcon sx={{color: "#1976d2", fontSize: '65px'}}/>
            <Typography variant="h4">Create an account</Typography>
            <Typography marginTop={'10px'}>Enter your Email address</Typography>
          </Box>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px', marginLeft: '100px', width: '50%'}}>
            <TextField label="Email address" variant="outlined" sx={{width: '90%'}}/>
            <Button variant="contained" sx={{marginTop: '15px', marginLeft: "80%", boxShadow: 'none', borderRadius: "100px"}}>Next</Button>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}
