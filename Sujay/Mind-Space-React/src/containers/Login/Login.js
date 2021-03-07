import React, { Component } from "react"
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider"
import "./login.css"
import Particles from "react-particles-js"
const particleOptions = {
    "particles": {
        "number": {
            "value": 200,
            "density": {
                "enable": true,
                "value_area": 1202.559045649142
            }
        },
        "color": {
            "value": "#000000"
        },
        "shape": {
            "type": "circle",
            "stroke": {
                "width": 0,
                "color": "#000000"
            },
        },
        "opacity": {
            "value": 0.8,
            "random": false,
            "anim": {
                "enable": false,
                "speed": 1,
                "opacity_min": 0.1,
                "sync": false
            }
        },
        "size": {
            "value": 5,
            "random": true,
            "anim": {
                "enable": false,
                "speed": 40,
                "size_min": 0.1,
                "sync": false
            }
        },
        "line_linked": {
            "enable": true,
            "distance": 250,
            "color": "#000000",
            "opacity": 0.4,
            "width": 1
        },
        "move": {
            "enable": true,
            "speed": 7,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": false,
            "attract": {
                "enable": false,
                "rotateX": 600,
                "rotateY": 1200
            }
        }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": {
                "enable": true,
                "mode": "repulse"
            },
            "onclick": {
                "enable": true,
                "mode": "push"
            },
            "resize": true
        },
        "modes": {
            "grab": {
                "distance": 400,
                "line_linked": {
                    "opacity": 1
                }
            },
            "repulse": {
                "distance": 150,
                "duration": 0.4
            },
            "push": {
                "particles_nb": 4
            },
            "remove": {
                "particles_nb": 2
            }
        }
    },
    "retina_detect": true
  }
class Login extends Component 
{
    constructor(props) 
    {
      super(props)
      this.state = {}
    }
    render() {
      return (
        <div className="login">  
            {/* <!-- particles.js container --> */}
            <Particles className="particles" params={particleOptions} />
            <div class="container">
                <div class="d-flex justify-content-center h-100">
                    <div class="card">
                        <div class="card-header">
                            <h3>Sign In</h3>
                            <div class="d-flex justify-content-end social_icon">
                                <span><i class="fab fa-facebook-square"></i></span>
                                <span><i class="fab fa-google-plus-square"></i></span>
                                <span><i class="fab fa-twitter-square"></i></span>
                            </div>
                        </div>
                        <div class="card-body">
                            <form method="POST">
                                <div class="input-group form-group">
                                    <input type="text" class="form-control" placeholder="Username" name="user_name" required/>
                                </div>
                                <div class="input-group form-group">
                                    <input type="password" class="form-control" placeholder="Password" name="pass" required/>
                                </div>
                                <div class="row align-items-center remember">
                                    <p><input type="checkbox" name="cb" id="cb1"/><label for="cb1">Remeber Me</label></p>
                                </div>
                                <div class="form-group">
                                    <input type="submit" value="Login" class="btn float-right login_btn"/>
                                </div>
                            </form>
                        </div>
                        <div class="card-footer">
                            <div class="d-flex justify-content-center links">
                                Don't have an account?<a href="/signup/" id="linking">Sign Up</a>
                            </div>
                            <div class="d-flex justify-content-center links">
                                <a href="/forgot_password/ " id="linking">Forgot your password?</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        )
    }
}
  export default Login