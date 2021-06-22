import React, {Fragment, useState, useEffect } from 'react';
import './App.css';
import {BrowserRouter as Router, Switch, Route, Redirect} from "react-router-dom";

// Components

import Schedule from "./components/Schedule";
import Predictor from "./components/Predictor";
import Rankings from "./components/Rankings";
import Header from "./components/Header";


function App() {

  return (
    <Fragment>
      <Router>
      <Header />

        <div className="container">
          <Switch>
          <Route exact path="/" >
            <Predictor />
          </Route>

          <Route exact path="/schedule" >
            <Schedule />
          </Route>

          <Route exact path="/rankings" >
            <Rankings />
          </Route>

          </Switch>
        </div>
      </Router>
    </Fragment>
  );
}

export default App;