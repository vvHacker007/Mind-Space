import React from "react"
import { Route, Switch } from "react-router-dom"
import { BrowserRouter as Router } from "react-router-dom";
import Home from "./Home/Home"
import Login from "./Login/Login"
import Signup from "./Signup/Signup"
function App() {
  return (
    <Router>
      <main>
      <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/login/" exact component={Login} />
          <Route path="/signup/" exact component={Signup} />
        {/* <Route component={Error} /> */}
      </Switch>
    </main>
    </Router>
    
  )
}

export default App
