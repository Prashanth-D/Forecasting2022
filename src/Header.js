import React, {useState} from "react";
import logo from "./logo.png";
import "./App.css";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import Menu from "@material-ui/core/Menu";
import MenuList from "@material-ui/core/MenuList";
import MenuIcon from "@material-ui/icons/Menu";
import Image from "@material-ui/icons/Image";
import { useHistory } from "react-router-dom";
import SimplePopover from "./info"
import SimplePopover_1 from "./page_index"


const useStyles = makeStyles((theme) => ({
  overrides: {
    MuiAppBar: {
      colorPrimary: { color: "black" },
    },
  },
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(5),
  },
  title: {
    flexGrow: 5,
  },
}));

export default function ButtonAppBar() {
  const classes = useStyles({
    overrides: { MuiAppBar: { colorPrimary: { color: "black" } } },
  });

  const history = useHistory();

// The simplepopover is the new dropdow for the header.js
  return (
    
    <div>
      <div id="wholepage">
    <div id="top">
        <div id="buttons">
            <div class="upperSocialBar">
                <div class="socialMediaIconsContainer">
                    <div class="upperIconWrapper">
                        <a href="https://www.instagram.com/gblhealthimpact/" target="_blank">
                            <div class="socialIconUpper iconInstagram"></div>
                        </a>
                    </div>
                    <div class="upperIconWrapper">
                        <a href="https://twitter.com/GBLHealthImpact" target="_blank">
                            <div class="socialIconUpper iconTwitter"></div>
                        </a>
                    </div>
                    <div class="upperIconWrapper">
                        <a href="https://www.facebook.com/GlobalHealthImpactProject" target="_blank">
                            <div class="socialIconUpper iconFacebook"></div>
                        </a>
                    </div>
                </div>

                
              <div class="copyRightUpper">© 2021 GLOBAL HEALTH IMPACT</div>
              </div>
              </div>
              </div>
              </div>
      <AppBar position="static" color="black" elevation={0}>
        <Toolbar>
          <img
            //onClick={handleClick1}
            className="App-logo"
            onClick={() => {
              history.push('/');
            }}
            src={logo}
            alt="logo"
          />
          <Typography variant="h6" className={classes.title}></Typography>
          <Button color="inherit" onClick={() => {
                  history.push('/');
                }}>Home</Button>
          <SimplePopover_1 color="inherit">Index</SimplePopover_1>
          <SimplePopover color="inherit">Info</SimplePopover>
        </Toolbar>
      </AppBar>
      
    </div>
  );
}