import './App.css';
import {AuthProvider} from './AuthContext';
import IdleTimerContainer from './components/Timeout';
import {NavigationBar} from './components/NavigationBar/NavigationBar';
import {BrowserRouter} from "react-router-dom";

import 'devextreme/dist/css/dx.light.css';
<<<<<<< HEAD
=======
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
>>>>>>> 90db70cf8106d62f5e72c4f8845037e80487f438
import {Footer} from "./components/Footer/Footer";

function App() {

    return (
        <div className="App">
            <BrowserRouter>
                <AuthProvider>
                    <IdleTimerContainer />
                    <NavigationBar/>
                </AuthProvider>
            </BrowserRouter>
            <Footer/>
        </div>
    );
}

export default App;
