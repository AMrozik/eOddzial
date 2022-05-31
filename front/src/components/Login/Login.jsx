import React, {useContext} from 'react'
import AuthContext from '../../AuthContext'


export const Login = () => {
  let {loginUser} = useContext(AuthContext)
  return (
      <div>
            <form onSubmit={loginUser} className="form_style">
              <div className="form-group">
                <label>Adres Email</label>
                <input type="email" name="email" className="form-control" placeholder="Podaj email"/>
              </div>

              <div className="form-group">
                <label >Hasło</label>
                <input type="password" name="password" autoComplete="off" className="form-control" placeholder="Podaj password"/>
              </div>

              <button type="submit" className="btn btn-primary btn-block submit_margin_top">Zaloguj się</button>
            </form>
      </div>
  )
}

export default Login;
