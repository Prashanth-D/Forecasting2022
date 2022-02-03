import React, { Component } from "react";
import axios from "axios";

import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

class Diseases extends Component {
  constructor(props) {
    super(props);
    this.state = {
      DiseaseName: [],
      selectedYear: "",
      selectedCountry: "",
      selectedDisease: "",
    };
    //const state1 = this.props.data;

  }

  handleClick(o) {
    //let selected_disease = o.target.value;
    let selected_disease = o;
    if (selected_disease === "Select a Disease") {
      selected_disease = "";
    }
    this.setState({ selectedDisease: selected_disease }, function () {
      this.props.fUpdate(this.state.selectedDisease);
    });
  }

  // componentDidUpdate(prevProps) {
  //   if (prevProps.selectedCountry !== this.props.selectedCountry) {
  //     this.setState({ selectedCountry: this.props.selectedCountry });
  //     axios
  //       .post(
  //         "/get_disease",
  //         { selected_country: this.props.selectedCountry },
  //         { headers: { "content-type": "application/json" } }
  //       )
  //       .then((res) => {
  //         const DiseaseName = Array.from(res.data);
  //         console.log(res.data);
  //         this.setState({ DiseaseName });
  //       });
  //   }
  // }

/*
  componentDidMount(){
    console.log(this.props.data)
    if (this.props.data === "Disease"){
     axios.get('/get_disease').then((res) => {
       const DiseaseName = res.data;
       this.setState({ DiseaseName});
     })
    }
  }*/

  // Country -> Disease -> Drug -> Company
// Drug -> Country -> Disease -> Company
// Disease -> Country -> Drug -> Company
// Company -> Country -> Disease -> Drug

  componentDidUpdate(prevProps) {
    if(prevProps.selectedYear !== this.props.selectedYear && this.props.data === 'Disease'){
      axios
        .post(
        '/get_disease', 
        {selected_year: this.props.selectedYear}, 
        {headers: {'content-type': 'application/json'}}
        )
        .then((res) => {
          const DiseaseName = res.data;
          this.setState({DiseaseName});
        })
    }


    if (prevProps.selectedCountry !== this.props.selectedCountry && this.props.data === 'Country') {
      console.log("Selected Year in Diseases:" +  this.props.selectedYear);
      axios.post('/get_disease', {selected_country: this.props.selectedCountry, selected_company: this.props.selectedCompany, selected_year : this.props.selectedYear,}, {headers: {'content-type': 'application/json'}}).then((res) => {
      const DiseaseName = Array.from(res.data);
      console.log(res.data);
      this.setState({DiseaseName});
  })
}

    if (prevProps.selectedCountry !== this.props.selectedCountry && this.props.data === 'Company') {
        axios.post('/get_disease_by_cmpny', { selected_year : this.props.selectedYear, selected_country: this.props.selectedCountry, selected_company: this.props.selectedCompany}, {headers: {'content-type': 'application/json'}}).then((res) => {
        const DiseaseName = Array.from(res.data);
        console.log(res.data);
        this.setState({DiseaseName});
    })
  }
  if (prevProps.selectedCountry !== this.props.selectedCountry && this.props.data === 'Drug') {
          axios.post('/get_disease_by_drug', { selected_year : this.props.selectedYear, selected_drug: this.props.selectedDrugs, selected_country: this.props.selectedCountry}, {headers: {'content-type': 'application/json'}}).then((res) => {
          const DiseaseName = Array.from(res.data);
          console.log(res.data);
          this.setState({DiseaseName});
      })
  }
}

  render() {
    let isDisabled
    console.log(this.props.data)
    if(this.props.data === "Country"){
      isDisabled = !this.props.selectedCountry;
    }
    else if(this.props.data === "Company"){
      isDisabled = !this.props.selectedCountry;
    }
    else if(this.props.data === "Disease"){
      isDisabled = !this.props.selectedYear

    }
    else if(this.props.data === "Drug"){
      isDisabled = !this.props.selectedCountry;
    }
    else{
      console.log("Error 404")
    }


    
    return (
      <div>
        <Autocomplete
          //fUpdate={this.updateSelectedCountry.bind(this)}
          disabled={isDisabled}
          name="Diseases"
          id="Diseases"
          //onChange={this.handleClick.bind(this)}
          onChange={(event, value) => this.handleClick(value)}
          options={this.state.DiseaseName}
          getOptionLabel={(name) => name}
          renderInput={(DiseaseName) => (
            <TextField
              {...DiseaseName}
              label="Select a Disease"
              margin="normal"
            />
          )}
        />

        {/* <select
          disabled={isDisabled}
          name="Diseases"
          id="Diseases"
          onChange={this.handleClick.bind(this)}
        >
          <option>Select a Disease</option>
          {this.state.DiseaseName.map((DiseaseName) => (
            <option>{DiseaseName}</option>
          ))}
        </select> */}
      </div>
    );
  }
}

export default Diseases;
