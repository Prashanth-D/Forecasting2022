import React, {useState} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Popover from '@material-ui/core/Popover';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';
import ButtonGroup from '@material-ui/core/ButtonGroup';
import {withRouter} from 'react-router-dom';
import { useHistory } from "react-router-dom";

//Creation of the popover/dropdown for the Muiappbar
const useStyles = makeStyles((theme) => ({
  typography: {
    padding: theme.spacing(2),
  },
}));

// Anchor events to position the dropdown below the button
export default function SimplePopover() {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;
  const history = useHistory();
//Return and hierarchy of the popover. I put this into the Header.js spot for the info.
  return (
    <div>
      <Box textAlign= 'top'>
        <Button aria-describedby={id} variant="text" color="inherit" elevation={0} onClick={handleClick}>
        Info
        </Button>
      </Box>
        <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
      >
      <ButtonGroup
        orientation="vertical"
        color="white"
        aria-label="vertical contained primary button group"
        variant="text"
      >
        <Button OnClick={() => {
                  history.push('/options');
                }}>About </Button>
        <Button>News</Button>
        <Button>Resources</Button>
        <Button>Methodology</Button>
        <Button>Organization</Button>        
      </ButtonGroup>
      </Popover>
    </div>
  );
}

