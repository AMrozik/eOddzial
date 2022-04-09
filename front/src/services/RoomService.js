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
    return http.get(`/room/${id}`);
};

export const create = data => {
    return http.post("/rooms/", data);
};

export const update = (id, data) => {
    return http.put(`/rooms/${id}`, data);
};

export const remove = id => {
    return http.delete(`/rooms/${id}`);
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
