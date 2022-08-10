import React from 'react'
import axios from "axios";

export const getAll = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get('/operation_types/')
};

export const get = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get(`/operation_type/${id}/`);
};

export const create = data => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.post("/operation_types/", data);
};

export const update = (id, data) => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.put(`/operation_type/${id}/`, data);
};

export const remove = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.delete(`/operation_type/${id}/`);
};
// I will leave this here just in case one day we need it (remember to uncomment export)
//export const removeAll = () => {
//    return http.delete(`/rooms/`);
//};

const apis = {
    getAll,
    get,
    create,
    update,
    remove,
//    removeAll
};

export default apis;
