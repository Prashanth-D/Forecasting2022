/* eslint-disable no-use-before-define */
import React, { Component } from "react";
import "./App.css";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import GridListTile from "@material-ui/core/GridListTile";
import GridListTileBar from "@material-ui/core/GridListTileBar";
import ListSubheader from "@material-ui/core/ListSubheader";

import Countries from "./Components/Countries";
import Diseases from "./Components/Diseases";
import Drugs from "./Components/Drugs";
import Company from "./Components/Company";
import Specification from "./Components/Specification";
import Year from "./Components/Year";

import {setData, setDictDataa} from './Components/actions';

import { connect } from 'react-redux';


class Mainmenu extends Component {
  constructor(props) {
    super(props);
    

    this.state = {
      selectedState : this.props.data,
      selectedYear: "",
      selectedCountry: "",
      selectedDisease: "",
      selectedDrugs: "",
      selectedCompany: "",
      selectedSpecification: "",
      dict_data1:{},
      dict_data:{},
    };

    this.state.dict_data["state"] =this.props.data;
  }

  updateSelectedYear(selectedYear) {
    this.setState(
      {
        selectedYear: selectedYear,
        selectedCompany: "hello",
        selectedCountry: "",
        selectedDisease: "",
        selectedDrugs: "",
        selectedSpecification: "",
        dict_data1:{},
      },
      function () {
        console.log("selectedYear", this.state.selectedYear);
        this.state.dict_data["Year"] = this.state.selectedYear;
      }
    );
  }

  updateSelectedCompany(selectedCompany) {
    this.setState(
      {
        selectedCompany: selectedCompany,
        selectedCountry: "",
        selectedDisease: "",
        selectedDrugs: "",
        selectedSpecification: "",
        dict_data1:{},
      },
      function () {
        console.log("selectedCompanyParent", this.state.selectedCompany);
        this.state.dict_data["Company"] = this.state.selectedCompany;

      }
    );
  }


  updateSelectedCountry(selectedCountry) {
    this.setState(
      {
        selectedCountry: selectedCountry,
        selectedDisease: "",
        selectedDrugs: "",
        selectedSpecification: "",
        dict_data1:{},
      },
      function () {
        console.log("selectedCountryParent", this.state.selectedCountry);
        this.state.dict_data["Country"] = this.state.selectedCountry;
      }
    );
  }

  updateSelectedDisease(selectedDisease) {
    this.setState(
      {
        selectedDisease: selectedDisease,
        selectedDrugs: "",
        selectedSpecification: "",
        dict_data1:{},
      },
      function () {
        console.log("selectedDiseaseParent", this.state.selectedDisease);
        this.state.dict_data["Disease"] = this.state.selectedDisease;
      }
    );
  }
  updateSelectedDrugs(selectedDrugs) {
    this.setState(
      {
        selectedDrugs: selectedDrugs,
        selectedSpecification: "",
        dict_data1:{},
      },
      function () {
        console.log("selectedDrugParent", this.state.selectedDrugs);
        this.state.dict_data["Drug"] = this.state.selectedDrugs;
      }
    );
  }

  

  updateSelectedSpecification(selectedSpecification) {
    this.setState(
      {
        selectedSpecification: selectedSpecification,
        dict_data1:{},
      },
      function () {
        console.log("selectedSpecificationParent", this.state.selectedSpecification);
        this.state.dict_data["Specification"] = this.state.selectedSpecification;
        console.log(this.state.dict_data);
      }
    );
  }

  updateSelectedWhole() {
    this.setState(
      {
        //selectedSpecification: selectedSpecification,
        dict_data1:this.state.dict_data,
      },
      function () {
        console.log("selectedSpecificationParent", this.state.selectedSpecification);
        //dict_data["Specification"] = this.state.selectedSpecification;
        this.props.dispatch(setDictDataa(this.state.dict_data1))
        console.log(this.state.dict_data1);
      }
    );
  }

  render() {
    console.log(this.props.data)
    return (
      
      //outlined
      <div id="wrap1">
        <br/> <br/> <br/>
        <br/>
        <br/>
        {/* <Button variant={this.props.button1_variation}
                color={this.props.button1_color}
                onClick={this.updateSelectedYear("2010")} data={this.props.data}
        >
          2010
        </Button>
        <Button variant={this.props.button2_variation} 
                color={this.props.button2_color}
                onClick={this.updateSelectedYear("2013")} data={this.props.data}
        >
          2013
        </Button>
        
        <Button varient ={this.props.button3_variation} 
                color={this.props.button3_color}
                onClick={this.updateSelectedYear("2015")} data={this.props.data}
        >
          2015
        </Button> */}

        <Year
          fUpdate={this.updateSelectedYear.bind(this)} data={this.props.data} 
        />
        <Company
          selectedYear={this.state.selectedYear}
          fUpdate={this.updateSelectedCompany.bind(this)} data={this.props.data}
        />
        <Countries 
          selectedYear={this.state.selectedYear}
          selectedCompany={this.state.selectedCompany}
          fUpdate={this.updateSelectedCountry.bind(this)}  data={this.props.data}/>
        <Diseases
          selectedYear={this.state.selectedYear}
          selectedCompany={this.state.selectedCompany}
          selectedCountry={this.state.selectedCountry}
          fUpdate={this.updateSelectedDisease.bind(this)} data={this.props.data}
        />
        <Drugs
          selectedYear={this.state.selectedYear}
          selectedCompany={this.state.selectedCompany}
          selectedCountry={this.state.selectedCountry}
          selectedDisease={this.state.selectedDisease}
          fUpdate={this.updateSelectedDrugs.bind(this)} data={this.props.data}
        />
        
        <Specification
          selectedYear={this.state.selectedYear}
          selectedCompany={this.state.selectedCompany}
          selectedCountry={this.state.selectedCountry}
          selectedDisease={this.state.selectedDisease}
          selectedDrugs={this.state.selectedDrugs}
          selectedState = {this.props.data}
          dict_dataa={this.state.dict_data}
          fUpdate={this.updateSelectedSpecification.bind(this)} data={this.props.data}
          fUpdate={this.updateSelectedWhole.bind(this)} data={this.props.data}
        />
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

export default connect(mapStateToProps, mapDispatchToProps)(Mainmenu);
