import React from 'react'
import axios from "axios";

export const getYearly = data => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']},

    });

    return instance.post('/yearlyAlg/', data)
};

export const getDaily = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.post('/dailyAlg/')
};

const apis = {
    getYearly,
    getDaily,
};

export default apis;
