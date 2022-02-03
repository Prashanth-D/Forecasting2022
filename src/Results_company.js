import React, { useState, useEffect } from "react";
import logo from "./logo.png";
import header from "./company.jpg";
import "./App.css";
import "react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css";
import RangeSlider from "react-bootstrap-range-slider";
import { Row, Col, Form, Button } from "react-bootstrap";
import { Chart } from "react-google-charts";
import { Link } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
import FormatAlignLeftIcon from '@material-ui/icons/FormatAlignLeft';
import FormatAlignCenterIcon from '@material-ui/icons/FormatAlignCenter';
import FormatAlignRightIcon from '@material-ui/icons/FormatAlignRight';
import FormatBoldIcon from '@material-ui/icons/FormatBold';
import FormatItalicIcon from '@material-ui/icons/FormatItalic';
import FormatUnderlinedIcon from '@material-ui/icons/FormatUnderlined';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';



const useStyles = makeStyles((theme) => ({
  root: {
    width: 'fit-content',
    border: `1px solid ${theme.palette.divider}`,
    borderRadius: theme.shape.borderRadius,
    backgroundColor: theme.palette.background.paper,
    color: theme.palette.text.secondary,
    '& svg': {
      margin: theme.spacing(1.5),
    },
    '& hr': {
      margin: theme.spacing(0, 0.5),
    },
  },
}));


