import React, { Component } from "react";
import "./App.css";
import ButtonAppBar from "./Header";
import Footer from "./Footer";
import Results_country from "./Results_country";
import Results_company from "./Results_company";
import Results_disease from "./Results_disease";
import Results_drug from "./Results_drug";
import header from "./ghi_background-2.png";
import { apply } from "async";
//import MyButton from './components/Footer'

import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import {setState, setDictDataa, setData, setDict, setDict_1, setFullData, setData1} from './Components/actions';

import mainReducer from './Components/reducers';
import thunkMiddleware from 'redux-thunk';

import { connect } from 'react-redux';


export default function Error(){
    console.log("error")

    return(
        <div id="wrap">
        <ButtonAppBar />
        <div className="header-img">
          <img className="App-header-img" src={header} alt="Header" />
          <h1 class="centered4">Viva-La-Vida Forecasting Tool</h1>           
        </div>
        <p> refresh still in development, please press back. or home</p>
        </div>    
        );
}

// function mapStateToProps(state1) {
//     return state1;
//   }
  
//   const mapDispatchToProps = dispatch => ({
//     //onCreatePressed : text=>dispatch(createForecast(text)),
//     //onCreatePressed : text=>dispatch(addForecastRequest(text)),
//     dispatch
//   });
  
//   export default connect(mapStateToProps, mapDispatchToProps)(Error)