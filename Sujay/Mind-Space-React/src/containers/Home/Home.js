import React, { Component } from "react"
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider"
import Searchbox from "../../components/Searchbox"
import "./Home.css"

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
        </nav>
        <div className="home-head">
          <div class="container h-100">
            <div class="row h-100 align-items-center justify-content-center text-center">
              <div class="col-lg-10 align-self-end">
                <h1 class="text-uppercase text-white font-weight-bold">
                  Mind Space
                </h1>
                <hr class="divider my-4" />
              </div>
              <div class="col-lg-8 align-self-baseline">
                <p class="text-white-75 font-weight-light mb-5">
                  A mint of Creativity...
                </p>
                <a
                  class="btn btn-primary btn-xl js-scroll-trigger"
                  href="#about"
                >
                  Find Out More
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Home
