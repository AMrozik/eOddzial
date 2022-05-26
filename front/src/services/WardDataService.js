import http from "../http-common";
import React from 'react'
import axios from "axios";

export const get = () => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get("/ward_data/");
};

export const create = data => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.post("/create_ward_data/", data);
};

export const update = data => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.put("/ward_data/", data);
};

export default {
    get,
    create,
    update
};
