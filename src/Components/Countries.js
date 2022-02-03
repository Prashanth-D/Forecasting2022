import React, { Component, useEffect } from "react";
import axios from "axios";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

import {connect} from 'react-redux';
import { ReactReduxContext } from "react-redux";
// import { removeForecast, markForecastAsCompleted} from "./actions";
import {displayAlert} from './thunks';
import { ContactPhoneTwoTone } from "@material-ui/icons";

import {getForecasts, getForecastsLoading} from './selectors';

import {loadForecasts} from './thunks';

const top100Films = [
  { title: "India", year: 1994 },
  { title: "Afganisthan", year: 1972 },
  { title: "Pakistan", year: 1974 },
  { title: "Sudan", year: 2008 },
  { title: "Albania", year: 1957 },
  { title: "Algeria", year: 1993 },
];

//const flatProps = {
//  options: this.state.countryName.map((countryName) => countryName.title),
//};

class Countries extends Component {
  constructor(props) {
    super(props);
    this.state = {
      countryName: [],
      selectedYear: "",
      selectedCountry: "",
    };

    this.defaultProps = {
      options: top100Films,

      getOptionLabel: (option) => option.title,
    };
    console.log(this.props.data)
    //const cntry_state = this.props.data;

  }


  handleClick(o) {
    //let selected_country = o.target.value;
    let selected_country;
    if(o === null){
      selected_country = '';
    }
    else{
      selected_country = o.trim();
    }
    //console.log(o.target);
    //console.log(o);
    if (selected_country === "Select a Country") {
      selected_country = "";
    }
    this.setState({ selectedCountry: selected_country }, function () {
      this.props.fUpdate(this.state.selectedCountry);
    });
  }

//
//  componentDidMount() {
//    console.log ("In Country Mount")
//    console.log(this.props.data);
//     console.log(this.prevProps.data);
//    if (prevProps.selectedYear !== this.props.selectedYear && this.props.data === "Country"){
//        axios.post("/country", {selected_year: this.props.selectedYear},{headers: {'content-type': 'application/json'}}).then((res) => {
//          const countryName = Array.from(res.data);
//          this.setState({ countryName });
//          console.log(res.data);
//        });
//    }
//  }


// Country -> Disease -> Drug -> Company
// Drug -> Country -> Disease -> Company
// Disease -> Country -> Drug -> Company
// Company -> Country -> Disease -> Drug

  componentDidUpdate(prevProps) {
    console.log ("In Country Update")
    console.log(this.prevProps)
    console.log(this.props)

    if (prevProps.selectedYear !== this.props.selectedYear && this.props.data === "Country") {
       console.log("Sending request from componentDidUpdate")
    // axios.post('/get_country_by_disease', {selected_disease: this.props.selectedDisease}, {headers: {'content-type': 'application/json'}}).then((res) => {
       axios.post('/country', {selected_year: this.props.selectedYear}, {headers: {'content-type': 'application/json'}}).then((res) => {
        const countryName = Array.from(res.data);
       console.log(res.data);
       this.setState({countryName});
       })
     }

     if (prevProps.selectedDisease !== this.props.selectedDisease && this.props.data === "Disease") {
    //       axios.post('/get_country_by_disease', {selected_disease: this.props.selectedDisease}, {headers: {'content-type': 'application/json'}}).then((res) => {
       axios.post('/country', {selected_year: this.props.selectedYear, selected_disease: this.props.selectedDisease}, {headers: {'content-type': 'application/json'}}).then((res) => {
       const countryName = Array.from(res.data);
       console.log(res.data);
       this.setState({countryName});
       })
     }

    if (prevProps.selectedCompany !== this.props.selectedCompany && this.props.data === "Company") {
        axios.post('/get_country_by_cmpny', {selected_year: this.props.selectedYear,selected_company: this.props.selectedCompany}, {headers: {'content-type': 'application/json'}}).then((res) => {
        const countryName = Array.from(res.data);
        console.log(res.data);
        this.setState({countryName});
    })
    }
    if (prevProps.selectedDrugs !== this.props.selectedDrugs && this.props.data === "Drug") {
      axios.post('/get_country_by_drug', {selected_year: this.props.selectedYear, selected_drug: this.props.selectedDrugs}, {headers: {'content-type': 'application/json'}}).then((res) => {
      const countryName = Array.from(res.data);
      console.log(res.data);
      this.setState({countryName});
    })
    }
  }

  render(data) {
    let isDisabled
    console.log(this.props.data)

    if(this.props.data === "Country"){
      isDisabled = !this.props.selectedYear
    }
    else if(this.props.data === "Company"){
      isDisabled = !this.props.selectedCompany;
    }
    else if(this.props.data === "Disease"){
      isDisabled = !this.props.selectedDisease;
    }
    else if(this.props.data === "Drug"){
      isDisabled = !this.props.selectedDrugs;
    }
    else{
      console.log("Error 404")
    }



    {
      this.state.countryName.map((countryName) => {
        //console.log(countryName);

        return countryName;
      });
    }

    const ForecastList = ({
      forecasts = [], 
      onRemovePressed, 
      onCompletedPressed, 
      onDisplayAlertClicked, 
      isLoading, 
      startLoadingForecasts, }) => ({
    }
    );

   // useEffect(()=>{
   //   startLoadingForecasts();
   // },[])

    const loadingMessage = <div>Loading forecast...</div>;

    return (
      

      <div>
        <Autocomplete
          //fUpdate={this.updateSelectedCountry.bind(this)}
          disabled={isDisabled}
          name="Countries"
          id="Countries"
          //onChange={this.handleClick.bind(this)}
          onChange={(event, value) => this.handleClick(value)}
          options={this.state.countryName}
          getOptionLabel={(name) => name}
          renderInput={(countryName) => (
            <TextField
              {...countryName}
              label="Select a Country"
              margin="normal"
            />
          )}
          
        />

        {/* <Autocomplete
          id="combo-box-demo"
          options={this.state.countryName}
          getOptionLabel={(name) => name}
          style={{ width: 300 }}
          renderInput={(params) => (
            <TextField {...params} label="Combo box" variant="outlined" />
          )}
        /> */}

        {/* <select
          name="Countries"
          id="Countries"
          onChange={this.handleClick.bind(this)}
        >
          <option>Select a Country</option>
          {this.state.countryName.map((countryName) => (
            <option>{countryName}</option>
          ))}
        </select> */}
      </div>
    );

    //return isLoading ? loadingMessage : content;
  }
}

function mapStateToProps(state1) {
  return state1;
}


const mapDispatchToProps = dispatch => (
  {
    // onRemovePrssed: text => dispatch(removeForecast(text)),
    // onCompletedPressed: text=> dispatch(markForecastAsCompleted(text)),
    // onDisplayAlertClicked: () => dispatch(displayAlert()),
    dispatch
  }
);



export default connect(mapStateToProps, mapDispatchToProps)(Countries);
