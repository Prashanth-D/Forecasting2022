import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import logo from "./logo.png";
import header from "./forecast.jpg";
import "./App.css";
import "react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css";
import RangeSlider from "react-bootstrap-range-slider";
import {
  Row,
  Col,
  Form,
  Button,
  Navbar,
  Nav,
  NavDropdown,
  FormControl,
} from "react-bootstrap";

// You can choose your kind of history here (e.g. browserHistory)
//import { Router } from "react-router";
// Your routes.js file
//import routes from "./routes";
import { Link, withRouter, NavLink, useHistory } from "react-router-dom";

export default function App(data) {
  //const { data } = props.location
  //console.log(data.data);
  var keys = [];
  var values = [];

  for(var k in data.data) keys.push(k);


  const [value1, setValue1] = useState(0);
  const [value2, setValue2] = useState(0);
  const [value3, setValue3] = useState(0);
  const [value4, setValue4] = useState(0);
  const [value5, setValue5] = useState(0);

  const history = useHistory();

  function simulateNetworkRequest() {
    return new Promise((resolve) => setTimeout(resolve, 2000));
  }

  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    if (isLoading) {
      simulateNetworkRequest().then(() => {
        setLoading(false);
      });
    }
  }, [isLoading]);

  const handleClick = () => {
    setLoading(true);
    history.push("/result");
  };

  const handleClick1 = () => {
    history.push("/");
  };

  //ReactDOM.App(<Router routes={routes} />, document.getElementById("your-app"));

  return (
    <div className="">
      {/* <header className="App-header">
        <div className="logo">
          <img
            onClick={handleClick1}
            className="App-logo"
            src={logo}
            alt="Logo"
          />
        </div>
        <div className="header-img">
          <img className="App-header-img" src={header} alt="Header" />
        </div> */}

        {/* <div>
          <Navbar bg="light" expand="lg">
            <Navbar.Brand href="#home"></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                <Nav.Link href="#home">Home </Nav.Link>
                <Nav.Link href="#link">Info</Nav.Link>
                <NavDropdown title="Index" id="basic-nav-dropdown">
                  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.2">
                    Another action
                  </NavDropdown.Item>
                  <NavDropdown.Item href="#action/3.3">
                    Something
                  </NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item href="#action/3.4">
                    Separated link
                  </NavDropdown.Item>
                </NavDropdown>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
        </div> */}
        <div>
          <h2>Specification</h2>
          <Form>
            <Form.Group as={Row}>
              <Col xs="9">
                <Form.Label>Overall Treatment Coverage {keys[0]} </Form.Label>
                <RangeSlider
                  value={value1}
                  onChange={(changeEvent) =>
                    setValue1(changeEvent.target.value)
                  }
                  size="sm"
                />
              </Col>
              <Col xs="9">
                <Form.Label>Adult Treatment Coverage {keys[1]} </Form.Label>
                <RangeSlider
                  value={value2}
                  onChange={(changeEvent) =>
                    setValue2(changeEvent.target.value)
                  }
                  size="sm"
                />
              </Col>
              <Col xs="9">
                <Form.Label>Children Treatment Coverage {keys[2]}</Form.Label>
                <RangeSlider
                  value={value3}
                  //value={data.data.keys[2]}
                  onChange={(changeEvent) =>
                    setValue3(changeEvent.target.value)
                  }
                  size="sm"
                />
              </Col>
              <Col xs="9">
                <Form.Label>Retention Rate {keys[3]}</Form.Label>
                <RangeSlider
                  value={value4}
                  onChange={(changeEvent) =>
                    setValue4(changeEvent.target.value)
                  }
                  size="sm"
                />
              </Col>
              <Col xs="9">
                <Form.Label>DALYs {keys[4]}</Form.Label>
                <RangeSlider
                  value={value5}
                  onChange={(changeEvent) =>
                    setValue5(changeEvent.target.value)
                  }
                  size="sm"
                />
              </Col>
            </Form.Group>
          </Form>

          <Button
            variant="primary"
            disabled={isLoading}
            onClick={!isLoading ? handleClick : null}
          >
            {isLoading ? "Loading…" : "ForeCasting"}
          </Button>
        </div>
      {/* {/* </header> */}
    </div>
  );
}