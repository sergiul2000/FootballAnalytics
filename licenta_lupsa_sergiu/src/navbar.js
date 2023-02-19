import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import { FaFish, FaPizzaSlice, FaBeer, FaGuitar } from "react-icons/fa";
import { GiRooster } from "react-icons/gi";

function NavScrollExample() {
  return (
    <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark" sticky="top">
      <Container>
        <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <NavDropdown title="Leagues" id="collasible-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">
                <FaFish />
                Premier League
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">
                <FaGuitar />
                La Liga
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">
                <GiRooster />
                Ligue 1
              </NavDropdown.Item>
              {/* <NavDropdown.Divider /> */}
              <NavDropdown.Item href="#action/3.4">
                <FaBeer />
                Bundensliga
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.5">
                <FaPizzaSlice />
                Serie A
              </NavDropdown.Item>
            </NavDropdown>
            <Nav.Link href="#teams">Teams</Nav.Link>
            <Nav.Link href="#players">Players</Nav.Link>
            <NavDropdown title="Dropdown" id="collasible-nav-dropdown">
              <NavDropdown.Item href="#action/3.6">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.7">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Item href="#action/3.8">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.9">
                Separated link
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <Form className="d-flex">
              <Form.Control
                type="search"
                placeholder="Search"
                className="me-2"
                aria-label="Search"
              />
              <Button variant="secondary">Search</Button>
            </Form>
            <Nav.Link href="#deets">Sign in</Nav.Link>
            <Nav.Link href="#memes">Log in</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavScrollExample;
