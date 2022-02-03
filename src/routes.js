import React from "react";
import { Route, IndexRoute } from "react-router";

/**
 * Import all page components here
 */
import App from "./App";
import Results from "./Result";
import Landing from "./Landing";
import Options from "./options";

/**
 * All routes go here.
 * Don't forget to import the components above after adding new route.
 */
export default (
  <Route path="/" component={App}>
    <Route path="/results" component={Results} />
    <Route path="/landing" component={Landing} />
    <Route path="/options" component={Options} />
    
  </Route>
);
