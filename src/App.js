import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import axios from "axios";
//import { makeStyles } from '@material-ui/core/styles';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import logo from "./logo.png";
import header from "./forecast.jpg";
import "./App.css";
import "react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css";
import RangeSlider from "react-bootstrap-range-slider";
import { ThemeProvider } from "@material-ui/styles";
import { createMuiTheme } from '@material-ui/core/styles';
import Slider from '@material-ui/core/Slider';
import Button from "@material-ui/core/Button"
import { batch } from 'react-redux'
import Box from "@material-ui/core/Box";
import Tooltip from "@material-ui/core/Tooltip";

import Error from './error'

import { connect } from 'react-redux';

import {setData, setDict, setDict_1, setDictDataa} from './Components/actions';

import {
  Row,
  Col,
  Form,
  Navbar,
  Nav,
  NavDropdown,
  FormControl,
} from "react-bootstrap";

// You can choose your kind of history here (e.g. browserHistory)
//import { Router } from "react-router";
// Your routes.js file
//import routes from "./routes";
import { Link, withRouter, NavLink, useHistory } from "react-router-dom";

const useStyles = makeStyles(theme => ({
  root: {
    width: 600,
  },
  margin: {
    height: theme.spacing(3),
  },
  disabled: {
    color: theme.palette.primary.main
  },
  thumb: {
    height: 30,
    width: 60
  },
  label: {
    color: '#FFF000'
  },
  indicator: {
    backgroundColor: '#FFF'
  }
  
  
}));

const muiTheme = createMuiTheme({
  overrides:{
    MuiSlider: {
      thumb:{
      //color: "black",     
      },
      valueLabel:{
        color: "black"
      }
    }
}
});

function ValueLabelComponent(props) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} interactive enterTouchDelay={0} title={value}>
      {children}
    </Tooltip>
  );
}
/*const useStyles = makeStyles((theme) => ({
  root: {
    width: 600,
  },
  margin: {
    height: theme.spacing(3),
  },
})); */

function valuetext(value) {
  return `${value}°C`;
}



console.log("dict_1");

function App1(data){
  
}

let dict;
let dict_1;

function delete1(key) {
   if(this.hasKey(key)) {
      delete this.container[key];
      return true;
   }
   return false;
}


