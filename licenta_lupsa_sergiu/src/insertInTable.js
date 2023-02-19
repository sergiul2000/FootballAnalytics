function insertInTable(nr_of_element, col1, col2, col3) {
  nr_of_element++;
  const tb = document.getElementById("tableBody");
  //   tb.innerHTML.concat(
  //     <tr>
  //       <th scope="row">{nr_of_element}</th>
  //       <td>{col1}</td>
  //       <td>{col2}</td>
  //       <td>{col3}</td>
  //     </tr>
  //   );

  //   const row = tb.insertRow(0);

  //   // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
  //   const cell1 = row.insertCell(0);
  //   const cell2 = row.insertCell(1);
  //   const cell3 = row.insertCell(2);

  //   // Add some text to the new cells:
  //   cell1.innerHTML = "NEW CELL1";
  //   cell2.innerHTML = "NEW CELL2";
  //   cell3.innerHTML = "NEW CELL4";
}

export default insertInTable;
