import React, { useState, Component } from "react"
import { ReactComponent as CloseMenu } from "./x.svg"
import { ReactComponent as MenuIcon } from "./menu.svg"
import "./Navbar.css"
// import { render } from "@testing-library/react"

const Navbar = () => {
  const [click, setClick] = useState(false)
  const [navbar, setNavbar] = useState(false)
  const handleClick = () => setClick(!click)
  const closeMobileMenu = () => setClick(false)
  const changeBackground = () => {
    if (window.scrollY >= 711) {
      setNavbar(true)
    } else {
      setNavbar(false)
    }
  }
  window.addEventListener("scroll", changeBackground)

  return (
    <div className={navbar ? "header active" : "header"}>
      <div className="logo-nav">
        <div className="logo-container">
          <a href="#">
            <p className="brand">Mind Space</p>
          </a>
        </div>
        <ul className={click ? "nav-options active" : "nav-options"}>
          <li
            className={navbar ? "option active" : "option"}
            onClick={closeMobileMenu}
          >
            <a href="#">ABOUT</a>
          </li>
          <li
            className={navbar ? "option active" : "option"}
            onClick={closeMobileMenu}
          >
            <a href="#">SERVICES</a>
          </li>
          <li
            className={navbar ? "option active" : "option"}
            onClick={closeMobileMenu}
          >
            <a href="#">STORIES</a>
          </li>
          <li
            className={navbar ? "option active" : "option"}
            onClick={closeMobileMenu}
          >
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
        <li className="sign-up-item" onClick={closeMobileMenu}>
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
