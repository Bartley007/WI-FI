import React from 'react'
import { createRoot } from 'react-dom/client'
import AppRouter from './app/router.jsx'
import './styles/global.css'

createRoot(document.getElementById('root')).render(<AppRouter />)
