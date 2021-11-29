import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from './pages/Home';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Nav from './components/Nav';
import Ordynator from './pages/Ordynator';
import Medic from './pages/Medic';
import PrivateRoute from './PrivateRoute';
import {AuthProvider} from './AuthContext';


function App() {

    return (
        <div className="App">

            <BrowserRouter>
                <AuthProvider>
                <Nav/>
                <Routes>
                    <Route path="/" exact element={<PrivateRoute/>}>
                        <Route path="/" exact element={<Home/>} />
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
                </AuthProvider>
            </BrowserRouter>

        </div>
    );
}

export default App;
