import http from "../http-common";
import React from 'react'
import axios from "axios";

export const getAll = () => {

    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });


    // return http.get("/rooms/", {"Authorization":"Bearer "+a['access']});
    return instance.get('/rooms/')
};

export const get = id => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.get(`/rooms/${id}/`);
};

export const create = data => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    return instance.post("/rooms/", data);
};

export const update = (id, data) => {
    let a = JSON.parse(localStorage.getItem('authTokens'));

    const instance = axios.create({
        baseURL: 'http://localhost:8000/api',
        timeout: 1000,
        headers: {'Authorization': 'Bearer ' + a['access']}
    });

    console.log(data)

    return instance.put(`/rooms/${id}/`, data);
};

export const remove = id => {
    return http.delete(`/rooms/${id}/`);
};

export const removeAll = () => {
    return http.delete(`/rooms/`);
};

export default {
    getAll,
    get,
    create,
    update,
    remove,
    removeAll
};
