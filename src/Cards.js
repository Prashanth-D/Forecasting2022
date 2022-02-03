import React,{useCallback} from "react";
import {withRouter} from 'react-router-dom';
import { makeStyles } from "@material-ui/core/styles";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";
import GridListTileBar from "@material-ui/core/GridListTileBar";
import ListSubheader from "@material-ui/core/ListSubheader";
import IconButton from "@material-ui/core/IconButton";
import InfoIcon from "@material-ui/icons/Info";
import tileData from "./tileData";
import Link from "@material-ui/core/Link";
import Box from "@material-ui/core/Box";
import Options from "./options";
//var history = require("history")
import { useHistory } from "react-router-dom";



// function nextPath(path) {
  
// }
//const handleOnClick = useCallback(() => history.push('/options'), [history]);



const defaultProps = {
  // bgcolor: "background.paper",
  // m: 0,
  // border: 4,
  // style: { width: "15em" },
};

const useStyles = makeStyles((theme) => ({
  // root: { background: "#18202c",
  //   display: 'flex',
  //   flexWrap: 'wrap',
  //   justifyContent: 'space-around',
  //   overflow: 'hidden',
    

  //  },


  // MuiGridListTileBar: {
  //   root: { background: "#18202c" },
  // },
  // props: {
  //   MuiGridListTileBar: {
  //     root: { background: "#18202c" },
  //   },
  // },
  // overrides: {
  //   MuiBox: { root: { margin: "-1px"} },
  //   MuiGridListTileBar: {
  //     root: { bgcolor: "#18202c" },
  //   },
  //   MuiAppBar: { colorPrimary: { color: "black" } },

  //   MuiAppBar: { colorPrimary: { color: "Black" } },
  // },
  // typography: { background: "rgba(0, 0, 0, 0)" },
  // root: {
  //   display: "flex",
  //   flexWrap: "wrap",
  //   justifyContent: "space-around",
  //   overflow: "hidden",
  //   backgroundColor: theme.palette.background.light,
  // },
  // gridList: {

  // },
  // title: {
  //   color: theme.palette.primary.light,
  // },
  // titleBar: {
  //   background:
  //     "linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, " +
  //     "rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)",
  // },
  // icon: {
  //   color: "rgba(255, 255, 255, 0.54)",
  // },
}));


export default function TitlebarGridList(props) {
  //console.log(props);
  const classes = useStyles({
    // MuiGridListTileBar: {
    //   root: { background: "rgba(0, 0, 0, 0.4)" },
    // },
    // overrides: {
    //   MuiBox: { root: { margin: "-1px" } },
    //   MuiGridListTileBar: {
    //     root: { background: "rgba(0, 0, 0, 0.4)" },
    //   },
    // },

    // root: { background: "white" },
  });

  // const MyComponent = (props) => {
  const history = useHistory();
  
  //   handleOnSubmit = () => {
  //     {history.push('\options');}
  //   };
  // };

  return (
    
    // <div className={classes.root}>
      <div id="wrap2">
      <GridList cellHeight={150} width={200.5} spacing={1} >
      {/* className={classes.gridList} */}
        <GridListTile key="Subheader" cols={2} style={{ height: "auto" }}>
          <ListSubheader component="div" class="centered3">
            <b> </b>
          </ListSubheader>
        </GridListTile>
        
        {tileData.map((tile) => (
          <GridListTile key={tile.img}>
           
          //Removed Box as suggested by Nicole
              <img
                height="100%"
                width="100%"
                src={tile.img}
                alt={tile.title}
                //state = {tile.title}
                onClick={() => {
                  //console.info("I'm a button.");
                  //{handleOnSubmit}
                  //console.log(tile.title)
                  history.push('\options',  tile.title);
                }}
              />
            <Link
              href="https://www.google.com"
              onClick={() => {
                console.info("I'm a button.");
              }}
            ></Link>
          </GridListTile>
        ))}
      </GridList>
    </div>
    // </div>
  );
}