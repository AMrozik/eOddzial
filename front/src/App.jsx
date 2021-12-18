import './App.css';
import {AuthProvider} from './AuthContext';
import IdleTimerContainer from './components/Timeout';
import {Nav} from './components/Nav';
import {BrowserRouter} from "react-router-dom";

import 'devextreme/dist/css/dx.light.css';

function App() {

    return (
        <div className="App">
            <BrowserRouter>
                <AuthProvider>
                    <IdleTimerContainer />
                    <Nav/>
                </AuthProvider>
            </BrowserRouter>
        </div>
    );
}

export default App;
