import React, { Component } from "react"
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider"
import Searchbox from "../../components/Searchbox"
import makeExpanding from "../../components/expanding-animation"
// import Stats from "../../components/Stats"
// import Category from "../../components/Category"
// import Complaint from "../../components/Complaint"
// import Login from "../../components/Login"
// import Logout from "../../components/Logout"
import "./Home.css"

const ExpandingSearchBox = makeExpanding(Searchbox)

class Home extends Component {
  render() {
    return (
      <div className="home">
        <nav
          class="navbar navbar-expand-lg navbar-light fixed-top py-3"
          id="mainNav"
        >
          <div class="container">
            <a class="navbar-brand js-scroll-trigger" href="#page-top">
              Mind Space
            </a>
            <button
              class="navbar-toggler navbar-toggler-right"
              type="button"
              data-toggle="collapse"
              data-target="#navbarResponsive"
              aria-controls="navbarResponsive"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
              <ul class="navbar-nav ml-auto my-2 my-lg-0">
                <li class="nav-item">
                  <a class="nav-link js-scroll-trigger" href="#about">
                    About
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link js-scroll-trigger" href="#services">
                    Services
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link js-scroll-trigger" href="#stats">
                    Stories
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link js-scroll-trigger" href="#contact">
                    Contact
                  </a>
                </li>
                <li class="nav-item">
                  <MuiThemeProvider>
                    <ExpandingSearchBox />
                  </MuiThemeProvider>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </div>
    )
  }
}

export default Home
