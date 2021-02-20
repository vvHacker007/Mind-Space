import React, { Component } from "react"
const makeExpanding = (Target) => {
  return class extends Component {
    constructor(props) {
      super(props)
      this.state = { isOpen: false }
    }

    onClick = () => {
      this.setState({ isOpen: !this.state.isOpen })
    }

    render() {
      return (
        <Target
          {...this.props}
          isOpen={this.state.isOpen}
          onClick={this.onClick}
        />
      )
    }
  }
}
export default makeExpanding
