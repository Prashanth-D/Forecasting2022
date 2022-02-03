import React from "react";
import logo from "./logo.png";
import header from "./ghi_background-2.png";
import "./App.css";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import Image from "@material-ui/icons/Image";

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

export default function Footer() {
  const classes = useStyles({
    overrides: { MuiAppBar: { colorPrimary: { color: "black" } } },
  });

  return (
    <div>
      <AppBar position="static" color="black" elevation={0}>
        <Toolbar>
        <div id="wholepage">
    <div id="foot">
        <div id="buttons">
            <div class="upperSocialBar">
            
            {/* <div id="contact">CONTACT US</div> */}
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
        </Toolbar>
      </AppBar>
    </div>
  );
}
