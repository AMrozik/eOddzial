import React, {useContext} from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../AuthContext'

import {BrowserRouter, Route, Routes} from "react-router-dom";

import Home from '../pages/Home';
import Login from '../pages/Login';
import Logout from '../pages/Logout';
import Ordynator from '../pages/Ordynator';
import Medic from '../pages/Medic';
import PrivateRoute from '../PrivateRoute';

export const Nav = () => {
    let {user, logoutUser} = useContext(AuthContext)
    return (
        <div>
            {user && (<Link to="/home">Home</Link>
            )}
            <span> | </span>
            {user && user.is_ordynator ? ( <Link to="/ordynator">Ordynator</Link>
            ):(user && user.is_medic && <Link to="/medic">Medic</Link>)}
            <span> | </span>
            {user ? (
                <Link onClick={logoutUser} to="/logout">Logout</Link>
            ) : (
                <Link to="/login">Login</Link>
            )}

            <Routes>
                <Route path="/home" exact element={<PrivateRoute/>}>
                    <Route path="/home" exact element={<Home/>} />
                </Route>
                <Route path="/ordynator" exact element={<PrivateRoute/>}>
                    <Route path="/ordynator" exact element={<Ordynator/>} />
                </Route>
                <Route path="/medic" exact element={<PrivateRoute/>}>
                    <Route path="/medic" exact element={<Medic/>} />
                </Route>
                <Route path="/login" element={<Login/>} />
                <Route path="/logout" element={<Logout/>} />
            </Routes>
        </div>
    )
};
