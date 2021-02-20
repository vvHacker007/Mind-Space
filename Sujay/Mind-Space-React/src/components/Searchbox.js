import React from "react"
import { TextField, IconButton } from "material-ui"
import SearchIcon from "material-ui/svg-icons/action/search"
import cross from "./cross.png"
//import CloseRoundedIcon from '@material-ui/icons/CloseRounded';
const SearchBox = ({ isOpen, onClick, additionalStyles }) => {
  const baseStyles = {
    open: {
      width: "180px",
    },
    closed: {
      width: "0px",
    },
    smallsearchIcon: {
      width: 30,
      height: 30,
    },
    icon: {
      position: "absolute",
      right: 0,
      height: "10px",
      width: "10px",
      background: "transparent",
      textAlign: "center",
      lineHeight: "35px",
      fontSize: "1em",
      color: "Black",
      cursor: "pointer",
      zIndex: 1,
      top: "-3px",
      transition: "all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    },
    frame: {
      border: "solid 0px black",
      borderRadius: 5,
      position: "relative",
      height: "35px",
      width: "35px",
      transition: "all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)",
      top: "-8px",
    },
  }

  let textStyle = isOpen ? baseStyles.open : baseStyles.closed
  textStyle = Object.assign(
    textStyle,
    additionalStyles ? additionalStyles.text : {}
  )

  const divStyle = Object.assign(
    {},
    textStyle,
    baseStyles.frame,
    additionalStyles ? additionalStyles.frame : {}
  )
  divStyle.width += baseStyles.icon.width + 5

  let iconDisplay = () => {
    if (!isOpen) {
      return <SearchIcon />
    } else return <img src={cross} alt="X" />
  }

  return (
    <div style={divStyle}>
      <IconButton
        iconStyle={baseStyles.smallsearchIcon}
        style={baseStyles.icon}
        onClick={() => onClick()}
      >
        {iconDisplay()}
        {/* <SearchIcon />
        <img src={cross} alt="X" /> */}
      </IconButton>
      <TextField name="Search..." style={textStyle} />
    </div>
  )
}
export default SearchBox