function App(data) {
  console.log(data);
//  const { data } = props.location
const classes = useStyles();
dict  = data.data.dict;
dict_1 = data.data.dict_1;

delete dict["Original Impact Score"]

const state = data.data.state
console.log(dict)
console.log(dict_1)


  
//const {x,y} = dataArray
//console.log(dataArray)
let min1 = 0;
let max1 = 100;
let i = -1;

  const [value, setValue1] = React.useState({});
  // const [value2, setValue2] = useState(values[1]*100);
  // const [value3, setValue3] = useState(values[2]);
  // const [value4, setValue4] = useState(values[3]*100);
  // const [value5, setValue5] = useState(values[4]);

  const history = useHistory();

  function simulateNetworkRequest() {
    return new Promise((resolve) => setTimeout(resolve, 2000));
  }

  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (isLoading) {
      simulateNetworkRequest().then(() => {
        setLoading(false);
      });
    }
  }, [isLoading]);

  const handleClick = () => {
    setLoading(true);
    
    // if(data.data.length == undefined){
    //   console.log("error");
    //   return(
    //     <div><Error/></div>
    //   );
    // }

    batch(() => {
      data.dispatch(setDict(dict))
      data.dispatch(setDict_1(dict_1))
      data.dispatch(setDictDataa(data.data.dict_dataa))
      data.dispatch(setData(data.data))
    });
    let xx

    if(Object.prototype.hasOwnProperty.call(data.data.data, 'Original Impact Score')){
      xx = data.data;
    }
    else{
      xx = data.data1;
    }

    console.log(Object.prototype.hasOwnProperty.call(data.data.data, 'Original Impact Score'));
    {
    axios
        .post(
          "/get_result",
          {
              updated_specification: xx,
          },
          { headers: { "content-type": "application/json" } }
          )
          .then((res) => {
            console.log(res)
            const results = Array.from(res.data);
            console.log(res.data);
            //this.props.history.push({pathname: '/slider', data: {data:res.data, state: this.props.selectedState}});
            history.push({pathname: '/result', data :{ data: res.data, state: state, full_data: data.data,} } );
            //alert(res.data);
          });
    ///axios
    }
    //history.push({pathname: '/result', data :{ data: dict, state: state} } );
  };  

  const handleClick1 = () => {
    history.push("/");
  };

  //ReactDOM.App(<Router routes={routes} />, document.getElementById("your-app"));

  const handleChange=(changeEvent)=>{
    //setValue1({[key]: changeEvent.target.value});
    //console.log(key);
    console.log(Object.keys(value));
    console.log(changeEvent.target.ariaValueNow);

    dict_1[Object.keys(value)] = parseFloat(changeEvent.target.ariaValueNow);
    console.log(dict_1);
  };

  return (
    //console.log(value.key)
    <div>
        <div id="wrap3">
          <h2>Specifications</h2>
          <Form>
            <Form.Group as={Row}>
            {Object.keys(dict).map((key, value) => {
              max1 = 100;
              i = i + 1

              /// TB ///

              {if(key == "TB Prevalence"){
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 33000;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 330000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 3300000;
                }
              }}
             


              {if(key== "TB/HIV+ DALYs"){
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 2100;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 21000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 210000;
                }
                if(dict[key] >= 99999){
                  max1 = 2100000;
                }
              }}
              {if(key== "TB/HIV- DALYs"){
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 2100;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 21000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 210000;
                }
                if(dict[key] >= 99999){
                  max1 = 2100000;
                }
                  
              }}

              {if(key== "MDR-TB DALYs"){
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 3000;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 30000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 300000;
                }
                if(dict[key] >= 99999){
                  max1 = 3000000;
                }
              }}

              {if(key== "XDR-TB DALYs"){
                  //min1 = 0;
                  if(dict[key] <= 999 || dict[key] >= 0){
                    max1 = 2800;
                  }
  
                  if(dict[key] < 9999 || dict[key] > 999){
                    max1 = 28000;
                  }
  
                  if(dict[key] >= 9999 || dict[key] < 99999){
                    max1 = 280000;
                  }
              }}


              /// Malaria ///

              {if(key == "Malaria Prevalence"){
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 25000;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 25000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 250000;
                }
                if(dict[key] >= 99999){
                  max1 = 2500000;
                }
              }}

              {if(key== "Malaria PFalc DALY"){
                //min1 = 0;
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 25100;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 251000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 2510000;
                }
                if(dict[key] >= 99999){
                  max1 = 25100000;
                }
            }}

            /// HIV ///


            {if(key== "Adults Needing Treatment"){
              if(dict[key] <= 999 || dict[key] >= 0){
                max1 = 9999;
              }

              if(dict[key] < 9999 || dict[key] > 999){
                max1 = 99999;
              }

              if(dict[key] >= 9999 || dict[key] < 99999){
                max1 = 999999;
              }
              if(dict[key] >= 99999){
                max1 = 9999999;
              }
            }}

            {if(key== "Adults Receiving Treatment"){
              if(dict[key] <= 999 || dict[key] >= 0){
                max1 = 9999;
              }

              if(dict[key] < 9999 || dict[key] > 999){
                max1 = 99999;
              }

              if(dict[key] >= 9999 || dict[key] < 99999){
                max1 = 999999;
              }
              if(dict[key] >= 99999){
                max1 = 9999999;
              }
            }}

            {if(key== "Children Needing Treatment"){
              if(dict[key] <= 999 || dict[key] >= 0){
                max1 = 9999;
              }

              if(dict[key] < 9999 || dict[key] > 999){
                max1 = 99999;
              }

              if(dict[key] >= 9999 || dict[key] < 99999){
                max1 = 999999;
              }
              if(dict[key] >= 99999){
                max1 = 9999999;
              }
            }}

            {if(key== "Children Receiving Treatment"){
              if(dict[key] <= 999 || dict[key] >= 0){
                max1 = 9999;
              }

              if(dict[key] < 9999 || dict[key] > 999){
                max1 = 99999;
              }

              if(dict[key] >= 9999 || dict[key] < 99999){
                max1 = 999999;
              }
              if(dict[key] >= 99999){
                max1 = 9999999;
              }
            }}

            {if(key== "Adult DALY"){
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 11000;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 110000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 1100000;
                }
                if(dict[key] >= 99999){
                  max1 = 11000000;
                }
            }}

            {if(key== "Child DALY"){
                //min1 = 0; 
                if(dict[key] <= 999 || dict[key] >= 0){
                  max1 = 3000;
                }

                if(dict[key] < 9999 || dict[key] > 999){
                  max1 = 30000;
                }

                if(dict[key] >= 9999 || dict[key] < 99999){
                  max1 = 300000;
                }
                if(dict[key] >= 99999){
                  max1 = 3000000;
                }
            }}

            {if(key=="First-line Regimen Adult Proportion" || key== "Second-line Regimen Adult Proportion" || key=="First-line Regimen Child Proportion"|| key=="Second-line Regimen Child Proportion"){
                max1 = 1
            }}

            /// Roundworm  , whipworm, hookworm

            {if(key== "DALYs for 5-14 year olds"){
              //min1 = 0; 
              if(dict[key] < 999 ){
                max1 = 10000;
              }

              if(dict[key] >= 999 ){
                max1 = 78000;
              }
              
             
            
            }}

            {if(key== "DALYs for 1-4 year olds"){
              //min1 = 0; 
              if(dict[key] <= 999 || dict[key] >= 0){
                max1 = 10000;
              }

              if(dict[key] < 9999 || dict[key] > 999){
                max1 = 23000;
              }

              if(dict[key] >= 9999 ){
                max1 = 120000;
              }
          
            }}

            /// Schist, oncho, LF

            {if(key== "DALY"){
              //min1 = 0; 
              if(dict[key] <= 999 || dict[key] >= 0){
                max1 = 4200;
              }

              if(dict[key] < 9999 || dict[key] > 999){
                max1 = 42000;
              }

              if(dict[key] >= 9999 ){
                max1 = 500000;
              }
          
            }}



              {if(key== "Original Impact Score"){
                  //min1 = 0;
                  key = null;

              }}


            //let x = "setValue".concat(i);
            //let y = x.concat(i);
              return <div className={classes.root}>
                <Form.Label> {key} </Form.Label>
                <ThemeProvider theme={muiTheme}>
                <Slider
                  /*PREVALENCE*/
                  /*value={values[0]}*/
                 aria-label="Always visible"
                  id="main-slider"
                  defaultValue={dict[key]}
                  size="small"
                // aria-labelledby="discrete-slider-custom"
                  getAriaValueText={valuetext}
                  valueLabelDisplay="auto"
                  //getAriaValueText={valuetext}
                 //value={dict[key]}
                //valueLabelFormat={value}
                  //ticks
                 // style={{ maxWidth: 600 }}
                  step={0.01}
                  min={min1}
                  max={max1}
               
                 tooltip={false}
                 handleTitle={dict[key]}
                 disabled={false}
                 color={'primary'}
                 
                 ValueLabelComponent={ValueLabelComponent}
                 valueLabelFormat={(value) => {
                   return (
                     <div style={{ textAlign: "center" }}>
                       {value}
                       
                     </div>
                   );
                 }}
                  //onChange={} // for example updating a state value
                  //onChangeCommitted={} // for example fetching new data

//                  marks={marks_arr[i]}
                  valueLabelDisplay="on"
                 // valueLabelDisplay="auto"
                  aria-labelledby="continuous-slider"
                   //onChange={handleChange}
                  
                  onChange={function updateValue(changeEvent, newValue){
                      console.log(changeEvent);
                      return setValue1({[key]: newValue})
                    }
                  }

                  onChangeCommitted={handleChange} 
                  
                />
                </ThemeProvider>
               
                
               </div>
            })
            }
            </Form.Group>
          </Form>

         

          <Button id="MuiButton-root-2"
            //to="/Slider"
            variant="outlined"
            color="primary"
            color="inherit"
            //onClick={this.handleSubmit}
            onClick={!isLoading ? handleClick : null}
          >
            {isLoading ? "Loading…" : "Forecast"}
          </Button>

        </div>
      {/* {/* </header> */}
    </div> 
  );
}

function mapStateToProps(state1) {
  return state1;
}

const mapDispatchToProps = dispatch => ({
  //onCreatePressed : text=>dispatch(createForecast(text)),
  //onCreatePressed : text=>dispatch(addForecastRequest(text)),
  dispatch
});

export default connect(mapStateToProps, mapDispatchToProps)(App)