import React, { Component } from "react";
import "./App.css";
import ButtonAppBar from "./Header";
import Footer from "./Footer";
import Mainoption_country from "./Mainmenu_country";
import Mainoption_company from "./Mainmenu_company";
import Mainoption_drug from "./Mainmenu_drug";
import Mainoption_disease from "./Mainmenu_disease";
import header from "./ghi_background-2.png";
import "./App.css";
import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
import {setState} from './Components/actions';

import mainReducer from './Components/reducers';
import thunkMiddleware from 'redux-thunk';

import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import Error from "./error";
import { PersistGate } from 'redux-persist/integration/react'


import { connect } from 'react-redux';
//import TitlebarGridList from "./Cards";
//import MyButton from './components/Footer'

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


class Options extends Component {

  constructor(props){
    super(props);
    this.state = {text:'', inputText:'', mode:'country'}
    this.handleChange = this.handleChange.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
  }

  handleChange(e){
   this.setState({inputText: e.target.value});

  }

  handleSave(e){
    //this.setState({text: this.state.inputText, mode:'country'});
  }

  handleEdit(e){
    //this.setState({mode: 'company'});
  }


  render() {

    let data  = this.props.location.state
    console.log(data);

    if(String(data) === ("Country")){
      return (
        <div id="wrap5">
          <ButtonAppBar />
          <div className="header-img">
          <img className="Options-new-header-img" src={header} alt="Header"/>
            <h1 class="options_TextHeader"><span class="bold">Country</span> Forecasting Tools</h1>
             <h2 class="options_Route"><span class="bold">Main Options</span>>Specifications>Results</h2>
          </div>
        <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
        <Mainoption_country data={data}/>
        </PersistGate>
        </Provider>,
        <Footer/>

        </div>

        
        );
        
    }
    else if(data === "Company"){
      return (
        <div id="wrap5">
          <ButtonAppBar />
          <div className="header-img">
          <img className="Options-new-header-img" src={header} alt="Header"/>
            <h1 class="options_TextHeader"><span class="bold">Company</span> Forecasting Tools</h1>
             <h2 class="options_Route"><span class="bold">Main Options</span>>Specifications>Results</h2>
          </div>
        <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
        <Mainoption_company data={data}/>
        </PersistGate>
        </Provider>,
        <Footer/>

        </div>
        );
    }
    else if(data === "Drug"){
      return (
      <div id="wrap5">
          <ButtonAppBar />
          <div className="header-img">
          <img className="Options-new-header-img" src={header} alt="Header"/>
            <h1 class="options_TextHeader"><span class="bold">Drug</span> Forecasting Tools</h1>
             <h2 class="options_Route_drug"><span class="bold">Main Options</span>>Specifications>Results</h2> 
          </div>
      <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
      <Mainoption_drug data={data}/>
      </PersistGate>
      </Provider>,
      <Footer/>

      </div>
        );
    }
    else if(data === "Disease"){
      return (
        <div id="wrap5">
            <ButtonAppBar />
            <div className="header-img">
            <img className="Options-new-header-img" src={header} alt="Header"/>
              <h1 class="options_TextHeader"><span class="bold">Disease</span> Forecasting Tools</h1>
             <h2 class="options_Route"><span class="bold">Main Options</span>>Specifications>Results</h2>  
            </div>
      <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
      <Mainoption_disease data={data}/>
      </PersistGate>
      </Provider>,
      <Footer/>

      </div>
        );
    }
    else{
      console.log("error 404")
      return (
        <Error/>
      );
    }   
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

export default connect(mapStateToProps, mapDispatchToProps)(Options);
