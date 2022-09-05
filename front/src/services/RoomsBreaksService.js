import React from 'react'
import axios from "axios";

export const getAll = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get('/not_available_rooms/')
};

export const get = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get(`/not_available_room/${id}/`);
};

export const create = data => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.post("/not_available_rooms/", data);
};

export const update = (id, data) => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.put(`/not_available_room/${id}/`, data);
};

export const remove = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.delete(`/not_available_room/${id}/`);
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