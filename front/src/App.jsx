import './App.css';
import {AuthProvider} from './AuthContext';
import IdleTimerContainer from './components/Timeout';
import {NavigationBar} from './components/NavigationBar/NavigationBar';
import {BrowserRouter} from "react-router-dom";

import 'devextreme/dist/css/dx.light.css';
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
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
            <div id="yolo"></div>
            <Footer/>
        </div>
    );
}

export default App;
