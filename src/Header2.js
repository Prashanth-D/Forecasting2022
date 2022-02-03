import React from "react";
import logo from "./logo.png";
import header from "./ghi_.png";
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

export default function ButtonAppBar() {
  const classes = useStyles({
    overrides: { MuiAppBar: { colorPrimary: { color: "black" } } },
  });

  return (
    <div id="wrap3">
      <AppBar position="static" color="black" elevation={0}>
        <Toolbar>
          <img
            //onClick={handleClick1}
            className="App-logo"
            src={logo}
            alt="Logo"
          />
          <Typography variant="h6" className={classes.title}></Typography>
          <Button color="inherit">Home</Button>
          <Button color="inherit">Index</Button>
          <Button color="inherit">Info</Button>
        </Toolbar>
      </AppBar>
      
    </div>
  );
}
