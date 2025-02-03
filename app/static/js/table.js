$(document).ready(function () {
  var table = $("#datatable").DataTable({
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
  });

  var table = $("#datatable1").DataTable({
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
  });

  var table = $("#datatable2").DataTable({
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
  });

  var table = $("#datatable3").DataTable({
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
  });

  var table = $("#datatable4").DataTable({
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
  });

  var table = $("#datatable5").DataTable({
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
  });

  $("#datatable tfoot th").each(function (i) {
    if ($(this).text() !== "") {
      var isStatusColumn = $(this).text() == "Status" ? true : false;
      var select = $('<select><option value=""></option></select>')
        .appendTo($(this).empty())
        .on("change", function () {
          var val = $(this).val();

          table
            .column(i)
            .search(val ? "^" + $(this).val() + "$" : val, true, false)
            .draw();
        });

      // Get the Status values a specific way since the status is a anchor/image
      if (isStatusColumn) {
        var statusItems = [];

        /* ### IS THERE A BETTER/SIMPLER WAY TO GET A UNIQUE ARRAY OF <TD> data-filter ATTRIBUTES? ### */
        table
          .column(i)
          .nodes()
          .to$()
          .each(function (d, j) {
            var thisStatus = $(j).attr("data-filter");
            if ($.inArray(thisStatus, statusItems) === -1)
              statusItems.push(thisStatus);
          });

        statusItems.sort();

        $.each(statusItems, function (i, item) {
          select.append('<option value="' + item + '">' + item + "</option>");
        });
      }
      // All other non-Status columns (like the example)
      else {
        table
          .column(i)
          .data()
          .unique()
          .sort()
          .each(function (d, j) {
            select.append('<option value="' + d + '">' + d + "</option>");
          });
      }
    }
  });

  var table = $("#datatable_sched1").DataTable({
    dom: "l<br>Bfrtip",
    buttons: [
      {
        extend: "print",
        text: "Print",
        autoPrint: true,
        exportOptions: {
          columns: ":visible",
          rows: function (idx, data, node) {
            var dt = new $.fn.dataTable.Api("#example");
            var selected = dt.rows({ selected: true }).indexes().toArray();
            if (selected.length === 0 || $.inArray(idx, selected) !== -1) {
              return true;
            } else {
              return false;
            }
          },
        },

        customize: function (win) {
          $(win.document.body)
            .find("table")
            .addClass("display")
            .css("font-size", "9px");
          $(win.document.body)
            .find("tr:nth-child(odd) td")
            .each(function (index) {
              $(this).css("background-color", "#D0D0D0");
            });
          $(win.document.body).find("h1").css("text-align", "center");
        },
      },

      "colvis",
    ],
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
  });

  var table = $("#datatable_sched2").DataTable({
    dom: "l<br>Bfrtip",
    buttons: [
      {
        extend: "print",
        text: "Print",
        autoPrint: true,
        exportOptions: {
          columns: ":visible",
          rows: function (idx, data, node) {
            var dt = new $.fn.dataTable.Api("#example");
            var selected = dt.rows({ selected: true }).indexes().toArray();
            if (selected.length === 0 || $.inArray(idx, selected) !== -1) {
              return true;
            } else {
              return false;
            }
          },
        },

        customize: function (win) {
          $(win.document.body)
            .find("table")
            .addClass("display")
            .css("font-size", "9px");
          $(win.document.body)
            .find("tr:nth-child(odd) td")
            .each(function (index) {
              $(this).css("background-color", "#D0D0D0");
            });
          $(win.document.body).find("h1").css("text-align", "center");
        },
      },

      "colvis",
    ],
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
  });
});
