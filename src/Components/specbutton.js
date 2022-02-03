import React, {useState} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Popover from '@material-ui/core/Popover';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import {withRouter} from 'react-router-dom';
import { useHistory } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
    root:{
      '& > *';{
        margin: theme.spacing(1),
      },
    },
  }));
  export default function OutlinedButtons() {
    const classes = useStyles();
  }

  return (
    <div className={classes.root}>
    <Button variant="contained">Default</Button>
    </Button>
    </div>
    );
  }
  