// import logo from "./logo.svg";
import "./App.css";
import NavScrollExample from "./navbar";
import TableComponent from "./table";

function App() {
  return (
    <>
      <header>
        <NavScrollExample />{" "}
      </header>
      <div className="paragraph">
        <TableComponent />
      </div>
    </>
  );
}

export default App;
