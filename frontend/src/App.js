import React, { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'

import { AuthContext, UserContext } from './contexts'
import api from './api'
import { SignIn } from "./pages";


function App() {
  let navigate = useNavigate();

  const [loggedIn, setLoggedIn] = useState(null)
  const [user, setUser] = useState({})
  const location = useLocation()

  const authorization = ({
    email, password
  }) => {
    api.signin({
      email, password
    }).then(res => {
      if (res.auth_token) {
        localStorage.setItem('token', res.auth_token)
        api.getUserData()
          .then(res => {
            setUser(res)
            setLoggedIn(true)
          })
          .catch(err => {
            setLoggedIn(false)
            navigate("/signin")
          })
      } else {
        setLoggedIn(false)
      }
    })
      .catch(err => {
        const errors = Object.values(err)
        if (errors) {
          alert(errors.join(', '))
        }
        setLoggedIn(false)
      })
  }

  return (
    <AuthContext.Provider value={loggedIn}>
      <UserContext.Provider value={user}>

        <div>
          <Routes>
            <Route exact path='/signin' element={
              <SignIn
                onSignIn={authorization} />
            } />
          </Routes>
        </div>

      </UserContext.Provider>
    </AuthContext.Provider>
  )
}

export default App;
