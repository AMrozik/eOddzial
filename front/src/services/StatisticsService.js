import React from 'react'
import axios from "axios";

export const getAll = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const date = new Date();
    var year = date.getFullYear();

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']},
        params: {
        'start_year':year,
        'start_month':1,
        'start_day':1,
        'end_year':year,
        'end_month':12,
        'end_day':31
        }
    });

//    temporary solution
    return instance.get('/statistics/')
};

export default {
    getAll
};
