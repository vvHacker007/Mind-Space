import React, { Component } from "react"
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider"
import Searchbox from "../../components/Searchbox"
import "./Home.css"
import Navbar from "./Navbar.js"

const animationStyle = {
  transition: "width 0.75s cubic-bezier(0.000, 0.795, 0.000, 1.000)",
}
class Home extends Component {
  constructor(props) {
    super(props)
    this.state = { isOpen: false }
  }
  onClick = () => {
    this.setState({ isOpen: !this.state.isOpen })
  }
  render() {
    return (
      <div className="home">
        {/* <nav
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
                    <Searchbox
                      {...this.state}
                      isOpen={this.state.isOpen}
                      onClick={this.onClick}
                      additionalStyles={{
                        text: animationStyle,
                        frame: animationStyle,
                      }}
                    />
                  </MuiThemeProvider>
                </li>
              </ul>
            </div>
          </div>
        </nav> */}

        <div className="home-head">
          <Navbar />
          <div class="container">
            <h1>MIND SPACE</h1>
            <p>A mint of creativity...</p>
            <button>FIND OUT MORE</button>
          </div>
        </div>
      </div>
    )
  }
}

export default Home
