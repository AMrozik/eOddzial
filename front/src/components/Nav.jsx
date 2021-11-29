import React, {useContext} from 'react'
import { Link } from 'react-router-dom'
import AuthContext from '../AuthContext'

const Nav = () => {
    let {user, logoutUser} = useContext(AuthContext)
    return (
        <div>
            <Link to="/">Home</Link>
            <span> | </span>
            {user && user.is_ordynator ? ( <Link to="/ordynator">Ordynator</Link>
            ):(user && user.is_medic && <Link to="/medic">Medic</Link>)}
            <span> | </span>
            {user ? (
                <Link onClick={logoutUser} to="/logout">Logout</Link>
            ) : (
                <Link to="/login">Login</Link>
            )}
            {user && user.is_ordynator &&<p>Hello ordynator {user.full_name} </p>}
            {user && user.is_medic &&<p>Hello medic {user.full_name} </p>}
            {user && user.is_planist &&<p>Hello planist {user.full_name} </p>}
        </div>
    )
}

export default Nav
