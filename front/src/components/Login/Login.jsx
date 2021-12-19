import React, {useContext} from 'react'
import AuthContext from '../../AuthContext'
import './Login.css';

export const Login = () => {
  let {loginUser} = useContext(AuthContext)
  return (
      <div>
            <form onSubmit={loginUser} className="form_style">
              <div className="form-group">
                <label>Email</label>
                <input type="email" name="email" className="form-control" placeholder="Enter email"/>
              </div>

              <div className="form-group">
                <label >Password</label>
                <input type="password" name="password" autoComplete="off" className="form-control" placeholder="Enter password"/>
              </div>

              <button type="submit" className="btn btn-primary btn-block submit_margin_top">Submit</button>
            </form>
      </div>
  )
}

export default Login;
