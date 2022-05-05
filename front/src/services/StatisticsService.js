import http from "../http-common";
import React from 'react'
import axios from "axios";

export const getAll = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']},
        params: {
        'start_year':'2021',
        'start_month':'12',
        'start_day':'1',
        'end_year':'2023',
        'end_month':'1',
        'end_day':'1'
        }
    });

//    temporary solution
    return instance.get('/statistics/')
};

export default {
    getAll
};
