import React, { Component } from "react";
import { useState, useEffect } from "react";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import axios from "axios";
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import ListItemText from "@material-ui/core/ListItemText";
import Select from "@material-ui/core/Select";
import Button from "@material-ui/core/Button";
import { withRouter } from 'react-router';
import App from "../App.js";

import { useHistory, Redirect } from "react-router-dom";
import { connect } from 'react-redux';
import {setData, setDictDataa} from './actions';


import {
  CheckBoxSelection,
  Inject,
  MultiSelectComponent,
} from "@syncfusion/ej2-react-dropdowns";

// function simulateNetworkRequest() {
//   return new Promise((resolve) => setTimeout(resolve, 2000));
// }

// const [isLoading, setLoading] = useState(false);

// useEffect(() => {
//   if (isLoading) {
//     simulateNetworkRequest().then(() => {
//       setLoading(false);
//     });
//   }
// }, [isLoading]);

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
    maxWidth: 300,
  },
  chips: {
    display: "flex",
    flexWrap: "wrap",
  },
  chip: {
    margin: 2,
  },
  noLabel: {
    marginTop: theme.spacing(3),
  },
}));

class Specification extends Component {
//  sportsData = ["Badminton", "Cricket", "Football", "Golf", "Tennis"];
  //selected_specification = []
  constructor(props) {
    super(props);
    this.handleSubmit=this.handleSubmit.bind(this);    
    this.state = {
      SpecificationName: [],
      selectedSpecification: [],
    };
    //Nutan added this
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleClick(o) {
    console.log("HANDLE CLICK EVENT")
    console.log(o.target.value)
    const { options } = o.target;

    let selected_specification= o.target.value;
    //options = o.target;

    console.log("options"+options);
    console.log("selected_specification"+selected_specification);

    const value = [];

        if (selected_specification === "Select a Specification") {
      selected_specification = [];
     

    }
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    console.log("values"+value);

    this.setState(
      { selectedSpecification: value },
      function () {
        this.props.fUpdate(this.state.selectedSpecification);
      }
    );
    console.log("selected_specification=" + selected_specification);
    console.log(
      "this.state.selectedSpecification=" + this.state.selectedSpecification
    );
  }

  handleChange = (e) =>{
    console.log("HANDLE CHANGE EVENT")
    console.log(e.target.value)
    let selected_specification = e.target.value
    const { options } = e.target;
    //options.push(e.target.value);
    //console.log("options"+options);
    console.log("selected_specification"+selected_specification);

    const value = [];

        if (selected_specification === "Select a Specification") {
      selected_specification = [];
     

    }
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        //console.log("options"+options);
        value.push(options[i].value);
      }
    }
    console.log("values"+value);

    
    //setPersonName(value);
    //selected_specification(value);

