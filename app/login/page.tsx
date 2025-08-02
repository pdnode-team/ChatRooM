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
import LoginIcon from '@mui/icons-material/Login';
import PasswordIcon from '@mui/icons-material/Lock';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import Typography from "@mui/material/Typography";
import UsernameIcon from '@mui/icons-material/Person';
import { useState } from "react";
import { useRouter } from "next/router";

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

export default function Login() {
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
        <Tooltip title="Back to Home">
          <IconButton href="/"><ArrowBackIcon sx={{fontSize: '35px'}}/></IconButton>
        </Tooltip>
        <Typography fontSize={'20px'}>Home</Typography>
      </Box>
      <div className='login-container'>
        <div className="login-content">
          <LoginIcon sx={{color: "#1976d2", fontSize: '65px', marginTop: '70px'}}/>
          <Typography variant="h4">Login to your account</Typography>
          <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%', marginTop: '10px'}}>
            <UsernameIcon sx={{color: "#747474", fontSize: '30px', marginRight: '10px'}}/>
            <TextField label="Username" variant="filled" type="username" sx={{width: '60%'}}/>
          </Box>
          <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%', marginTop: '10px'}}>
            <PasswordIcon sx={{color: "#747474", fontSize: '30px', marginRight: '10px'}}/>
            <TextField label="Password" variant="filled" type="password" sx={{width: '60%'}}/>
          </Box>
          <Button variant="contained" sx={{width: '33%', height: '48px', marginTop: '15px', boxShadow: 'none', fontSize: '15px'}}>Login</Button>
          <Typography sx={{marginTop: '10px'}}>Haven&apos;t got an account yet? <Link href="/register" style={{color: '#006fdeff', textDecoration: 'underline'}}>Create an account.</Link></Typography>
        </div>
      </div>
    </ThemeProvider>
  );
}
