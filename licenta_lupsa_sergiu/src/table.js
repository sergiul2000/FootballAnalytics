import React from "react";
import insertInTable from "./insertInTable";
let nr_of_element = 0;

function TableComponent() {
  return (
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">First</th>
          <th scope="col">Last</th>
          <th scope="col">Handle</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
  );
}

// window.onload(insertInTable(nr_of_element, "ana", "are", "mere"));

export default TableComponent;