let temp_data = [];
export default function Results(data) {
  console.log(data.data);

  const classes = useStyles();
  temp_data = data.data["TOTAL IMPACTS"]["Company"]
  let selected_company = data.data["Selected Company"]
  let selected_disease = data.data["Selected Disease"]
  let orig_score = data.data["ORIGINAL IMPACTS"]["Company"]
  let new_score = data.data["NEW IMPACTS"]["Company"]

  console.log(data.data["COMPANY/DISEASE"])
  let score_by_dis = data.data["COMPANY/DISEASE"]

  let diff_sp = data.data["diff_specs"]

  let specs_keys = Object.keys(diff_sp);
  let specs_values = Object.values(diff_sp);

  let final_string = "";

  for (const x in diff_sp){
    final_string = final_string + diff_sp[x] + " " + "in " + x + "," + " ";
  }
  let val_inc_dec = "";
  if (new_score/orig_score >= 1){
    val_inc_dec = "increased"
  }
  else{
    val_inc_dec = "decreased"
  }

  let fin_perc = Math.round((Math.abs(new_score - orig_score) /orig_score) *100); 

  //***** SET MAP Values **************
  let orig_impact = [selected_company,orig_score]
  let new_impact = [selected_company,new_score]
  console.log(orig_impact)
  console.log(new_impact)

  let mapCol = ['Company', 'Score']
  if(temp_data.hasOwnProperty(selected_company)){
    delete temp_data[selected_company];
  }
  let mapDataOrig = Object.entries(temp_data)
  mapDataOrig.unshift(mapCol)
  mapDataOrig.push(orig_impact)

  let mapDataNew = Object.entries(temp_data)
  mapDataNew.unshift(mapCol)
  mapDataNew.push(new_impact)

  console.log(mapDataOrig)

//Set Visual 2 data - Score by disease
  let map2DataOrig = Object.entries(score_by_dis)
  map2DataOrig.unshift(mapCol)
  map2DataOrig.push(orig_impact)

  console.log(map2DataOrig)

  let map2DataNew = Object.entries(score_by_dis)
  map2DataNew.unshift(mapCol)
  map2DataNew.push(new_impact)
//End

  console.log(mapDataOrig)
  console.log(mapDataNew)

  //** Company/Disease Map Values ******//
  //********* SET DISEASE SCORE VALUE  **********
  let orig_dis_impact = [selected_company,orig_score]
  let new_dis_impact = [selected_company,new_score]
  let barCol = ['Disease', 'Score']
  let barDataOrig = []
  barDataOrig.unshift(mapCol)
  barDataOrig.push(orig_dis_impact)

  let barDataNew = []
  barDataNew.unshift(mapCol)
  barDataNew.push(new_dis_impact)

//Set Visual 4 data - by ranking
  let orig_data4 = {}
  let new_data4 = {}
  orig_data4 = temp_data
  new_data4 = temp_data
  orig_data4[selected_company] = []
  new_data4[selected_company] = []
  orig_data4[selected_company].push(orig_score)
  new_data4[selected_company].push(new_score)
  console.log(orig_data4)
  console.log(new_data4)
//  let map4DataOrig = Object.entries(orig_data4).sort((a,b)) => b[1] - a[1])
  let map4DataOrig = sortobj(orig_data4)
  map4DataOrig.unshift(mapCol)
  console.log(map4DataOrig)

  let map4DataNew = sortobj(new_data4)
  map4DataNew.unshift(mapCol)
  console.log(map4DataNew)

  function sortobj (obj){
        return Object.entries(obj).sort((a,b) => b[1] - a[1])
  }
//End


  return (
        <div id="wrap">
            <div class="row">
                <div class="column">
                    <div class="left-column-extended" align="center">
                        <h1 class="original-impact"><span class="bold">Original</span> Impact</h1>
                          <p class="map-titles"><span class="bold">Impact Score by Company</span></p>
                          <Chart
                              width={'500px'}
                              height={'300px'}
                              chartType="PieChart"
                              loader={<div>Loading Chart</div>}
                              data={mapDataOrig}
                              options={{
                              // Just add this option
                              is3D: true,
                              pieSliceText: 'value',
                              sliceVisibilityThreshold: 0.00000001,
                              tooltip: {
                                  trigger: 'selection',
                                  text: 'value',
                              }
                              }}
                              rootProps={{ 'data-testid': '2' }}
                           />
                          <p class="map-titles"><span class="bold">Impact Score by Disease</span></p>
                          <Chart
                            width={'500px'}
                            height={'300px'}
                            chartType="PieChart"
                            loader={<div>Loading Chart</div>}
                            data={map2DataOrig}
                            options={{
                            // Just add this option
                            is3D: true,
                            pieSliceText: 'value',
                            sliceVisibilityThreshold: 0.00000001,
                            tooltip: {
                                trigger: 'selection',
                                text: 'value',
                            }
                            }}
                            rootProps={{ 'data-testid': '2' }}
                         />                         
                          <p class="map-titles"><span class="bold">Total Impact Score</span></p>
                          <Chart
                            width={'500px'}
                            height={'300px'}
                            chartType="BarChart"
                            loader={<div>Loading Chart</div>}
                            data={barDataOrig}
                            options={{
                            chartArea: { width: '50%' },
//                          colorAxis: {colors : ['#548A9B', '#C0E188', '#EE8D7D']},
                            hAxis: {
                            //title: 'Disability Adjusted Life \n Years Saved',
                            minValue: 0,
                            },
                            pieSliceText: 'value',
                            sliceVisibilityThreshold: 0.00000001,
                            tooltip: {
                                trigger: 'selection',
                                text: 'value',
                            }
                            // vAxis: {
                            //   title: 'City',
                            // },
                            }}
                            // For tests
                            rootProps={{ 'data-testid': '1' }}
                          />

                          <p class="map-titles"><span class="bold">Patient Holders Total Drug Scores</span></p>
                          <Chart
                            width={'500px'}
                            height={'300px'}
                            chartType="BarChart"
                            loader={<div>Loading Chart</div>}
                            data={map4DataOrig}
                            options={{
                            chartArea: { width: '50%' },
//                          colorAxis: {colors : ['#548A9B', '#C0E188', '#EE8D7D']},
                            hAxis: {
                            //title: 'Disability Adjusted Life \n Years Saved',
                            minValue: 0,
                            },
                            pieSliceText: 'value',
                            sliceVisibilityThreshold: 0.00000001,
                            tooltip: {
                                trigger: 'selection',
                                text: 'value',
                            }
                            // vAxis: {
                            //   title: 'City',
                            // },
                            }}
                            // For tests
                            rootProps={{ 'data-testid': '1' }}
                          />
                      </div>
                  </div>
                <div class="company-divider" align="center"></div>
                  <div class="column"> 
                      <div class="right-column-extended" align="center">
                          <h1 class="new-impact"><span class="bold">New</span> Impact</h1> 
                          <p class="map-titles"><span class="bold">Impact Score by Company</span></p>              
                          <Chart
                            width={'500px'}
                            height={'300px'}
                            chartType="PieChart"
                            loader={<div>Loading Chart</div>}
                            data={mapDataNew}
                            options={{
                            // Just add this option
                            is3D: true,
                            pieSliceText: 'value',
                            sliceVisibilityThreshold: 0.00000001,
                            tooltip: {
                                trigger: 'selection',
                                text: 'value',
                            }
                            }}
                            rootProps={{ 'data-testid': '2' }}
                          />
                          <p class="map-titles"><span class="bold">Impact Score by Disease</span></p>
                          <Chart
                            width={'500px'}
                            height={'300px'}
                            chartType="PieChart"
                            loader={<div>Loading Chart</div>}
                            data={map2DataNew}
                            options={{
                            // Just add this option
                            is3D: true,
                            pieSliceText: 'value',
                            sliceVisibilityThreshold: 0.00000001,
                            tooltip: {
                                trigger: 'selection',
                                text: 'value',
                            }
                            }}
                            rootProps={{ 'data-testid': '2' }}
                          />
                          <p class="map-titles"><span class="bold">Total Impact Score</span></p>
                          <Chart
                            width={'500px'}
                            height={'300px'}
                            chartType="BarChart"
                            loader={<div>Loading Chart</div>}
                            data={barDataNew}
                            options={{
                            chartArea: { width: '50%' },
                            hAxis: {
                            //title: 'Disability Adjusted Life \n Years Saved',
                            minValue: 0,
                            },
                            pieSliceText: 'value',
                            sliceVisibilityThreshold: 0.00000001,
                            tooltip: {
                                trigger: 'selection',
                                text: 'value',
                            }
                            // vAxis: {
                            //   title: 'City',
                            // },
                            }}
                            // For tests
                            rootProps={{ 'data-testid': '1' }}
                          />   
                            <p class="map-titles"><span class="bold">Patient Holders Total Drug Scores</span></p>
                            <Chart
                              width={'500px'}
                              height={'300px'}
                              chartType="BarChart"
                              loader={<div>Loading Chart</div>}
                              data={map4DataNew}
                              options={{
                              chartArea: { width: '50%' },
  //                          colorAxis: {colors : ['#548A9B', '#C0E188', '#EE8D7D']},
                              hAxis: {
                              //title: 'Disability Adjusted Life \n Years Saved',
                              minValue: 0,
                              },
                              pieSliceText: 'value',
                              sliceVisibilityThreshold: 0.00000001,
                              tooltip: {
                                  trigger: 'selection',
                                  text: 'value',
                              }
                              // vAxis: {
                              //   title: 'City',
                              // },
                              }}
                              // For tests
                              rootProps={{ 'data-testid': '1' }}
                            /> 
                      </div>
                 </div>

             </div>




         </div>
    )
 }

