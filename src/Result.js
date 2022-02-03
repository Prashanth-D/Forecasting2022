import React, { Component } from "react";
import "./App.css";
import ButtonAppBar from "./Header";
import Footer from "./Footer";
import Results_country from "./Results_country";
import Results_company from "./Results_company";
import Results_disease from "./Results_disease";
import Results_drug from "./Results_drug";
import Results_specification from "./Results_specification";
import companyheader from "./company_background.png";
import diseaseheader from "./disease_background.png";
import drugheader from "./drug_background.png";
import header from "./ghi_background-2.png";
import { apply } from "async";
import { batch } from 'react-redux'

//import MyButton from './components/Footer'

import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
import {setState, setDictDataa, setData, setDict, setDict_1, setFullData, setData1} from './Components/actions';

import mainReducer from './Components/reducers';
import thunkMiddleware from 'redux-thunk';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
//import MyButton from './components/Footer'
import { connect } from 'react-redux';



import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import Error from "./error";
import { PersistGate } from 'redux-persist/integration/react'


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


class Result extends Component {


  constructor(props){
    super(props);
    // this.state = {text:'',inputText:'',mode:'view'};
  }


  render() {

    let data = {};
    let new_Data = {};
    let new_dict= {};
    let diff_specs = {};

    if(this.props.full_data1 == undefined ){
      console.log(this.props); 


      return (
        
        // <div id="wrap">
        // <ButtonAppBar />
        // <div className="header-img">
        //   <img className="App-header-img" src={header} alt="Header" />
        //   <h1 class="centered4">Viva-La-Vida Forecasting Tools Results</h1>
        //    <h2 class="centered5">Main Options>Specifications><span class="bold">Results</span></h2>
           
        // </div>
        // <p>Results refresh still in development, please press back. or home</p>
        // </div>
        <Error/>
      )
    }

    else if(this.props.location.data == undefined){
      //data = this.props.data
      console.log("dadada"); 
      //data.state = "Country";
      console.log(this.props); 

      new_Data = this.props.full_data1.dict;
      new_dict = this.props.full_data1.data;
      data.state = this.props.full_data1.state;
      data.data = this.props.data2;
      console.log(new_Data);
      console.log(new_dict);

      // console.log(this.props);
      // data.state = this.props.data.state;
      // data.full_data.dict = this.props.data.full_data1.dict;
      // data.full_data.data = this.props.data.full_data1.data;
      // console.log(new_dict);
      //delete new_dict["Original Impact Score"]

      for (const x in new_dict){
        if(new_Data[x] !== new_dict[x]){
          diff_specs[x] = new_dict[x] - new_Data[x];
        }
      }

      for (const y in diff_specs){
        if(diff_specs[y] < 0){
          diff_specs[y] = "decrease";
        }
        else{
          diff_specs[y] = "increase";
        }
      }

      console.log(diff_specs);

      data["diff_specs"] = diff_specs;

      console.log(data);

      if(data.state == "Country"){
        return (
          <div id="wrap5">
            <ButtonAppBar />
            <div className="header-img">
              <img className="Results-header-img" src={header} alt="Header"/>
              <h1 class="countryresults-TextHeader">Country Forecasting Tools Results</h1>
               <h2 class="countryresults-Route">Main Options>Specifications><span class="bold">Results</span></h2>
               <a href="javascript:history.back()">Go Back</a>
               <br></br>
            </div>
            <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Country Results</Tab>
                                <Tab>Company Results</Tab>
                                <Tab>Disease Results</Tab>
                                <Tab>Drug Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}> 
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_country data={data.data}/>  
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_company data={data.data}/>
                                </PersistGate> 
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_disease data={data.data}/> 
                                </PersistGate>  
                                </Provider>                          
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_drug data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_specification data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
    
            </div>
              <Footer/>
    
           
    
            
          </div>
        );
        }
        else if(data.state == "Company"){
          return (
            <div id="wrap5">
              <ButtonAppBar />
              <div className="header-img">
                <img className="Results-header-img" src={companyheader} alt="companyheader" />
                <h1 class="companyresults-TextHeader">Company Forecasting Tools Results</h1>
                 <h2 class="companyresults-Route">Main Options>Specifications><span class="bold">Results</span></h2>
                 <a href="javascript:history.back()">Go Back</a>
                 <br></br>
              </div>
              <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Company Results</Tab>
                                <Tab>Country Results</Tab>
                                <Tab>Disease Results</Tab>
                                <Tab>Drug Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_company data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_country data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_disease data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_drug data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_specification data={data.data}/>
                                </PersistGate>
                                </Provider>
                              <TabPanel>
                              </TabPanel>
                            </Tabs>
          
            
             </div>
                <Footer/>
    
              
            </div>
          );
        }
        else if(data.state == "Disease"){
          return (
            <div id="wrap5">
              <ButtonAppBar />
              <div className="header-img">
                <img className="Results-header-img" src={diseaseheader} alt="diseaseheader" />
                <h1 class="countryresults-TextHeader">Disease Forecasting Tools Results</h1>
                 <h2 class="countryresults-Route">Main Options>Specifications<span class="bold">Results</span></h2>
                 <a href="javascript:history.back()">Go Back</a>
                 <br></br>
              </div>
                <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Disease Results</Tab>
                                <Tab>Country Results</Tab>
                                <Tab>Company Results</Tab>
                                <Tab>Drug Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_disease data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_country data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_company data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_drug data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_specification data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
              </div>
                <Footer/>
    
             
      
              
            </div>
          );
        }
        else if(data.state == "Drug"){
          return (
            <div id="wrap5">
              <ButtonAppBar />
              <div className="header-img">
                <img className="Results-header-img" src={drugheader} alt="drugheader" />
                <h1 class="drugresults-TextHeader">Drug Forecasting Tools Results</h1>
                 <h2 class="drugresults-Route">Main Options>Specifications><span class="bold">Results</span></h2> 
                 <a href="javascript:history.back()">Go Back</a>
                 <br></br>
              </div>
                  <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Drug Results</Tab>
                                <Tab>Country Results</Tab>
                                <Tab>Company Results</Tab>
                                <Tab>Disease Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}>
                                <Results_drug data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}>
                                <Results_country data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}>
                                <Results_company data={data.data}/>
                                </PersistGate>
                                </Provider>
    
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}>
                                <Results_disease data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                              <PersistGate loading={null} persistor={persistor}> 
                                <Results_specification data={data.data}/>
                                </PersistGate>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
                 </div>
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
    


    else{
      let data_data_result = this.props.location.data.data;
      let full_data_result = this.props.location.data.full_data;
      let data_state_result = this.props.location.data.state;
      batch(() => {
        this.props.dispatch(setData1(data_data_result))
        this.props.dispatch(setFullData(full_data_result))
        this.props.dispatch(setState(data_state_result))
      });
      data = this.props.location.data
      let result_data = data.data
      console.log(data);
      console.log(data.data);
      console.log(this.props.location.data.full_data);
      

      console.log(this.props);

      new_Data = data.full_data.dict;
      new_dict = data.full_data.data;
      console.log(new_dict);

      //delete new_dict["Original Impact Score"]

      for (const x in new_dict){
        if(new_Data[x] !== new_dict[x]){
          diff_specs[x] = new_dict[x] - new_Data[x];
        }
      }

      for (const y in diff_specs){
        if(diff_specs[y] < 0){
          diff_specs[y] = "decrease";
        }
        else{
          diff_specs[y] = "increase";
        }
      }

      console.log(diff_specs);

      data.data["diff_specs"] = diff_specs;
      
      console.log(data);
     

      console.log(data);

      if(data.state == "Country"){
        return (
          <div id="wrap5">
            <ButtonAppBar />
            <div className="header-img">
              <img className="Results-header-img" src={header} alt="Header" />
              <h1 class="countryresults-TextHeader">Country Forecasting Tools Results</h1>
               <h2 class="countryresults-Route">Main Options>Specifications><span class="bold">Results</span></h2>
               <a href="javascript:history.back()">Go Back</a>
               <br></br>
            </div>
            <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Country Results</Tab>
                                <Tab>Company Results</Tab>
                                <Tab>Disease Results</Tab>
                                <Tab>Drug Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}> 
                                <Results_country data={data.data}/>  
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_company data={data.data}/> 
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_disease data={data.data}/>   
                                </Provider>                          
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_drug data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_specification data={data.data}/>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
    
            </div>
              <Footer/>
    
           
    
            
          </div>
        );
        }
        else if(data.state == "Company"){
          return (
            <div id="wrap5">
              <ButtonAppBar />
              <div className="header-img">
                <img className="Results-header-img" src={companyheader} alt="companyheader" />
                <h1 class="companyresults-TextHeader">Company Forecasting Tools Results</h1>
                 <h2 class="companyresults-Route">Main Options>Specifications><span class="bold">Results</span></h2>
                 <a href="javascript:history.back()">Go Back</a>
                 <br></br>
              </div>
              <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Company Results</Tab>
                                <Tab>Country Results</Tab>
                                <Tab>Disease Results</Tab>
                                <Tab>Drug Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}>
                                <Results_company data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_country data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_disease data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_drug data={data.data}/>
                                </Provider>
                              </TabPanel>

                              <TabPanel>
                              <Provider store={store}>
                                <Results_specification data={data.data}/>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
             </div>
                <Footer/>
    
              
            </div>
          );
        }
        else if(data.state == "Disease"){
          return (
            <div id="wrap5">
              <ButtonAppBar />
              <div className="header-img">
                <img className="Results-header-img" src={diseaseheader} alt="diseaseheader" />
                <h1 class="countryresults-TextHeader">Disease Forecasting Tools Results</h1>
                 <h2 class="countryresults-Route">Main Options>Specifications><span class="bold">Results</span></h2>
                 <a href="javascript:history.back()">Go Back</a>
                 <br></br>
              </div>
                <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Disease Results</Tab>
                                <Tab>Country Results</Tab>
                                <Tab>Company Results</Tab>
                                <Tab>Drug Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}>
                                <Results_disease data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_country data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_company data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_drug data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_specification data={data.data}/>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
              </div>
                <Footer/>
    
             
      
              
            </div>
          );
        }
        else if(data.state == "Drug"){
          return (
            <div id="wrap5">
              <ButtonAppBar />
              <div className="header-img">
                <img className="Results-header-img" src={drugheader} alt="drugheader" />
                <h1 class="drugresults-TextHeader">Drug Forecasting Tools Results</h1>
                 <h2 class="drugresults-Route">Main Options>Specifications><span class="bold">Results</span></h2> 
                 <a href="javascript:history.back()">Go Back</a>
                 <br></br>
              </div>
                  <div id="row">
                             <Tabs>
                              <TabList>
                                <Tab>Drug Results</Tab>
                                <Tab>Country Results</Tab>
                                <Tab>Company Results</Tab>
                                <Tab>Disease Results</Tab>
                                <Tab>Specifications</Tab>
                              </TabList>
    
                              <TabPanel>
                              <Provider store={store}>
                                <Results_drug data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_country data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_company data={data.data}/>
                                </Provider>
    
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_disease data={data.data}/>
                                </Provider>
                              </TabPanel>
                              <TabPanel>
                              <Provider store={store}>
                                <Results_specification data={data.data}/>
                                </Provider>
                              </TabPanel>
                            </Tabs>
          
            
                 </div>
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
}

function mapStateToProps(state1) {
  return state1;
}

const mapDispatchToProps = dispatch => ({
  //onCreatePressed : text=>dispatch(createForecast(text)),
  //onCreatePressed : text=>dispatch(addForecastRequest(text)),
  dispatch
});

export default connect(mapStateToProps, mapDispatchToProps)(Result);
