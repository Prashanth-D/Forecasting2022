import React, { Component } from "react";
import axios from "axios";

import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

class Drugs extends Component {
  constructor(props) {
    super(props);
    this.state = {
      DrugName: [],
      selectedCountry: "",
      selectedDisease: "",
      selectedDrugs: "",
    };

    //const state1 = this.props.data;

  }

  handleClick(o) {
    let selected_drug = o;
    console.log(o);
    if (selected_drug === "Select a Drug") {
      selected_drug = "";
    }
    this.setState({ selectedDrugs: selected_drug }, function () {
      this.props.fUpdate(this.state.selectedDrugs);
    });
  }
  // componentDidUpdate(prevProps) {
  //   if (prevProps.selectedDisease !== this.props.selectedDisease) {
  //     axios
  //       .post(
  //         "/get_drug",
  //         {
  //           selected_disease: this.props.selectedDisease,
  //           selected_country: this.props.selectedCountry,
  //         },
  //         { headers: { "content-type": "application/json" } }
  //       )
  //       .then((res) => {
  //         const DrugName = Array.from(res.data);
  //         console.log(res.data);
  //         this.setState({ DrugName });
  //       });
  //   }
  // }

  /*

  componentDidMount(){
    if (this.props.data === "Drug"){
    axios.get('/drug').then((res) => {
      const DrugName = res.data;
      this.setState({ DrugName});
    })
    }
  }
  */

  // Country -> Disease -> Drug -> Company
// Drug -> Country -> Disease -> Company
// Disease -> Country -> Drug -> Company
// Company -> Country -> Disease -> Drug

  componentDidUpdate(prevProps) {
    
    if(prevProps.selectedYear !== this.props.selectedYear && this.props.data === "Drug"){
      axios
      .post(
        '/drug',
        {selected_year : this.props.selectedYear},
        {headers: {'content-type': 'application/json'}}
      )
      .then((res) => {
        const DrugName = res.data;
        this.setState({ DrugName});
      })
    }

    if (prevProps.selectedDisease !== this.props.selectedDisease && this.props.data === 'Country') {
        axios
        .post(
          '/get_drug', 
          {
            selected_disease: this.props.selectedDisease, 
            selected_country: this.props.selectedCountry, 
            selected_company: this.props.selectedCompany, 
            selected_year: this.props.selectedYear
          }, 
          {headers: {'content-type': 'application/json'}}
        )
        .then((res) => {
          const DrugName = Array.from(res.data);
          console.log(res.data);
          this.setState({DrugName});
        })
  }

  if (prevProps.selectedDisease !== this.props.selectedDisease && this.props.data === 'Company') {
    axios
      .post('/get_drug_by_cmpny', {
        selected_disease: this.props.selectedDisease, 
        selected_country: this.props.selectedCountry, 
        selected_company: this.props.selectedCompany,
        selected_year: this.props.selectedYear,
      }, 
      {headers: {'content-type': 'application/json'}}
      )
      .then((res) => {
        const DrugName = Array.from(res.data);
        console.log(res.data);
        this.setState({DrugName});
    })
}

 if (prevProps.selectedCountry !== this.props.selectedCountry && this.props.data === 'Disease') {
   axios
    .post('/get_drug', {
      selected_disease: this.props.selectedDisease, 
      selected_country: this.props.selectedCountry, 
      selected_company: this.props.selectedCompany,
      selected_year: this.props.selectedYear,
    }, 
    {headers: {'content-type': 'application/json'}}
    )
    .then((res) => {
    const DrugName = Array.from(res.data);
    console.log(res.data);
    this.setState({DrugName});
    })
 }

  }

  render() {
    let isDisabled
    console.log(this.props.data)
    if(this.props.data === "Country"){
      isDisabled = !this.props.selectedDisease;
    }
    else if(this.props.data === "Company"){
      isDisabled = !this.props.selectedDisease;
    }
    else if(this.props.data === "Disease"){
      isDisabled = !this.props.selectedCountry;
    }
    else if(this.props.data === "Drug"){
      isDisabled = !this.props.selectedYear


    }
    else{
      console.log("Error 404")
    }


    this.state.DrugName.map((DrugName) => {
      console.log(DrugName);

      return DrugName;
    });

    
    return (
      <div>
        <Autocomplete
          //fUpdate={this.updateSelectedCountry.bind(this)}
          disabled={isDisabled}
          name="Drugs"
          id="Drugs"
          //onChange={this.handleClick.bind(this)}
          onChange={(event, value) => this.handleClick(value)}
          options={this.state.DrugName}
          getOptionLabel={(name) => name}
          renderInput={(DrugName) => (
            <TextField {...DrugName} label="Select a Drug" margin="normal" />
          )}
        />

        {/* <select
          disabled={isDisabled}
          name="Drugs"
          id="Drugs"
          onChange={this.handleClick.bind(this)}
        >
          <option>Select a Drug</option>
          {this.state.DrugName.map((DrugName) => (
            <option>{DrugName}</option>
          ))}
        </select> */}
      </div>
    );
  }
}

export default Drugs;
