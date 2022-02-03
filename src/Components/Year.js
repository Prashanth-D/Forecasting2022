import React, { Component } from "react";
import axios from "axios";

import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

const availableYears = [
    "2010",
    "2013",
    "2015",
  ];
  
class Year extends Component {
  constructor(props) {
    super(props);
    this.state = {
      SelectedYear: "",
      selectedCountry: "",
      selectedDisease: "",
      selectedDrugs: "",
      selectedCompany: "",
    };

    //const state1 = this.props.data;
    this.defaultProps = {
        options: availableYears,
  
        getOptionLabel: (option) => option,
      };  

  }

  handleClick(o) {
   
    let selected_year = o;
    console.log(selected_year);
    if (selected_year === "Select a Year") {
      selected_year = "";
    }
    this.setState({ selectedYear: selected_year }, function () {
      this.props.fUpdate(this.state.selectedYear);
    });
  }

//   componentDidMount(){
//   console.log ("In Company Mount")
//   if (this.props.data === "Company"){
//        axios.get('/company').then((res) => {
//          const CompanyName = res.data;
//          this.setState({ CompanyName});
//          console.log(res.data);
//        })

//   }
//  }

 // Country -> Disease -> Drug -> Company
// Drug -> Country -> Disease -> Company
// Disease -> Country -> Drug -> Company
// Company -> Country -> Disease -> Drug

//    componentDidUpdate(prevProps) {
//    console.log ("In Company Update")
//    console.log(prevProps)

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

//      if ((prevProps.selectedDrugs !== this.props.selectedDrugs && this.props.data === 'Disease') ||
//          (prevProps.selectedDrugs !== this.props.selectedDrugs && this.props.data === 'Country')) {
//        axios
//          .post(
//            "/get_company",
//            {
//              selected_country: this.props.selectedCountry,
//              selected_disease: this.props.selectedDisease,
//              selected_drug: this.props.selectedDrugs,
//            },
//            { headers: { "content-type": "application/json" } }
//          )
//          .then((res) => {
//            const CompanyName = Array.from(res.data);
//            console.log(res.data);
//            this.setState({ CompanyName });
//          });
//      }

//      if (prevProps.selectedDisease !== this.props.selectedDisease && this.props.data === 'Drug') {
//       axios
//         .post(
//           "/get_company_by_drug",
//           {
//             selected_country: this.props.selectedCountry,
//             selected_disease: this.props.selectedDisease,
//             selected_drug: this.props.selectedDrugs,
//           },
//           { headers: { "content-type": "application/json" } }
//         )
//         .then((res) => {
//           const CompanyName = Array.from(res.data);
//           console.log(res.data);
//           this.setState({ CompanyName });
//         });
//     }

//    }

 

  render() {
    //let isDisabled
    console.log(this.props.data)
    // if(this.props.data === "Country"){
    //   isDisabled = !this.props.selectedDrugs;
    // }
    // else if(this.props.data === "Company"){

    // }
    // else if(this.props.data === "Disease"){
    //   isDisabled = !this.props.selectedDrugs;
    // }
    // else if(this.props.data === "Drug"){
    //   isDisabled = !this.props.selectedDisease;
    // }
    // else{
    //   console.log("Error 404")
    // }



    //let isDisabled = !this.props.selectedDrugs;
    return (
      <div>
        <Autocomplete
          //fUpdate={this.updateSelectedCountry.bind(this)}
          //disabled={isDisabled}
          name="Year"
          id="Year"
          options={availableYears}
          getOptionLabel={(option) => option}
          //onChange={this.handleClick.bind(this)}
          onChange={(event, value) => this.handleClick(value)}
          //options={this.state.SelectedYear}
          //getOptionLabel={(name) => name}
          renderInput={(SelectedYear) => (
            <TextField
              {...SelectedYear}
              label="Select a Year"
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
export default Year;
