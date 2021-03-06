import React from "react"
import { Route, Switch } from "react-router-dom"
import { BrowserRouter as Router } from "react-router-dom";
import Home from "./Home/Home"

function App() {
  return (
    <Router>
      <main>
      <Switch>
          <Route path="/" exact component={Home} />
        {/* <Route component={Error} /> */}
      </Switch>
    </main>
    </Router>
    
  )
}

export default App
