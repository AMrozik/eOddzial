import { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext()
export default AuthContext;
export const AuthProvider = ({children}) => {

    const apiUrl = 'http://127.0.0.1:8000/api'
    const aT = 'authTokens'
    const jwtToken = localStorage.getItem(aT)
    let [authTokens, setAuthTokens]  = useState(()=> jwtToken ? JSON.parse(jwtToken) : null)
    let [user, setUser] = useState(()=> jwtToken ? jwt_decode(jwtToken) : null)
    let [loading, setLoading] = useState(true)
    let navigate = useNavigate()
    const ref = {'refresh':authTokens?.refresh}
    const head = {'Content-Type':'application/json'}
    const met = 'POST'
    const str = JSON.stringify

    let loginUser = async (event) => {
        event.preventDefault()
        let response = await fetch(apiUrl + '/token/', {
            method:met,
            headers:head,
            body:str({
                'email': event.target.email.value,
                'password': event.target.password.value
            })
        })
        let data = await response.json()
        if(response.status !== 200){
            alert('Error!')
        }else{
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem(aT, str(data))
            navigate('/home');
        }
    }

    let logoutUser = async () => {
        let response = await fetch(apiUrl + '/logout/', {
            method:met,
            headers:head,
            body:str(ref)
        })
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem(aT)
        navigate('/login')
    }

    let updateToken = async ()=> {

        let response = await fetch(apiUrl + '/token/refresh/', {
            method:met,
            headers:head,
            body:str(ref)
        })

        let data = await response.json()

        if (response.status !== 200){
            logoutUser()
        }else{
            setAuthTokens(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem(aT, str(data))
        }

        if(loading){
            setLoading(false)
        }
    }

    let contextData = {
        user:user,
        authTokens:authTokens,
        loginUser:loginUser,
        logoutUser:logoutUser
    }

    useEffect(()=> {

        if(loading){
            if(authTokens){
                updateToken()
            } else {
                setLoading(false)
            }
        }

        let interval = setInterval(()=> {
            if(authTokens){
                updateToken()
            }
        }, 240000)
        return ()=> clearInterval(interval)

    }, [authTokens, loading])

    return(
        <AuthContext.Provider value={contextData}>
            {!loading && children}
        </AuthContext.Provider>
    )
}