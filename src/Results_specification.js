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
  
    const classes = useStyles();

//    console.log(data);
//    console.log(props);
    console.log(data.data);
    console.log(data.data["ORIGINAL SPECIFICATIONS"]);
    console.log(data.data["UPDATED SPECIFICATIONS"]);
    
    let orig_spec = data.data["ORIGINAL SPECIFICATIONS"]
    let upd_spec = data.data["UPDATED SPECIFICATIONS"]

    if(upd_spec.hasOwnProperty("Original Impact Score")){
      delete upd_spec["Original Impact Score"];
    }

    let selected_country = data.data["Selected Country"]
    let selected_disease = data.data["Selected Disease"]

    let temp_orig = 0;
    let temp_upd = 0;
    let temp_pct_chng = 0;
    let pct_chng_list = {}
    let pct_chng_list_sorted = {}
    if ((Object.keys(orig_spec).length) > 3) {
        for (const key in orig_spec){
            temp_orig = orig_spec[key];
            temp_upd = upd_spec[key];
            if (temp_orig > temp_upd){
                temp_pct_chng = ((temp_orig - temp_upd) / temp_orig) * 100;
                pct_chng_list[key] = temp_pct_chng;
            } else {
                temp_pct_chng = ((temp_upd - temp_orig) / temp_upd) * 100;
                pct_chng_list[key] = temp_pct_chng;
            }
        }
        console.log(pct_chng_list)
        pct_chng_list_sorted = sortobj(pct_chng_list)
        const sortArrLen = pct_chng_list_sorted.length - 3
        pct_chng_list_sorted.splice(3,sortArrLen)
        console.log(pct_chng_list_sorted)
//        Object.keys(pct_chng_list_sorted).length = 3;
    }

    function sortobj (obj){
            return Object.entries(obj).sort((a,b) => b[1] - a[1])
    }

    console.log(pct_chng_list_sorted)
    let orig_spec_byrank = {}
    let upd_spec_byrank = {}
    if (Object.keys(pct_chng_list_sorted).length > 0) {
        for (const element of pct_chng_list_sorted) {
            let key = element [0]
            orig_spec_byrank[key] = orig_spec[key]
            upd_spec_byrank[key] = upd_spec[key]
        }
//        for (const key in orig_spec){
//            if (!(pct_chng_list_sorted.hasOwnProperty(key))){
//                delete orig_spec[key]
//                delete upd_spec[key]
//            }
//        }
    } else {
        orig_spec_byrank = orig_spec
        upd_spec_byrank = upd_spec
    }

    let orig_spec_vals= []
    let new_spec_vals= []

    let graph1_title = []
    for (const key in orig_spec_byrank){
        graph1_title.push(key)
//        orig_spec_vals.push(['Specification', 'Original' ,orig_spec[key]])
        orig_spec_vals.push(['Specification', orig_spec_byrank[key], upd_spec_byrank[key]])
//        new_spec_vals.push(['Specifcation', 'Updated',upd_spec[key]])
    }

//  let barCol = ['Original Value', 'New Value']
  let barCol = ['Specification', 'Original Value','New Value']
  let barDataAll = []
  let barDataOrig = []
  barDataOrig.unshift(barCol)
  barDataOrig.push(orig_spec_vals[0])
//  barDataOrig.push(new_spec_vals[0])
  barDataAll.push(barDataOrig)

  let barData2Orig = []
  if (Object.keys(orig_spec).length > 1) {
      barData2Orig.unshift(barCol)
      barData2Orig.push(orig_spec_vals[1])
//      barData2Orig.push(new_spec_vals[1])
      barDataAll.push(barData2Orig)
  }

  let barData3Orig = []
  if (Object.keys(orig_spec).length > 2) {
      barData3Orig.unshift(barCol)
      barData3Orig.push(orig_spec_vals[2])
//      barData3Orig.push(new_spec_vals[2])
      barDataAll.push(barData3Orig)
  }
//  for(var i = 0; i < specs_keys.length-1; i++){
//    barDataOrig.push([specs_keys[i], orig_spec[specs_keys[i]]])
//    barDataUpd.push([specs_keys[i], upd_spec[specs_keys[i]]])
//  }

  console.log(barDataAll)
  console.log(barDataOrig)
  console.log(barData2Orig)
  console.log(barData3Orig)

    let i = 0;
   const title_idx = [0,1,2];
    return (
        <div id="wrap">
            <div align="center">
                <Form>
                <Form.Group as={Row}>

                {barDataAll.map((value) => {
                console.log(value);
                let j = 0;
                j = j+i;
                i++;
                return <div align="center">
                    <h3 class="bold">{ graph1_title[j] } </h3>
                    <Chart
                        width={'500px'}
                        height={'300px'}
                        chartType="ColumnChart"
                        loader={<div>Loading Chart</div>}
                        data={value}
                        options={{
                        ///title: { graph1_title[0] },
                        chartArea: { width: '30%' },
                        hAxis: {
                        //title: 'Disability Adjusted Life \n Years Saved',
                        minValue: 0,
                        },
                          vAxis: {
                            title: 'Specification Values',
                          },
                        }}
                        // For tests
                        rootProps={{ 'data-testid': '1' }}
                    />
                    </div>
                    //i++;
                }
                 )
                }

                </Form.Group>
                </Form>
            </div>
        </div>
    )
 }

