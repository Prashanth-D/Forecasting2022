import React, { Component } from "react";
import "./App.css";
import ButtonAppBar from "./Header";
import Footer from "./Footer";
import App from "./App";
import App1 from "./App";
import { apply } from "async";
//import MyButton from './components/Footer'
import header from "./ghi_background-2.png";

import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
import {setState, setDictDataa, setData, setDict, setDict_1} from './Components/actions';

import mainReducer from './Components/reducers';
import thunkMiddleware from 'redux-thunk';
import { connect } from 'react-redux';


import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

import { PersistGate } from 'redux-persist/integration/react'

//import store from './Landing';

//import TitlebarGridList from "./Cards";
//import MyButton from './components/Footer'

// let store = createStore(
//   mainReducer,
//   applyMiddleware(thunkMiddleware)
// );

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


class Slider extends Component {



  render() {
    // const { data } = this.props.location
    let data = {};
    let data_temp = {};
    
    console.log(this.props.data1)
    console.log(this.props)
    console.log(this.props.state)

    if(this.props.location.data == undefined){
      console.log(this.props.data1)
      data.data = this.props.data1
      data.dict_dataa = this.props.dict_dataa1
      data.state = this.props.state
    }
    else{
      data  = this.props.location.data
      console.log(data.data)
      this.props.dispatch(setData(this.props.location.data.data))
      this.props.dispatch(setDictDataa(this.props.location.data.dict_dataa))
      this.props.dispatch(setState(this.props.location.data.state))
    }
 
    console.log(data);
    //console.log(state);
    let dict_1 = {};
    let dict = {};

    var keys = [];
    var values = [];
    let updated_dict = data;
    const dataArray = data.data;
 
//  let marks =[
//    {value:min1,
//     label:min1,
//    },
//    {value:max1,
//     label:max1,
//    }
//  ]
//  let marks_arr = []
//  marks_arr.push(marks)
    for(var k in dataArray) {
      keys.push(k);
      values.push(dataArray[k])
      //dict.push({key:k, value:dataArray[k]});
      dict[k] = dataArray[k];
    }
    dict_1 = data.data;
    data.dict = dict;
    data.dict_1 = dict_1;
    console.log(dict_1);
    console.log(data);
    console.log(keys);
    console.log(values);
    
    return (
      
      <div id="wrap5">
        <ButtonAppBar />
        <div className="header-img">
          <img className="Options-header-img" src={header} alt="Header" />
          <h1 class="options_TextHeader"><span class="bold">{data.dict_dataa.state}</span> Forecasting Tools</h1>
             <h2 class="options_Route">Main Options><span class="bold">Specifications</span>>Results</h2> 
             <a href="javascript:history.back()">Go Back</a>
        </div>
        <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}> 
        <App data={data}/>
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

export default connect(mapStateToProps, mapDispatchToProps)(Slider);
