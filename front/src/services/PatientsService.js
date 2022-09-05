import React from 'react'
import axios from "axios";

export const getAll = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get('/patients/')
};

export const get = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get(`/patient/${id}/`);
};

export const create = data => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.post("/create_patient/", data);
};

export const update = (id, data) => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.put(`/update_patient/${id}/`, data);
};

export const remove = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.delete(`/delete_patient/${id}/`);
};

const apis = {
    getAll,
    get,
    create,
    update,
    remove,
//    removeAll
};

export default apis;