    this.setState(
      { selectedSpecification: value },
      //{selectedSpecification: [...this.state.selected_specification , selected_specification]},
      function () {
        this.props.fUpdate(this.state.selectedSpecification);
        //this.props.history.push("/Slider");
      }
    );
    }

  handleSubmit = (e) =>{
    e.preventDefault();
    //const history = useHistory();

    let selected_specification = this.state.selectedSpecification;
    if (selected_specification === "Select a Specification") {
      selected_specification = [];
    }
    this.setState(
      { selectedSpecification: selected_specification },
      function () {
        this.props.fUpdate(this.state.selectedSpecification);
        //this.props.history.push("/Slider");
      }
    );

    if (this.props.selectedDisease === "TB") {
      console.log(this.props.dict_dataa);
      axios
        .post(
          "/get_spec_tb",
          {
          
            dict_dataa: this.props.dict_data1,
            selected_country: this.props.selectedCountry,
            selected_disease: this.props.selectedDisease,
            selected_drug: this.props.selectedDrugs,
            selected_company: this.props.selectedCompany,
            selected_specification: selected_specification,
            selected_year: this.props.selectedYear,
          },
          { headers: { "content-type": "application/json" } }
        )
        .then((res) => {
          const SpecificationName = Array.from(res.data);
          console.log(res.data);
          this.props.dispatch(setData(res.data))
          //this.props.dispatch(setDictDataa(this.props.dict_dataa))
          console.log(this.props.data1)
          
          this.props.history.push({pathname: '/slider', data: {data:this.props.data1, state: this.props.data, dict_dataa: this.props.dict_dataa1}});

          alert(res.data);
        });
    } else if (this.props.selectedDisease === "Malaria") {
      axios
        .post(
          "/get_spec_malaria",
          {
            dict_dataa: this.props.dict_data1,
            selected_country: this.props.selectedCountry,
            selected_disease: this.props.selectedDisease,
            selected_drug: this.props.selectedDrugs,
            selected_company: this.props.selectedCompany,
            selected_specification: selected_specification,
            selected_year: this.props.selectedYear,
          },
          { headers: { "content-type": "application/json" } }
        )
        .then((res) => {
          const SpecificationName = Array.from(res.data);
          console.log(res.data);
          this.props.dispatch(setData(res.data))
          //this.props.dispatch(setDictDataa(this.props.dict_dataa))
          this.props.history.push({pathname: '/slider', data: {data:this.props.data1, state: this.props.selectedState, dict_dataa: this.props.dict_dataa}});

          alert(res.data);
        });
    }
      else if(this.props.selectedDisease === 'HIV') {
        axios.post('/get_spec_hiv', 
        {
          dict_dataa: this.props.dict_data1,
          selected_country: this.props.selectedCountry,
          selected_disease: this.props.selectedDisease,
          selected_drug: this.props.selectedDrugs,
          selected_company: this.props.selectedCompany,
          selected_specification: selected_specification,
          selected_year: this.props.selectedYear,
        }, 
          {headers: {'content-type': 'application/json'}}
          )
          .then((res) => {
            const SpecificationName = Array.from(res.data);
            console.log(res.data);
            this.props.dispatch(setData(res.data))
            //this.props.dispatch(setDictDataa(this.props.dict_dataa))
            this.props.history.push({pathname: '/slider', data: {data:this.props.data1, state: this.props.selectedState, dict_dataa: this.props.dict_dataa}});
            
            alert(res.data);
          });
      }
    // worms
    else if (
      this.props.selectedDisease === "Roundworm" ||
      this.props.selectedDisease === "Hookworm" ||
      this.props.selectedDisease === "Whipworm"
    ) {
      axios
        .post(
          "/get_spec_worms",
          {
            dict_dataa: this.props.dict_data1,
            selected_country: this.props.selectedCountry,
            selected_disease: this.props.selectedDisease,
            selected_drug: this.props.selectedDrugs,
            selected_company: this.props.selectedCompany,
            selected_specification: selected_specification,
            selected_year: this.props.selectedYear,
          },
          { headers: { "content-type": "application/json" } }
        )
        .then((res) => {
          const SpecificationName = Array.from(res.data);
          console.log(res.data);
          this.props.dispatch(setData(res.data))
          //this.props.dispatch(setDictDataa(this.props.dict_dataa))
          this.props.history.push({pathname: '/slider', data: {data:this.props.data1, state: this.props.selectedState, dict_dataa: this.props.dict_dataa}});
          alert(res.data);
        });
    }

    // other
    else if (
      this.props.selectedDisease === "Schistosomiasis" ||
      this.props.selectedDisease === "Onchoceriasis" ||
      this.props.selectedDisease === "LF"
    ) {
      alert(this.state.selected_specification);
      axios
        .post(
          "/get_spec_other",
          {
            dict_dataa: this.props.dict_data1,
            selected_country: this.props.selectedCountry,
            selected_disease: this.props.selectedDisease,
            selected_drug: this.props.selectedDrugs,
            selected_specification: selected_specification,
            selected_year: this.props.selectedYear,
          },
          { headers: { "content-type": "application/json" } }
        )
        .then((res) => {
          const SpecificationName = Array.from(res.data);
          console.log(res.data);
          this.props.dispatch(setData(res.data))
          //this.props.dispatch(setDictDataa(this.props.dict_dataa))
          this.props.history.push({pathname: '/slider', data: {data:this.props.data1, state: this.props.selectedState, dict_dataa: this.props.dict_dataa}});

          alert(res.data);
        });
    }


  }

  componentDidUpdate(prevProps) {
  console.log(prevProps);
  console.log(this.props);
  if ((prevProps.selectedCompany !== this.props.selectedCompany && prevProps.selectedState === "Country") || 
  (prevProps.selectedDrugs !== this.props.selectedDrugs && prevProps.selectedState === "Company") || 
  (prevProps.selectedCompany !== this.props.selectedCompany && prevProps.selectedState === "Disease") ||
  (prevProps.selectedCompany !== this.props.selectedCompany && prevProps.selectedState === "Drug")) 
   {
      axios
        .post(
          "/get_specification",
          {
            selected_disease: this.props.selectedDisease,
            selected_drug: this.props.selectedDrugs,
            selected_year : this.props.selectedYear,
            selected_country: this.props.selectedCountry
          },
          { headers: { "content-type": "application/json" } }
        )
        .then((res) => {
          const SpecificationName = Array.from(res.data);
          console.log(res.data);
          this.setState({ SpecificationName });
        });
    }
  }


  render(data) {
    console.log(this.props.data);

    

    //let classes = useStyles();
    let isDisabled = !this.props.selectedCompany;
    let isDisabledSpec = !this.state.selectedSpecification;
    return (
      <div>
        <div>
          <FormControl style={{minWidth: 300}}>
            <InputLabel shrink htmlFor="select-multiple-native">
              Specifications
            </InputLabel>
            <Select
              multiple
              native
              //value={personName}
              //onClick={this.handleClick.bind(this)}
              onChange={this.handleChange.bind(this)}
              inputProps={{
                id: "select-multiple-native",
              }}
            >
              {this.state.SpecificationName.map((SpecificationName) => (
                <option key={SpecificationName} value={SpecificationName}>
                  {SpecificationName}
                </option>
              ))}
            </Select>
          </FormControl>
          {/* <div>
          <select
            multiple
            disabled={isDisabled}
            name="Specifications"
            id="Specifications"
            onChange={this.handleClick.bind(this)}
          >
            <option>Select a Specification</option>
            {this.state.SpecificationName.map((SpecificationName) => (
              <option>{SpecificationName}</option>
            ))}
          </select>
        </div> */}
        </div>
        <p>
         <div id="container"> 
        <Button id="button1"
            //to="/Slider"
            variant="outlined"
            
            color="primary"
            color="inherit"
            disabled={isDisabledSpec}
            //onClick={this.handleSubmit}
            //onClick={!isLoading ? this.handleSubmit.bind(this) : null}
            onClick={this.handleSubmit.bind(this)}
          >
            {/* {isLoading ? "Loading…" : "Forecast"} */}
            Forecast
          </Button>
      
        <Button id="button2" 
          variant="outlined"
          color="primary"
          color="inherit"
          disabled={isDisabledSpec}>            
            Reset
          </Button>
          </div>
          </p>  
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

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Specification));
