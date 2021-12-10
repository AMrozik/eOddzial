import React, { useState, useRef, useContext } from 'react'
import IdleTimer from 'react-idle-timer'
import Modal from 'react-modal'
import AuthContext from '../AuthContext'

Modal.setAppElement('#root')
function IdleTimerContainer () {
  const [modalIsOpen, setModalIsOpen] = useState(false)
  const idleTimerRef = useRef(null)
  const sessionTimeoutRef = useRef(null)
  let {user, logoutUser} = useContext(AuthContext)

  const onIdle = () => {
    console.log('Użytkownik jest nieaktywny')
    setModalIsOpen(true)
    sessionTimeoutRef.current = setTimeout(todo, 5000)
  }
  const logOut = () => {
    setModalIsOpen(false)
    clearTimeout(sessionTimeoutRef.current)
    console.log('Użytkownik został wylogowany')
  }
  const stay = () => {
    setModalIsOpen(false)
    clearTimeout(sessionTimeoutRef.current)
    console.log('Użytkownik jest aktywny')
  }

  function todo () {
  logoutUser()
  logOut()
  }

  return (
    <div>
      {user &&
          <IdleTimer
            ref={idleTimerRef}
            timeout={1000 * 5}
            onIdle={onIdle}
          />
      }
      <Modal isOpen={modalIsOpen}>
        <h2>Jesteś nieaktywny przez jakiś czas!</h2>
        <p>Wkrótce zostaniesz wylogowany</p>
        <div>
          <button onClick={todo}>Wyloguj mnie</button>
          <button onClick={stay}>Nie wylogowuj mnie</button>
        </div>
      </Modal>
    </div>
  )
}

export default IdleTimerContainer