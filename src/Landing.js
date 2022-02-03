import React, { Component } from "react";
import "./App.css";
import ButtonAppBar from "./Header";
import Footer from "./Footer";
import TitlebarGridList from "./Cards";
//import MyButton from './components/Footer'
import header from "./country.jpg";
import SimplePopover from "./info"

import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
import mainReducer from './Components/reducers';
import thunkMiddleware from 'redux-thunk';
import { PersistGate } from 'redux-persist/integration/react'

import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { connect } from 'react-redux';

// import store from './Landing';
// let store = createStore(
//   mainReducer,
//   applyMiddleware(thunkMiddleware)
// );

const composeEnhancer = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;


const persistConfig = {
  key: 'data',
  storage: storage,
  whitelist: ['data'] // which reducer want to store
};
const pReducer = persistReducer(persistConfig, mainReducer);

const store = createStore(
  pReducer,
  applyMiddleware(thunkMiddleware,logger),
  // compose(batchedSubscribe(
  //   debounce(notify => {
  //     notify();
  //   })
  // )),
);

const persistor = persistStore(store);

class Landing extends Component {
  render() {
    return (
        <div id="wrap5">
        <ButtonAppBar />
        <div className="header-img">
        <img className="App-header-img" src={header} alt="Header" />
        <h2 class="centered1">The Forecasting Tool is a predictive application for the Global Health Impact Project. 
        This application allows users to manipulate various inputs to the Impact Score and see how the output is affected.</h2>
        <h3 class="centered">FORECASTING TOOL</h3>
        <h1 class="centered2">What would you like to forecast?</h1>
        </div>
        <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
        <TitlebarGridList />
        </PersistGate>
        </Provider>,
        <Footer/>
      </div>

    );
  }
}


function mapStateToProps(state1) {
  return state1;
}

const mapDispatchToProps = dispatch => ({
  //onCreatePressed : text=>dispatch(createForecast(text)),
  //onCreatePressed : text=>dispatch(addForecastRequest(text)),
  dispatch
});

export default connect(mapStateToProps, mapDispatchToProps)(Landing)
