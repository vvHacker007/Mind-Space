import React, { useState } from "react"
import { ReactComponent as CloseMenu } from "./x.svg"
import { ReactComponent as MenuIcon } from "./menu.svg"
import { ReactComponent as Logo } from "./logo.svg"
import "./Navbar.css"

const Navbar = () => {
  const [click, setClick] = useState(false)
  const handleClick = () => setClick(!click)
  const closeMobileMenu = () => setClick(false)
  return (
    <div className="header">
      <div className="logo-nav">
        <div className="logo-container">
          <a href="#">
            <Logo className="logo" />
            <p className="brand">Mind Space</p>
          </a>
        </div>
        <ul className={click ? "nav-options active" : "nav-options"}>
          <li className="option" onClick={closeMobileMenu}>
            <a href="#">ABOUT</a>
          </li>
          <li className="option" onClick={closeMobileMenu}>
            <a href="#">SERVICES</a>
          </li>
          <li className="option" onClick={closeMobileMenu}>
            <a href="#">STORIES</a>
          </li>
          <li className="option" onClick={closeMobileMenu}>
            <a href="#">CONTACT</a>
          </li>
          <li className="option mobile-option" onClick={closeMobileMenu}>
            <a href="" className="sign-up">
              SIGN-UP
            </a>
          </li>
        </ul>
      </div>
      <ul className="signin-up">
        <li onClick={closeMobileMenu}>
          <a href="" className="signup-btn">
            SIGN-UP
          </a>
        </li>
      </ul>
      <div className="mobile-menu" onClick={handleClick}>
        {click ? (
          <CloseMenu className="menu-icon" />
        ) : (
          <MenuIcon className="menu-icon" />
        )}
      </div>
    </div>
  )
}

export default Navbar
