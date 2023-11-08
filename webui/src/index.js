import {createRoot} from 'react-dom/client';
import React from 'react'
import ReactDOM from 'react-dom'


export function runMainPage() {
    document.addEventListener('DOMContentLoaded', () => {
        const container = document.createElement('div');
        container.style.width = '100%';
        container.style.height = '100%';
        document.body.appendChild(container);
        console.log('open sim, preload:', window.PRELOAD);
        const root = createRoot(container);
    });
}


window.main_page = runMainPage

