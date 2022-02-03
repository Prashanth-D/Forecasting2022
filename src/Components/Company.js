import React, { Component } from "react";
import axios from "axios";

import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

class Company extends Component {
  constructor(props) {
    super(props);
    this.state = {
      CompanyName: [],
      selectedYear: "",
      selectedCountry: "",
      selectedDisease: "",
      selectedDrugs: "",
      selectedCompany: "",
    };

    //const state1 = this.props.data;

  }

  handleClick(o) {
    let selected_company = o;
    if (selected_company === "Select a Company") {
      selected_company = "";
    }
    this.setState({ selectedCompany: selected_company }, function () {
      this.props.fUpdate(this.state.selectedCompany);
    });
  }

  /*
  componentDidMount(){
  console.log ("In Company Mount")
  if (this.props.data === "Company"){
       axios.get('/company').then((res) => {
         const CompanyName = res.data;
         this.setState({ CompanyName});
         console.log(res.data);
       })

  }
 }

 */

 // Country -> Disease -> Drug -> Company
// Drug -> Country -> Disease -> Company
// Disease -> Country -> Drug -> Company
// Company -> Country -> Disease -> Drug

   componentDidUpdate(prevProps) {
   console.log ("In Company Update")
   console.log(prevProps)

//    if (prevProps.selectedDrugs !== this.props.selectedDrugs && this.props.data === 'Disease') {
//     axios
//       .post(
//         "/get_company",
//         {
//           selected_country: this.props.selectedCountry,
//           selected_disease: this.props.selectedDisease,
//           selected_drug: this.props.selectedDrugs,
//         },
//         { headers: { "content-type": "application/json" } }
//       )
//       .then((res) => {
//         const CompanyName = Array.from(res.data);
//         console.log(res.data);
//         this.setState({ CompanyName });
//       });
//   }

    if(prevProps.selectedYear !== this.props.selectedYear && this.props.data === 'Company'){
      axios
      .post
      (
        '/company',
        {selected_year : this.props.selectedYear},
        { headers: { "content-type": "application/json" } }
      )
      .then((res) => {
        const CompanyName = res.data;
        this.setState({ CompanyName});
        console.log(res.data);
      })
    }

     if ((prevProps.selectedDrugs !== this.props.selectedDrugs && this.props.data === 'Disease') ||
         (prevProps.selectedDrugs !== this.props.selectedDrugs && this.props.data === 'Country')) {
       axios
         .post(
           "/get_company",
           {
             selected_country: this.props.selectedCountry,
             selected_disease: this.props.selectedDisease,
             selected_drug: this.props.selectedDrugs,
             selected_year: this.props.selectedYear,
           },
           { headers: { "content-type": "application/json" } }
         )
         .then((res) => {
           const CompanyName = Array.from(res.data);
           console.log(res.data);
           this.setState({ CompanyName });
         });
     }

     if (prevProps.selectedDisease !== this.props.selectedDisease && this.props.data === 'Drug') {
      axios
        .post(
          "/get_company_by_drug",
          {
            selected_country: this.props.selectedCountry,
            selected_disease: this.props.selectedDisease,
            selected_drug: this.props.selectedDrugs,
            selected_year : this.props.selectedYear,
          },
          { headers: { "content-type": "application/json" } }
        )
        .then((res) => {
          const CompanyName = Array.from(res.data);
          console.log(res.data);
          this.setState({ CompanyName });
        });
    }

   }

 

  render() {
    let isDisabled
    console.log(this.props.data)
    if(this.props.data === "Country"){
      isDisabled = !this.props.selectedDrugs;
    }
    else if(this.props.data === "Company"){
      isDisabled = !this.props.selectedYear
    }
    else if(this.props.data === "Disease"){
      isDisabled = !this.props.selectedDrugs;
    }
    else if(this.props.data === "Drug"){
      isDisabled = !this.props.selectedDisease;
    }
    else{
      console.log("Error 404")
    }



    //let isDisabled = !this.props.selectedDrugs;
    return (
      <div>
        <Autocomplete
          //fUpdate={this.updateSelectedCountry.bind(this)}
          disabled={isDisabled}
          name="Companies"
          id="Companies"
          //onChange={this.handleClick.bind(this)}
          onChange={(event, value) => this.handleClick(value)}
          options={this.state.CompanyName}
          getOptionLabel={(name) => name}
          renderInput={(CompanyName) => (
            <TextField
              {...CompanyName}
              label="Select a Company"
              margin="normal"
            />
          )}
        />

        {/* <select
          disabled={isDisabled}
          name="Companies"
          id="Companies"
          onChange={this.handleClick.bind(this)}
        >
          <option>Select a Company</option>
          {this.state.CompanyName.map((CompanyName) => (
            <option>{CompanyName}</option>
          ))}
        </select> */}
      </div>
    );
  }
}
export default Company;
