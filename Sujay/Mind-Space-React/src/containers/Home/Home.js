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
