import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import Result from "./Result";
import Landing from "./Landing";
import Options from "./options";
import Slider from "./slider";

import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
// import { batchedSubscribe } from "redux-batched-subscribe";
// import { debounce } from "lodash";
//import {setState, setDictDataa, setData, setDict, setDict_1} from './Components/actions';

import mainReducer from './Components/reducers';
import thunkMiddleware from 'redux-thunk';

import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';


import * as serviceWorker from "./serviceWorker";
import {
  Route,
  BrowserRouter as Router,
  HashRouter,
  Redirect,
} from "react-router-dom";
import routes from "./routes";

// const store = configureStore();
// const persistor = persistStore(store);


const persistConfig = {
  key: 'data',
  storage: storage,
  whitelist: ['data'] // which reducer want to store
};
const pReducer = persistReducer(persistConfig, mainReducer);

export const store = createStore(
  pReducer,
  applyMiddleware(thunkMiddleware,logger),
  // compose(batchedSubscribe(
  //   debounce(notify => {
  //     notify();
  //   })
  // )),
);

export const persistor = persistStore(store);



ReactDOM.render(
  // <Provider store = {configureStore()}>
  //   <PersistGate 
  //     loading={<div>Loading...</div>}
  //     persistor={persistor}
  //   >
  <Provider store={store}>
  <Router>
    <Route exact path="/" component={Landing} />
    <Route exact path="/landing" component={Landing} />
    <Route exact path="/slider" component={Slider} />
    <Route exact path="/options" component={Options} />
    <Route exact path="/result" component={Result} />
  </Router>,
  {/* // </PersistGate> */}
  </Provider>,

  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();