import './App.css';
import {AuthProvider} from './AuthContext';
import IdleTimerContainer from './components/Timeout';
import {NavigationBar} from './components/NavigationBar/NavigationBar';
import {BrowserRouter} from "react-router-dom";

import 'devextreme/dist/css/dx.light.css';
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
