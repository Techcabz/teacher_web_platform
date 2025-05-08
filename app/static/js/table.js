$(document).ready(function () {
  // Common DataTable settings
  const commonOptions = {
    dom: "lfrtip",
    responsive: {
      details: true,
      breakpoints: [
        { name: "desktop", width: Infinity },
        { name: "tablet", width: 1024 },
        { name: "fablet", width: 768 },
        { name: "phone", width: 480 },
      ],
    },
    language: {
      paginate: {
        first: "First",
        previous: "Previous",
        next: "Next",
        last: "Last",
      },
    },
    select: true,
    pageLength: 5,
    lengthMenu: [5, 10, 25, 50, 100],
    columnDefs: [{ orderable: false, targets: "_all" }],
  };

  // Initialize simple tables
  const simpleTables = [
    "#datatable",
    "#datatable1",
    "#datatable2",
    "#datatable3",
    "#datatable4",
    "#datatable5",
  ];

  const dataTables = {};

  simpleTables.forEach((selector) => {
    dataTables[selector] = $(selector).DataTable(commonOptions);
  });

  // Filter footer (for #datatable only)
  const filterTable = dataTables["#datatable"];
  $("#datatable tfoot th").each(function (i) {
    if ($(this).text() !== "") {
      const isStatusColumn = $(this).text() === "Status";
      const select = $('<select><option value=""></option></select>')
        .appendTo($(this).empty())
        .on("change", function () {
          const val = $(this).val();
          filterTable
            .column(i)
            .search(val ? "^" + val + "$" : val, true, false)
            .draw();
        });

      if (isStatusColumn) {
        const statusItems = [];
        filterTable
          .column(i)
          .nodes()
          .to$()
          .each(function () {
            const status = $(this).attr("data-filter");
            if ($.inArray(status, statusItems) === -1) statusItems.push(status);
          });
        statusItems.sort();
        $.each(statusItems, (i, item) => {
          select.append(`<option value="${item}">${item}</option>`);
        });
      } else {
        filterTable
          .column(i)
          .data()
          .unique()
          .sort()
          .each(function (d) {
            select.append(`<option value="${d}">${d}</option>`);
          });
      }
    }
  });

  // Schedule tables with export buttons
  const schedTables = ["#datatable_sched1", "#datatable_docs2"];
  schedTables.forEach((selector) => {
    $(selector).DataTable({
      ...commonOptions,
      dom: "l<br>Brtip",
      buttons: [
       
      ],
    });
  });
});
